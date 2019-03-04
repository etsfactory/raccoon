Changelog
=========

1.5.1 (2019-02-08)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Actualiza la versión del paquete. [Javier Rodríguez Valiñas]
- ENH: Se añade siempre a la dle. [Javier Rodríguez Valiñas]
- ENH: Se confirma utilizando la var delivery_tags. [Javier Rodríguez
  Valiñas]

Bugs
~~~~
- BUG: Subido cambio que no era necesario. [Javier Rodríguez Valiñas]
- BUG: Typo en un mensaje de log. [Javier Rodríguez Valiñas]
- BUG: Error al notificar el reintento de las transientException.
  [Javier Rodríguez Valiñas]
- BUG: Se elimina de la lista los rechazados. [Javier Rodríguez Valiñas]
- BUG: se estaba iterando mal. [Javier Rodríguez Valiñas]
- BUG: Se elimina el tag de la lista. [Javier Rodríguez Valiñas]
- BUG: Error en la palabra delivery. [Javier Rodríguez Valiñas]
- BUG: Permite seleccionar los mensajes fallidos. [Javier Rodríguez
  Valiñas]

Limpieza de Código
~~~~~~~~~~~~~~~~~~
- CLN: Utiliza un nombre de funcion mas apropiado para el evio de
  errores. [Javier Rodríguez Valiñas]


1.5.0 (2019-01-23)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Incrementa la versión de raccoon. [Javier Rodríguez Valiñas]

Bugs
~~~~
- BUG: El Exchange dle a tipo direct. [Javier Rodríguez Valiñas]

  El Exchange dle utiliza el routing key para seleccionar a que
  cola dle enviar el mensaje, con lo que es necesario configurarlo
  en modo direct ya que en otro caso se ignora


1.4.0 (2019-01-11)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Se actualiza la nueva versión de la librería en el setup.py.
  [Nelson Saturno]
- ENH: Se reencola un mensaje que ha fallado por un TransientException
  sólo una vez. [Nelson Saturno]
- ENH: Se capturan excepciones puntuales al procesar mensajes del Bus.
  [Nelson Saturno]


1.3.1 (2019-01-09)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: en caso de error durante una llamada rpc se devuelve la excepción
  generada por el servicio consumidor. [amaqueda]

Other
~~~~~
- Se añade en el metadata del mensaje el exchange y la key. [Diego
  López]
- Nuevo método para hacer unbind de una cola a un exchange. [Diego
  López]
- Refactorización de la manera de conseguir las variables del
  diccionario. [Diego López]
- Añadido una manera de configurar la durabilidad de cada exchange.
  [Diego López]
- Refactorización de la manera en la que se declara el tipo de exchange
  - Faltaba por añadir que asegurar que la cola de la que lee existe.
  [Diego López]
- Añadido el filtro del bus con tipo de exchange también. [Diego López]
- Se vuelve a añadir el bucle while para que no se llene el stack.
  [Diego López]

  Con el bucle for, si hay muchas llamadas se puede llenar el stack
- Añadido reconexión al bus si salta excepción pero sin bucle while.
  [Diego López]
- Autenticación en el bus obligatoria, como antes. [Diego López]
- Añadido los parámetros en la función de procesado al recibir mensajes.
  [Diego López]
- Inicialización de los mensajes a procesar. [Diego López]
- Añadido otra vez el heartbeat - Añadida comprobación antes de procesar
  el mensaje, de que el canal y el mensaje existe. [Diego López]
- Ahora se puede leer de una lista de varios exchanges con keys. [Diego
  López]

  - Se puede pasar como partámetro al Consumer una lista de varios exchanges con varias keys para leer
  de todas a la vez. También se puede pasar un solo exchange con una key.
  - Si no se pasa usuario y contraseña se crea una conexión al bus sin credenciales.
  - Se comprueba si los exchanges que llegan son una lista y se hace un for bindeando cada exchange y key de la lista
  con la cola para leer.
  - En lugar de usar basic_consume se hace un for leyendo con la función consume(), ésto se hace para no tener
  que usar un while exterior más el propio bucle de leer mensajes con basic_consume() ahorrando recursos
  y teniendo un control de lo que ocurre al leer cada mensaje pudiendo parar la escucha saliendo del bucle.


