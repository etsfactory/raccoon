from .consumer import Consumer
from .publisher import Publisher, RpcPublisher
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
