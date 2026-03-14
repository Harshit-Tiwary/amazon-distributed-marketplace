import pika
import json

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "marketplace_events"

inventory_db = {
    1: 10,
    2: 5
}


def process_inventory(order):

    product_id = order["product_id"]
    quantity = order["quantity"]

    print("Checking inventory for product:", product_id)

    if inventory_db.get(product_id, 0) >= quantity:

        inventory_db[product_id] -= quantity

        print("Stock reserved for order:", order["order_id"])

    else:

        print("Out of stock for product:", product_id)


def callback(ch, method, properties, body):

    message = json.loads(body)

    if message["event_type"] == "ORDER_CREATED":

        order = message["payload"]

        process_inventory(order)


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

    print("Inventory Service waiting for events...")

    channel.start_consuming()