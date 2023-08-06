import asyncio
import time

import httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt  # type: ignore
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

__version__ = "0.0.1"


class CloudTaskAuth:
    # https://developers.google.com/identity/protocols/oauth2/openid-connect#discovery
    discovery_url = "https://accounts.google.com/.well-known/openid-configuration"

    def __init__(self):
        self._jwks_uri = None
        self._public_keys = None
        self._public_keys_timestamp = 0
        self._lock = asyncio.Lock()

    async def _get_jwk_uri(self, client):
        if self._jwks_uri is None:
            resp = await client.get(self.discovery_url)
            self._jwks_uri = resp.json()["jwks_uri"]
        return self._jwks_uri

    async def _fetch_public_keys(self) -> None:
        async with self._lock:
            if self._public_keys is not None and (
                time.time() - self._public_keys_timestamp <= 300
            ):
                return
            async with httpx.AsyncClient() as client:
                jwks_uri = await self._get_jwk_uri(client)
                resp = await client.get(jwks_uri)
                self._public_keys = resp.json()["keys"]
                self._public_keys_timestamp = time.time()

    async def __call__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        if request.headers.get("user-agent") != "Google-Cloud-Tasks":
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid user agent")
        header = jwt.get_unverified_header(token.credentials)
        await self._fetch_public_keys()
        for public_key in self._public_keys:
            if public_key["kid"] == header["kid"]:
                try:
                    claims = jwt.decode(
                        token.credentials, public_key, audience=str(request.url),
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail=f"Invalid Token {e}",
                    )
                break
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown Token"
            )

        hs = request.headers
        return CloudTask(
            queue_name=hs["x-cloudtasks-queuename"],
            name=hs["x-cloudtasks-taskname"],
            retry_count=int(hs["x-cloudtasks-taskretrycount"]),
            execution_count=int(hs["x-cloudtasks-taskexecutioncount"]),
            eta=float(hs["x-cloudtasks-tasketa"]),
            claims=claims,
        )


cloud_task_auth = CloudTaskAuth()


class CloudTask(BaseModel):
    queue_name: str
    name: str
    retry_count: int
    execution_count: int
    eta: float
    claims: dict
