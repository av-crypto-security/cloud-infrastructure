import os
import time
import logging
import requests
import psycopg2


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONNECTION_ID = os.getenv("CONNECTION_ID")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
VERBOSE_LOG = os.getenv("VERBOSE_LOG", "False") == "True"

TARGET_URL = os.getenv("TARGET_URL", "https://ya.ru")


def log(msg):
    if VERBOSE_LOG:
        logger.info(msg)


def validate_env():
    if not CONNECTION_ID or not DB_USER or not DB_HOST:
        raise ValueError("Missing required environment variables")


def measure():
    start = time.time()

    try:
        response = requests.get(TARGET_URL, timeout=(1, 3))
        duration = time.time() - start
        return response.status_code, duration

    except requests.exceptions.ConnectTimeout:
        return 602, 0

    except requests.exceptions.ReadTimeout:
        return 601, 0

    except requests.exceptions.Timeout:
        return 603, 0

    except Exception:
        return 500, 0


def save(result, duration, context):
    conn = psycopg2.connect(
        database=CONNECTION_ID,
        user=DB_USER,
        password=context.token["access_token"],
        host=DB_HOST,
        port=6432,
        sslmode="require",
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO measurements (result, response_time) VALUES (%s, %s)",
                (result, duration),
            )
        conn.commit()

    finally:
        conn.close()


def handler(event, context):
    logger.info("Monitoring function invoked")

    try:
        validate_env()

        result, duration = measure()

        log(f"Result={result}, Duration={duration}")

        save(result, duration, context)

        return {
            "statusCode": result,
            "body": "Measurement stored"
        }

    except Exception as e:
        logger.exception("Monitoring function failed")

        return {
            "statusCode": 500,
            "body": "Internal error"
        }