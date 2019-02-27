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
Wrapper personalizado que gestiona la conexión y comunicación con el bus, procesando los datos de un exchange. Para
ello, crea y conecta una cola en modo escucha al exchange, en caso de no estar ya creada.


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

.. autoclass:: raccoon.exceptions.PartialyProcessedException
    :members:
