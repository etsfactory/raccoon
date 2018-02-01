class ConnectionErrorException(Exception):
    pass


class RoutingErrorException(Exception):
    def __init__(self, mt_name):
        super().__init__()
        self.mt_name = mt_name
