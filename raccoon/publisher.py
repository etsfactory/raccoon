from datetime import datetime
import time
import uuid

import ujson
import pika
from pika.exceptions import ConnectionClosed


class Publisher(object):
    """Clase encargada de publicar los mensajes de forma asíncrona"""

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
        connection_out = None
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
        """
        Método público encargado de enviar  el mensaje

        :param message: mensaje a enviar
        :param mandatory: activa el modo de confirmación ACK en RabbitMQ
        :param routing_key: la ruta a vincular
        :return: True si la confirmación no está activada. Si está activada True si el mensaje fue entregado, si no False
        """
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


class RpcPublisher(object):
    """Clase encargada de publicar los mensajes de forma síncrona"""

    def __init__(self, host, user, password, exchange, exchange_type='fanout', retry_wait_time=1, max_retries=1,
                 time_limit=300, source_app=None):

        self.host = host
        self.user = user
        self.password = password
        self.exchange = exchange
        self.max_retries = max_retries
        self.retry_wait_time = retry_wait_time
        self.exchange_type = exchange_type
        self.source_app = source_app
        self.time_limit = time_limit
        self.response = None
        self.corr_id = None

    def _on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = ujson.loads(body)

    def __enter__(self):
        tries = 0
        finished = False
        connection_out = None
        while not finished:
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                connection_out = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))
                self.connection = connection_out
                finished = True
            except ConnectionClosed as e:
                print('Tries: %s, maxTries: %s' % (tries, self.max_retries))
                if tries > self.max_retries:
                    raise e
                time.sleep(10)
                tries += 1

        self.channel = connection_out.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type, durable=True)

        # Configure a queue for a response
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self._on_response, no_ack=True, queue=self.callback_queue)
        return self

    def __exit__(self, type, value, traceback):
        self.channel.close()

    def rpc_call(self, message, mandatory=False, routing_key=''):
        """
        Método público encargado de enviar  el mensaje

        :param message: mensaje a enviar
        :param mandatory: activa el modo de confirmación ACK en RabbitMQ
        :param routing_key: la ruta a vincular
        :return: JSON con la respuesta recibida despues de enviar el mensaje
        """
        tries = 0
        finished = False
        if mandatory:
            self.channel.confirm_delivery()
        # Añade metadatos al mensaje
        metadata = {'CreationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        if self.source_app is not None:
            metadata['AppName'] = self.source_app
        message['metadata'] = metadata

        self.corr_id = str(uuid.uuid4())
        props = pika.BasicProperties(delivery_mode=2, correlation_id=self.corr_id, reply_to=self.callback_queue)
        while not finished:
            try:
                self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key,
                                           body=ujson.dumps(message),
                                           properties=props,
                                           mandatory=mandatory)
                self.connection.process_data_events(time_limit=self.time_limit)
                if self.response is None:
                    raise Exception('No reply RPC consumer of queue {}.'.format(self.exchange))
                return self.response
            except ConnectionClosed as e:
                if tries > self.max_retries:
                    raise e
                time.sleep(self.retry_wait_time)
                tries += 1
