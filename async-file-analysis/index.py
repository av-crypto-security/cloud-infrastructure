import hashlib
import time
import json
import os
#import requests
import subprocess
import uuid
from urllib.parse import urlencode

import boto3
import yandexcloud
from yandex.cloud.lockbox.v1.payload_service_pb2 import GetPayloadRequest
from yandex.cloud.lockbox.v1.payload_service_pb2_grpc import PayloadServiceStub

boto_session = None
storage_client = None
docapi_table = None
ymq_queue = None


def get_boto_session():
    global boto_session
    if boto_session is not None:
        return boto_session

    # initialize lockbox and read secret value
    yc_sdk = yandexcloud.SDK()
    channel = yc_sdk._channels.channel("lockbox-payload")
    lockbox = PayloadServiceStub(channel)
    response = lockbox.Get(GetPayloadRequest(secret_id=os.environ['SECRET_ID']))

    # extract values from secret
    access_key = None
    secret_key = None
    for entry in response.entries:
        if entry.key == 'ACCESS_KEY_ID':
            access_key = entry.text_value
        elif entry.key == 'SECRET_ACCESS_KEY':
            secret_key = entry.text_value
    if access_key is None or secret_key is None:
        raise Exception("secrets required")
    print("Key id: " + access_key)

    # initialize boto session
    boto_session = boto3.session.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    return boto_session


def get_ymq_queue():
    global ymq_queue
    if ymq_queue is not None:
        return ymq_queue

    ymq_queue = get_boto_session().resource(
        service_name='sqs',
        endpoint_url='https://message-queue.api.cloud.yandex.net',
        region_name='ru-central1'
    ).Queue(os.environ['YMQ_QUEUE_URL'])
    return ymq_queue


def get_docapi_table():
    global docapi_table
    if docapi_table is not None:
        return docapi_table

    docapi_table = get_boto_session().resource(
        'dynamodb',
        endpoint_url=os.environ['DOCAPI_ENDPOINT'],
        region_name='ru-central1'
    ).Table('tasks')
    return docapi_table


def get_storage_client():
    global storage_client
    if storage_client is not None:
        return storage_client

    storage_client = get_boto_session().client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        region_name='ru-central1'
    )
    return storage_client

# API LOGIC

def create_task():
    task_id = str(uuid.uuid4())

    object_name = "sample.bin"  # file saved in the Object Storage

    get_docapi_table().put_item(Item={
        'task_id': task_id,
        'ready': False
    })

    get_ymq_queue().send_message(
        MessageBody=json.dumps({
            'task_id': task_id,
            'object_name': object_name
        })
    )

    return {
        'task_id': task_id
    }


def get_task_status(task_id):
    task = get_docapi_table().get_item(Key={
        "task_id": task_id
    })

    if 'Item' not in task:
        return {"error": "task not found"}

    if task['Item']['ready']:
        return {
            'ready': True,
            'result': task['Item']['result']
        }

    return {'ready': False}


def handle_api(event, context):
    action = event.get('action')

    if action == 'analyze':
        return create_task()

    elif action == 'get_task_status':
        return get_task_status(event['task_id'])

    return {"error": "unknown action"}
    
# ANALYSIS (WORKER)

def mock_analysis(data: bytes):
    time.sleep(2)                # heavy load imitation

    sha256 = hashlib.sha256(data).hexdigest()

    verdict = "malicious" if int(sha256, 16) % 2 == 0 else "clean"

    return {
        "sha256": sha256,
        "verdict": verdict,
        "size": len(data)
    }


def handle_process_event(event, context):
    for message in event['messages']:
        task_json = json.loads(message['details']['message']['body'])

        task_id = task_json['task_id']
        object_name = task_json['object_name']

        # read file from Object Storage
        obj = get_storage_client().get_object(
            Bucket=os.environ['S3_BUCKET'],
            Key=object_name
        )

        data = obj['Body'].read()

        # analysis
        result = mock_analysis(data)

        # save the result
        get_docapi_table().update_item(
            Key={'task_id': task_id},
            AttributeUpdates={
                'ready': {'Value': True, 'Action': 'PUT'},
                'result': {'Value': json.dumps(result), 'Action': 'PUT'},
            }
        )

    return "OK"
