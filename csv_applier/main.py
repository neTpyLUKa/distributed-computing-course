import os

from handler import handle_message
from rmq import MessageQueueClass

queue = MessageQueueClass(queue=os.environ.get('QUEUE_CSV'))

queue.consuming_loop(handle_message)
