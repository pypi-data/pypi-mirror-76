from trending_bay_messaging.client import Client

def consume(channel, callback, exchange = None ,**kwargs):
    client = Client(channel=channel)
    if exchange is None:
        exchange = "DEFAULT_EXCHANGE"
    while True:
        for method_frame, properties, body in channel.consume(exchange):
            print(method_frame, properties, body)
            channel.basic_ack(method_frame.delivery_tag)

            if method_frame.delivery_tag == 10:
                raise Exception("too many delivery tags".format(method_frame))
            callback(body)