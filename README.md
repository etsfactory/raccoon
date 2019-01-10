# Raccoon

Racoon es una librería que implementa un wrapper sobre pika (gestiona la conexión a un bus rabbitMQ).

Racoon permite la creación de threads para leer mensajes de varios exchanges con varias keys a la vez. Además 
permite la reconexión al bus automáticamente y tras varios intentos.

## Getting started

Para empezar a usar esta librería puedes descargarla mediante el comando de python:

```bash
pip install git+git://github.com/etsfactory/raccoon.git
```

Para usar la librería en tu proyecto puedes importar las dos clases que ofrece:

```python
from raccoon import Consumer
from raccoon import Publisher
```

La clase consumer sirve para leer del bus y acepta los siguientes parámetros:

- **process_function** : Funcion que procesara los datos recibidos. En esta función recibirás los datos procesados
- **host** : Direccion del rabbit
- **user** : Usuario para conectar con rabbit
- **password** : Contraseña de rabbit
- **exchange** : Nombre del exchange al que conectar la cola
- **rabbit_queue_name** : Nombre de la cola
- **error_queue** : Cola para escribir los mensajes de error
- **prefetch_count** : Número de mensajes a leer de rabbit
- **exchange_type** : Typo de exchange a definir
- **retry_wait_time** : Segundos de espera para el siguiente reintento de conexión con rabbit
- **routing_key** : Clave de la que escuchar
- **dle** : Nombre del exchange al que enviar los mensajes en caso de error
- **dle_queue** : Nombre de la cola conectada al exchange de dle
- **dle_routing_key** : Clave de enrutado para la cola dle
- **reply_origin** : If True, sends de result to the original queue using the reply_to prop of the request
- **retries_to_error** : Número de reintentos de conexión con rabbit antes de notificar el error
- **heartbeat** : tiempo con el que se comprueba si está viva la conexión

