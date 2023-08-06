import json

def publish(channel, routing_key, body, exchange = None, **kwargs):
    if exchange is None:
        exchange = "DEFAULT_EXCHANGE"
    return channel.basic_publish(exchange=exchange, routing_key=routing_key,
                          body=json.dumps(body))