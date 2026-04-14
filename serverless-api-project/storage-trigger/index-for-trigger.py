import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def safe_serialize(data):
    try:
        return json.dumps(data)
    except Exception:
        return str(data)


def handler(event, context):
    logger.info("Trigger function invoked")

    try:
        logger.info(f"Event payload: {safe_serialize(event)}")

        if context:
            logger.info(f"Request ID: {getattr(context, 'request_id', 'unknown')}")

        return {
            "statusCode": 200,
            "body": "Event processed successfully"
        }

    except Exception as e:
        logger.error(f"Error processing event: {e}")

        return {
            "statusCode": 500,
            "body": "Internal error"
        }
