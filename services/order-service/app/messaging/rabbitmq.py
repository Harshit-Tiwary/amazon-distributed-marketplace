import pika
import json

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "marketplace_events"


def publish_event(event_type: str, payload: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="fanout",
        durable=True
    )

    message = {
        "event_type": event_type,
        "payload": payload
    }

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=json.dumps(message)
    )

    connection.close()