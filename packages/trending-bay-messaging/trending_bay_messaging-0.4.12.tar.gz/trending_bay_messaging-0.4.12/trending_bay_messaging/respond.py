import pika
import json
from trending_bay_messaging.Message import Message, from_json

def respond(connection, callback, topics = [], app_name = "", exchange=None, publish = True, **kwargs):
    if exchange is None:
        exchange = "DEFAULT_ROUTE_EX"
    channel = connection.channel()
    channel.exchange_declare(exchange, exchange_type="topic")
    # result = channel.queue_declare(queue='', exclusive=True)
    result = channel.queue_declare(queue=app_name)
    for topic in topics:
        channel.queue_bind(exchange=exchange, queue=result.method.queue, routing_key="{}.*".format(topic))
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=result.method.queue, on_message_callback=lambda ch, method, props, body: on_request(callback, ch, method, props, body, exchange, publish))

    print(" [x] Awaiting Requests")
    channel.start_consuming()

def on_request(callback, ch, method, props, message, exchange, publish = True):
    print("received a message with topic {} method {}".format(from_json(message).topic, from_json(message).method))
    json_msg = from_json(message)
    response = callback(json_msg)

    print("responding with {}".format(response))

    if publish:

        ch.basic_publish(exchange=exchange,
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id = \
                                                             props.correlation_id),
                         body=Message(json_msg.method, json_msg.topic, response).get_json())
        ch.basic_ack(delivery_tag=method.delivery_tag)
