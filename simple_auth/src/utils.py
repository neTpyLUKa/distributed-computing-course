import os
import json

import pika


class MessageQueueClass:
    def __init__(self, queue="email"):
        self.queue_ = queue
        self.connection_ = None
        self.channel_ = None

    # TODO transform token to email message with url(token)
    def send(self, email, token):
        if not self.connection_:
            self.connection_ = pika.BlockingConnection(
                pika.ConnectionParameters('rabbitmq', port=os.environ.get("MQ_PORT")))
            self.channel_ = self.connection_.channel()
            self.channel_.queue_declare(queue=self.queue_)

        self.channel_.basic_publish(exchange='', routing_key=self.queue_,
                                    body=json.dumps({"email": email, "token": token}))


message_queue = MessageQueueClass()
