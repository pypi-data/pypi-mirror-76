# fastapi-authenticator
from fastapi import Depends, FastAPI
fastapi authenticator for google cloud tasks

## Installation

server:

~~~
pip3 install fastapi-authenticator
~~~

client:

~~~
pip3 install gcp-taskqueue
~~~

## Usage

server:

~~~python
from fastapi_authenticator import CloudTask, cloud_task_auth

app = FastAPI()

@app.post("/task1")
def task_handler(task: CloudTask: Depends(cloud_task_auth)):
    ...
~~~

client:

~~~python
from gcp_taskqueue import TaskQueue

queue = TaskQueue(queue_id="your-queue-name")

queue.create_http_task("https://url", deadline=300)
~~~
