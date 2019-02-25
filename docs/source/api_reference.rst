API Reference
=============

Esta sección presenta un resumen de todos los objetos de ``raccoon`` que sirven tanto para realizar las publicaciones y
procesado de datos en las colas del bus, como para el manejo de excepciones.


Publisher
---------
Módulo que implementa las clases públicas: ``Publisher`` y ``RpcPublisher``, encargadas de publicar los mensajes en las
colas del bus. Para ello, las dos clases contienen los métodos ``publish_msg()`` y ``rpc_call()`` respectivamente.

.. automodule:: raccoon.publisher
    :members:


Consumer
--------
Wrapper personalizado que procesa los datos recibidos de una cola del bus. El objeto consumidor se ejecuta en un hilo
independiente.

.. automodule:: raccoon.consumer
    :members:

Exceptions
----------
Módulo encargado del tratamiento personalizado de excepciones.

.. autoclass:: raccoon.exceptions.ConnectionErrorException
    :members:

.. autoclass:: raccoon.exceptions.RoutingErrorException
    :members:

.. autoclass:: raccoon.exceptions.TransientException
    :members:
