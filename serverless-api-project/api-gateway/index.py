import os
import json
import logging
import psycopg2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONNECTION_ID = os.getenv("CONNECTION_ID")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
API_TOKEN = os.getenv("API_TOKEN")


def validate_env():
    if not CONNECTION_ID or not DB_USER or not DB_HOST or not API_TOKEN:
        raise ValueError("Missing required environment variables")


def get_connection(context):
    return psycopg2.connect(
        database=CONNECTION_ID,
        user=DB_USER,
        password=context.token["access_token"],
        host=DB_HOST,
        port=6432,
        sslmode="require",
    )


def fetch_results(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT result, response_time
            FROM measurements
            ORDER BY time DESC
            LIMIT 50
        """)
        rows = cursor.fetchall()

    return [
        {
            "status": r[0],
            "response_time": r[1]
        }
        for r in rows
    ]


def handler(event, context):
    logger.info("API function invoked")

    try:
        validate_env()

        params = event.get("queryStringParameters") or {}
        token = params.get("token")

        if token != API_TOKEN:
            return {
                "statusCode": 401,
                "body": "Unauthorized"
            }

        conn = get_connection(context)

        try:
            results = fetch_results(conn)
        finally:
            conn.close()

        return {
            "statusCode": 200,
            "body": json.dumps({"results": results})
        }

    except Exception:
        logger.exception("API function failed")

        return {
            "statusCode": 500,
            "body": "Internal error"
        }