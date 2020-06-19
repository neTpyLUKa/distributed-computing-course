import os

import pika as pika


class MessageQueueClass:
    def __init__(self, queue):
        self.queue = queue
        self.connection = None
        self.channel = None

    def consuming_loop(self, callback):
        if not self.connection:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=os.environ.get('RABBITMQ_NAME'), port=os.environ.get("MQ_PORT")))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

        self.channel.basic_consume(queue=self.queue,
                                   auto_ack=True,
                                   on_message_callback=callback)

        self.channel.start_consuming()