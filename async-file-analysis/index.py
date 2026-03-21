import json
import os
import uuid
import requests
import boto3

QUEUE_URL = os.getenv("YMQ_QUEUE_URL")
S3_BUCKET = os.getenv("S3_BUCKET")

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url=os.getenv("DOCAPI_ENDPOINT"),
    region_name="ru-central1"
)

table = dynamodb.Table("analysis_tasks")

sqs = boto3.client(
    "sqs",
    endpoint_url="https://message-queue.api.cloud.yandex.net",
    region_name="ru-central1"
)

s3 = boto3.client(
    "s3",
    endpoint_url="https://storage.yandexcloud.net",
    region_name="ru-central1"
)


# -------- API --------

def create_task(file_url):
    task_id = str(uuid.uuid4())

    table.put_item(Item={
        "task_id": task_id,
        "status": "pending"
    })

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({
            "task_id": task_id,
            "file_url": file_url
        })
    )

    return {"task_id": task_id}


def get_status(task_id):
    response = table.get_item(Key={"task_id": task_id})
    item = response.get("Item")

    if not item:
        return {"error": "not found"}

    return item


def handle_api(event, context):
    action = event.get("action")

    if action == "analyze":
        return create_task(event.get("file_url"))

    elif action == "status":
        return get_status(event.get("task_id"))

    return {"error": "unknown action"}


# -------- WORKER --------

def analyze_file(file_url):
    response = requests.get(file_url, timeout=5)
    size = len(response.content)

    return {
        "size": size,
        "status": "clean"  # mock analysis
    }


def handle_worker(event, context):
    for msg in event["messages"]:
        body = json.loads(msg["details"]["message"]["body"])

        task_id = body["task_id"]
        file_url = body["file_url"]

        result = analyze_file(file_url)

        table.update_item(
            Key={"task_id": task_id},
            UpdateExpression="SET #s = :s, result = :r",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={
                ":s": "done",
                ":r": result
            }
        )

    return "ok"