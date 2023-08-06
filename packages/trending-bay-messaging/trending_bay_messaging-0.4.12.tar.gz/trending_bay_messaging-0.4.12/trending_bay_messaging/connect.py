import pika

def connect(host = 'localhost', port = 5672, **kwargs):
    parameters = pika.ConnectionParameters(
        host=host, port=port
    )

    connection = pika.BlockingConnection(parameters=parameters)
    # channel = connection.channel()
    return connection