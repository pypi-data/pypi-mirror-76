import json

def get_routing_key(method, topic):
    return "{topic}.{method}".format(topic=topic, method=method)

class Message(object):
    def __init__(self, method, topic, body):
        self.method = method
        self.topic = topic
        self.body = body
        self.routing_key = get_routing_key(method, topic)

    def get_dict(self):
        return {
            "method": self.method,
            "topic": self.topic,
            "body": self.body
        }

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_body_as_json(self):
        return json.dumps(self.body)

def from_dict(dic):
    return Message(dic["method"], dic["topic"], dic["body"])

def from_json(js):
    return from_dict(json.loads(js))
