from datetime import datetime
import time

import ujson

import pika
from pika.exceptions import ConnectionClosed


class Publisher(object):

    def __init__(self, host, user, password, exchange, exchange_type='fanout', retry_wait_time=1, max_retries=1,
                 source_app=None):
        self.host = host
        self.user = user
        self.password = password
        self.exchange = exchange
        self.max_retries = max_retries
        self.retry_wait_time = retry_wait_time
        self.exchange_type = exchange_type
        self.source_app = source_app

    def __enter__(self):
        tries = 0
        finished = False
        while not finished:
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                connection_out = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))
                finished = True
            except ConnectionClosed as e:
                print('Tries: %s, maxTries: %s' % (tries, self.max_retries))
                if tries > self.max_retries:
                    raise e
                time.sleep(10)
                tries += 1
        self.channel = connection_out.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)
        return self

    def __exit__(self, type, value, traceback):

        self.channel.close()

    def publish_msg(self, message, mandatory=False, routing_key=''):
        tries = 0
        finished = False
        if mandatory:
            self.channel.confirm_delivery()
        # Añade metadatos al mensaje
        metadata = {'CreationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        if self.source_app is not None:
            metadata['AppName'] = self.source_app
        message['metadata'] = metadata
        while not finished:
            try:
                return self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key,
                                                  body=ujson.dumps(message),
                                                  properties=pika.BasicProperties(delivery_mode=2),
                                                  mandatory=mandatory)
            except ConnectionClosed as e:
                if tries > self.max_retries:
                    raise e
                time.sleep(self.retry_wait_time)
                tries += 1
