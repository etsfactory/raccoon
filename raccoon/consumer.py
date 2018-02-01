import threading
import time
import traceback
import ujson

import pika
from pika.exceptions import ConnectionClosed

from raccoon.exceptions import ConnectionErrorException


class Consumer(threading.Thread):
    """
    Procesa los datos de una cola del bus.
    Permite la opción de procesarlos en bloques utilizando el argumento "prefetch_count".
    Los datos pasados a la función definida en el argumento "process_function" dependen del valor de "prefetch_count":
      - prefetch_count==1, la función definida recibe el mensaje de la cola parseado.
      - En otro caso, la función definida recibe una lista con (prefetch_count // 2) mensajes de la cola parseados.
    La funcion que se para por process_function tiene que ser capaz de manejar el tipo de dato correspondiente
     (lista/mensaje que va a depender del valor de prefect_count).
    """

    def process_data_in_baches(self):
        return self.prefetch_count != 1

    def data_ready(self):
        """
        Comprueba que tenemos listo toda los datos que queremos procesar
        :return: Si el bloque de datos esta listo para ser procesado.
        """
        return (not self.process_data_in_baches()
                or self.is_queue_empty()
                or len(self.messages) >= self.batch_processing_size)

    def process_bus_data(self, ch, method, properties, body):
        """
        Obtiene el objeto del bus y lo procesa.
        En caso de que la clase defina el atributo "prefetch_count", los mensajes se procesaran el bloque.
        En caso de error, pone un mensaje en la cola de errores.
        """

        try:
            data = ujson.loads(body)
            if self.data_ready():
                if self.process_data_in_baches():
                    data_to_process = self.messages + [data]
                else:
                    data_to_process = data
                self.messages = []
                self.process_function(data_to_process)

            else:
                # Se almacena el mensaje para su posterior procesado
                self.messages.append(data)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except ConnectionErrorException as e:
            try:
                ch.basic_nack(delivery_tag=method.delivery_tag)
            except ConnectionClosed:
                raise ConnectionErrorException('NACK not delivered.')
            raise e
        except Exception as e:
            exception = {
                'error': e,
                'trace': traceback.format_exc()
            }

            if body:
                exception.update({'body': body})
            self.error_queue.put(exception)

            if self.dle:
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            else:
                # Se ignora el mensaje y se elimina de la cola
                ch.basic_ack(delivery_tag=method.delivery_tag)

    def is_queue_empty(self):
        res = self.ch.queue_declare(queue=self.rabbit_queue_name,
                                    durable=True, exclusive=False,
                                    auto_delete=False, passive=True)
        return res.method.message_count == 0

    def __init__(self, process_function, host, user, password, exchange, rabbit_queue_name, error_queue,
                 prefetch_count=1, exchange_type='fanout', retry_wait_time=1, routing_key=None, dle=None, dle_queue=None):
        """
        :param process_function: Funcion que procesara los datos recibidos
        :param host: Direccion del rabbit
        :param user : Usuario para conectar con rabbit
        :param password: Contraseña de rabbit
        :param exchange: Nombre del exchange al que conectar la cola
        :param rabbit_queue_name: Nombre de la cola
        :param error_queue: Cola para escribir los mensajes de error
        :param prefetch_count: Número de mensajes a leer de rabbit
        :param exchange_type: Typo de exchange a definir
        :param retry_wait_time: Número de reintentos de conexión con rabbit
        :param routing_key: Clave de la que escuchar
        :param dle: Nombre del exchange al que enviar los mensajes en caso de error
        :param dle_queue: Nombre de la cola conectada al exchange de dle
        """
        super().__init__()

        self.process_function = process_function
        self.host = host
        self.user = user
        self.password = password
        self.exchange = exchange
        self.rabbit_queue_name = rabbit_queue_name
        self.error_queue = error_queue
        self.prefetch_count = prefetch_count
        self.exchange_type = exchange_type
        self.retry_wait_time = retry_wait_time
        self.routing_key = routing_key
        self.dle = dle
        self.dle_queue = dle_queue

        self.count = 0
        self.number_of_messages = 0
        self.messages = []


        # Se procesa la mitad de los objetos obtenidos si prefetch_count es distinto de 1
        self.batch_processing_size = 1 if prefetch_count == 1 else (prefetch_count // 2)

    def run(self):
        retries = 0
        while True:
            try:
                credentials = pika.PlainCredentials(self.user, self.password)
                connection = pika.BlockingConnection(pika.ConnectionParameters(self.host, credentials=credentials))
                channel = connection.channel()

                queue_args = None
                if self.dle:
                    # Declara el Dead letter exchange
                    channel.exchange_declare(exchange=self.dle, durable=True, type=self.exchange_type)
                    result = channel.queue_declare(queue=self.dle_queue, durable=True, arguments=queue_args)
                    tmp_queue_name = result.method.queue
                    channel.queue_bind(exchange=self.dle, queue=tmp_queue_name, routing_key=self.routing_key)
                    queue_args = {'x-dead-letter-exchange': self.dle}

                channel.exchange_declare(exchange=self.exchange, durable=True, exchange_type=self.exchange_type)
                self.ch = channel

                result = channel.queue_declare(queue=self.rabbit_queue_name, durable=True, arguments=queue_args)
                queue_name = result.method.queue


                channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.routing_key)

                # Definiendo callback
                channel.basic_qos(prefetch_count=self.prefetch_count)
                channel.basic_consume(self.process_bus_data, queue=self.rabbit_queue_name)

                retries = 0
                channel.start_consuming()
            except (ConnectionClosed, ConnectionErrorException) as e:
                # Solo publica el primer error de conexion
                if retries == 0:
                    exception = {
                        'error': e,
                        'trace': traceback.format_exc()
                    }
                    self.error_queue.put(exception)
                try:
                    channel.close()
                except Exception:
                    pass
            except Exception as e:
                exception = {
                    'error': e,
                    'trace': traceback.format_exc()
                }
                self.error_queue.put(exception)
            finally:
                retries += 1
                time.sleep(self.retry_wait_time)