Ejemplos
========

Sección dedicada a mostrar ejemplos de uso de la librería

**Manejo de excepciones no controladas en Flask, enviando un mensaje al bus**

.. code-block:: python

    import ujson
    import sys
    import traceback as tb

    from cancun.errors.exceptions import InternalServerErrorException
    from flask import Flask, Response, request

    import ..settings as st


    @app.errorhandler(Exception)
    def all_exception_handler(error):
        process_exception(error, request=request, exc_tb=tb.format_exc())
        exception = InternalServerErrorException()
        return Response(response=ujson.dumps(exception.to_dict()),
                        status=exception.status_code,
                        mimetype='application/json')


    def process_exception(exception, request=None, exc_tb=None):
        if exc_tb is None:
            exc_tb = tb.format_exc()

        log_exception(type(exception), exception, exc_tb, request)

        # Creamos el JSON con el mensaje a escribir en el bus, en la cola de error
        msg = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "app_name": __name__.split('.')[0],
            "server": socket.gethostname(),
            "message": str(exception),
            "stack": exc_tb,
            "type": type(exception).__name__,
        }

        if request:
            msg["request"] = request.url
            if request.data:
                msg["tag"] = request.json

        with Publisher(st.BUS_HOST, st.BUS_USER, st.BUS_PASSWORD, st.EXCHANGE_ERROR) as bus:
            bus.publish_msg(msg)


    def log_exception(exc_type, exc_value, exc_tb, request=None):

        try:

            if not isinstance(exc_tb, str):
                exc_tb = ''.join(tb.format_tb(exc_tb))

            msg = '\nRequest: ' + str(request)[14:-1] + '\n' if request is not None else '\n'

            msg += ERROR_FORMAT
            msg = msg.replace('{t}', exc_type.__name__)
            msg = msg.replace('{m}', str(exc_value))
            msg = msg.replace('{tb}', exc_tb)

            st.logger.error(msg)
        except:
            pass



**Clase consumidora**

.. code-block:: python

    import queue
    from raccoon import Consumer

    import settings as st


    class BusConnectionHandler():
        """
        Bus connection class
        """

        def start(self):
            """
            Starts the thread
            """
            error = queue.Queue()
            self.bus_thread = Consumer(
                self.on_message,
                st.RABBITMQ_SERVER,
                st.RABBITMQ_USER,
                st.RABBITMQ_PASSWORD,
                self.subscriptions,
                st.RABBITMQ_QUEUE,
                error)

            self.bus_thread.start()

        def stop(self):
            """
            Stops the thread
            """
            self.bus_thread.stop()
            self.bus_thread.join()

        def on_message(self, message):
            """"
            When a message is received
            """
            exchange = message.get('metadata').get('exchange')
            routing_key = message.get('metadata').get('routing_key', '')
            print(message)

