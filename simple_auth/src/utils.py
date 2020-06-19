import os
import json
import socket

import netifaces as netifaces
import pika


def form_body(token):
    auth_port = os.environ.get("AUTH_PORT")
    ip = "192.168.1.75" #netifaces.ifaddresses('wlp1s0')[netifaces.AF_INET][0]['addr'] # TODO get ip somehow
    return f"To confirm your registration click on this link \n\n" \
           f"http://{ip}:{auth_port}/confirm_email?token={token}\n\n" \
           f"This link is available only for 12 hours"


class MessageQueueClass:
    def __init__(self, queue):
        self.queue_ = queue
        self.connection_ = None
        self.channel_ = None

    # TODO retry publish ?
    def send(self, address, token, retry_count=10):
        if not self.connection_:
            self.connection_ = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBITMQ_NAME'), port=os.environ.get("MQ_PORT")))
            self.channel_ = self.connection_.channel()
            self.channel_.queue_declare(queue=self.queue_)

        self.channel_.basic_publish(exchange='', routing_key=self.queue_,
                                    properties=pika.BasicProperties(content_type='application/json'),
                                    body=json.dumps({"address": address, "body": form_body(token),
                                                     "subject": "Email confirmation from Online Store",
                                                     "retry_count": retry_count}))


message_queue_email = MessageQueueClass(queue=os.environ.get("QUEUE_EMAIL"))
message_queue_sms = MessageQueueClass(queue=os.environ.get("QUEUE_SMS"))
