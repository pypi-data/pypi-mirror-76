__version__ = '0.1.0'


from logging import getLogger

logger = getLogger('setux')
debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception
