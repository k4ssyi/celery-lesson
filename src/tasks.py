from random import randint
from time import sleep

from celery import Celery, chord, group

app = Celery("tasks")
app.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost",
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Europe/Oslo",
    enable_utc=True,
    result_expires=3600,
)


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task
def hello(m):
    sleep(randint(0, 2))
    return m


@app.task
def build_server():
    print("wait 10 sec")
    sleep(10)
    server_id = randint(1, 100)
    return server_id


@app.task
def build_servers():
    """グループ化"""
    g = group(build_server.s() for _ in range(10))
    return g()


@app.task
def callback(result):
    for server_id in result:
        print(server_id)
    print("clean up")
    return "Done"


@app.task
def build_servers_with_cleanup():
    """コールバック"""
    c = chord((build_server.s() for _ in range(10)), callback.s())
    return c()


@app.task
def setup_dns(server_id):
    """チェーン"""
    print(f"setup dns for {server_id}")
    return f"done for {server_id}"


@app.task
def deploy_customer_server():
    """チェーン"""
    chain = build_server.s() | setup_dns.s()
    return chain()
