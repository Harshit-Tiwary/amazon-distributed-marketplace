import pika
import json
import time

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "marketplace_events"


def process_payment(order):

    print("Processing payment for order:", order)

    time.sleep(2)

    print("Payment successful for order:", order["order_id"])


def callback(ch, method, properties, body):

    message = json.loads(body)

    if message["event_type"] == "ORDER_CREATED":

        order = message["payload"]

        process_payment(order)


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

    queue = channel.queue_declare(queue="", exclusive=True)

    queue_name = queue.method.queue

    channel.queue_bind(
        exchange=EXCHANGE_NAME,
        queue=queue_name
    )

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("Payment Service waiting for events...")

    channel.start_consuming()