1.2.11 (2018-10-25)
-------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Se añade el RPCPublisher. [jarrizabalaga]
- ENH: Se añade el RPCPublisher a Raccoon. [jarrizabalaga]


1.2.10 (2018-07-10)
-------------------

Bugs
~~~~
- BUG: El atributo properties.headers puede ser vacio. [Javier Rodríguez
  Valiñas]


1.2.9 (2018-07-10)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Se añade un campo metadata con información del mensaje. [Javier
  Rodríguez Valiñas]

  Por defecto guarda la fecha de creación del mensaje y
  añade tambien la aplicación que genera el mensaje

Build
~~~~~
- BLD: Incrementa la version de raccoon. [Javier Rodríguez Valiñas]


1.2.8 (2018-07-10)
------------------

Nueva Funcionalidad
~~~~~~~~~~~~~~~~~~~
- ENH: Añade al mensaje recibido de rabbit información de si es
  federado. [Javier Rodríguez Valiñas]

  Añade en el campo metadata la clave 'IsFederated' a True para mensajes
  que provengan de una federación.
- ENH: Marca los mensajes que provengan de una federacion. [Javier
  Rodríguez Valiñas]

  Se añade un campo 'IsFederated' a los mensajes que tengan el origen
  en otra cola de rabbit y que fueran transmitidos a tavés de una
  federación

Build
~~~~~
- BLD: Actualiza la version de raccoon. [Javier Rodríguez Valiñas]


1.2.7 (2018-06-28)
------------------
- Se actualiza la versión de pika a la 0.12.0. [jarrizabalaga]


1.2.6 (2018-06-05)
------------------
- Se aumenta el número de versión. [jarrizabalaga]
- Se captura la excepción de conexión cerrada. [jarrizabalaga]
- Se elimina el proceso que duerme a la conexión. [jarrizabalaga]
- Prueba 3. [jarrizabalaga]
- Prueba. [jarrizabalaga]
- Prueba. [jarrizabalaga]
- Prueba reconexión. [jarrizabalaga]


1.2.5 (2018-06-04)
------------------
- Se añade el parámetro "heartbeat" al consumidor. [jarrizabalaga]


1.2.4 (2018-05-31)
------------------
- Se actualiza la última versión de pika para disponer de funcionalidad
  de control de timeout de BlockingConnections. [schacon]
- Se actualiza la última versión de pika para disponer de funcionalidad
  de control de timeout de BlockingConnections. [schacon]
- Se añade un parámetro que define el numero de reintentos de conexión
  al bus antes de notificar el error. [schacon]


1.2.3 (2018-04-18)
------------------
- Se repetía la función en el consumidor. [jarrizabalaga]
- Corregido un bug al intentar escribir en el log. [jarrizabalaga]
- Modificado el número de versión. [jarrizabalaga]
- Se añade funcionalidad al consumidor para poder usarse como RPC.
  [jarrizabalaga]


1.2.2 (2018-04-17)
------------------
- Se deja de utilizar pip.req para resolver las dependencias en el
  setup.py porque da problemas en las versiones más actuales de pip.
  [schacon]


1.2.1 (2018-04-06)
------------------
- Deshace cambios que no son necesarios. [Javier Rodríguez Valiñas]
- Prueba sin cerrar la conexion, solo el canal. [Javier Rodríguez
  Valiñas]
- Cierra el canal. [Javier Rodríguez Valiñas]
- Error al comprobar el estado. [Javier Rodríguez Valiñas]
- Añade un metodo de stop, que para el consumidor. [Javier Rodríguez
  Valiñas]


1.1.0 (2018-03-02)
------------------
- Se añade el parámetro x-dead-letter-routing-key a la cola si está
  definida la routing key de la cola DLE. [David Martín]
- Se añade la posibilidad de definir una routing_key para la cola DLE.
  [David Martín]


1.0.0 (2018-02-09)
------------------
- Error al declarar el exchange. [Alberto Maqueda]
- Se adapta a los cambios de la última versión de pika. [Alberto
  Maqueda]
- Primera versión de la librería, incluye un método consumidor y otro
  publicador. [Alberto Maqueda]
- Se añade readme. [Alberto Maqueda]


