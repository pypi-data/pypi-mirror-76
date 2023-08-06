import pika
import uuid
import json
from trending_bay_messaging.Message import Message, from_json

class Client(object):

    def __init__(self, channel, publish_only = False, exchange = None):
        # self.connection = pika.BlockingConnection(
        #     pika.ConnectionParameters(host='localhost'))
        #
        # self.channel = self.connection.channel()
        self.channel = channel

        self.exchange = exchange

        self.publish_only = publish_only

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self, message, exchange = None ,**kwargs):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        if exchange is None:
            if self.exchange is None:
                exchange = "DEFAULT_ROUTE_EX"
        print("publishing to topic {} method {}".format(message.topic, message.method))
        self.channel.queue_bind(exchange=exchange, queue=self.callback_queue, routing_key=self.callback_queue)

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=message.routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message.get_json())
        if not self.publish_only:
            while self.response is None:
                self.channel.connection.process_data_events()
            return from_json(self.response).body
        else:
            return

