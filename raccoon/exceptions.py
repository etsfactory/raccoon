class ConnectionErrorException(Exception):
    pass


class RoutingErrorException(Exception):
    def __init__(self, mt_name):
        super().__init__(self)
        self.mt_name = mt_name


class TransientException(Exception):
    pass


class PartialyProcessedException(Exception):
    def __init__(self, failed_messages):
        super().__init__(self, "Some messages faile while processing: {}".format(failed_messages))
        self.failed_messages = failed_messages
