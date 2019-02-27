class ConnectionErrorException(Exception):
    """Captura excepciones por error de conexión."""
    pass


class RoutingErrorException(Exception):
    """Captura excepciones cuando hay un error con el `routing key` al enviar un mensaje."""

    def __init__(self, mt_name):
        super().__init__()
        self.mt_name = mt_name


class TransientException(Exception):
    """Captura excepciones que podrían ser puntuales y resolverse reintentando."""
    pass


class PartialyProcessedException(Exception):
    """Excepción generada cuando algunos de los mensajes han fallado al ser procesados."""

    def __init__(self, failed_messages):
        super().__init__(self, "Some messages failed while processing: {}".format(failed_messages))
        self.failed_messages = failed_messages
