from trending_bay_messaging.client import Client
from trending_bay_messaging.connect import connect

def request(host, port, message, publish_only = False, exchange = None, **kwargs):
    print("REQUESTING")
    if exchange is None:
        exchange = "DEFAULT_ROUTE_EX"
    connection = connect(host, port)
    channel = connection.channel()
    # channel.exchange_declare(exchange, exchange_type="topic")
    client = Client(channel=channel, publish_only=publish_only, exchange=exchange)
    return client.request(message, exchange, **kwargs)