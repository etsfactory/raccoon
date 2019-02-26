Ejemplos
========

Sección dedicada a mostrar ejemplos de uso de la librería

**Manejo de excepción, enviando un mensaje al bus**

.. code-block:: python

    from datetime import datetime

    import ..settings as st


    def process_exception(exception, request=None):
        # Creamos el JSON con el mensaje a escribir en el bus, en la cola de error
        msg = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "app_name": __name__.split('.')[0],
            "message": str(exception),
            "type": type(exception).__name__,
        }

        if request:
            msg["request"] = request.url
            if request.data:
                msg["tag"] = request.json

        with Publisher(st.BUS_HOST, st.BUS_USER, st.BUS_PASSWORD, st.EXCHANGE_ERROR, source_app=st.APP_NAME) as bus:
            bus.publish_msg(msg)


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

