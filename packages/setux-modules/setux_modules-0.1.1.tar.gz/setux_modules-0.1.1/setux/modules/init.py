__version__ = '0.1.1'

from logging import getLogger

logger = getLogger('setux')
debug = logger.debug
info = logger.info
error = logger.error
exception = logger.exception


from setux.core.module import Module
