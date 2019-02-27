.. raccoon documentation master file, created by
   sphinx-quickstart on Mon Feb 11 12:37:13 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Bienvenido a la documentación de Raccoon!
=========================================

============
Introducción
============

``Raccoon`` es una librería que implementa un wrapper sobre `Pika <https://pika.readthedocs.io/en/stable/>`_, librería
python que gestiona la conexión al bus a través de un sistema de colas `RabbitMQ <https://www.rabbitmq.com/>`_,
añadiendo robustez además de mejorar el tratamiento de excepciones.

Gracias a ``raccoon`` puedes publicar y recibir mensajes de una manera sencilla, segura y trasparente. Es fundamental
para la gestión de errores en el sistema.

``Raccoon`` te permite publicar los mensajes de dos maneras:

- **Asíncronamente**, con el metodo ``Publisher.publish_msg()``. Es la forma habitual de utilizar la librería, el mensaje se envía a la cola del bus sin necesidad de esperar una respuesta.

- **Síncronamente**, con el metodo ``RpcPublisher.rpc_call()``. El mensaje se lanza esperando una respuesta, en caso de no recibirla, se lanza una excepción.


Los módulos más importantes que componen ``raccoon`` son:

- ``publisher.py``, wrapper que gestiona las publicaciones de mensajes sobre el bus
- ``consumer.py``, wrapper que procesa los datos recibidos de una cola del bus
- ``exceptions.py`` tratamiento personalizado de excepciones


Tabla de Contenidos
================

.. toctree::
   :maxdepth: 2

   instalation
   first_steps
   api_reference
   examples
