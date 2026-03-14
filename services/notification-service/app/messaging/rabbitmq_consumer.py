import pika
import json

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "marketplace_events"


def callback(ch, method, properties, body):
    event = json.loads(body)

    event_type = event["event_type"]
    payload = event["payload"]

    print(f"[Notification Service] Event received: {event_type}")
    print(f"[Notification Service] Payload: {payload}")

    if event_type == "PRODUCT_CREATED":
        print("Sending notification for new product...")


def start_consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )

    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type="fanout",
        durable=True
    )

    result = channel.queue_declare(queue="", exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name
    )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("Notification Service waiting for events...")
    channel.start_consuming()