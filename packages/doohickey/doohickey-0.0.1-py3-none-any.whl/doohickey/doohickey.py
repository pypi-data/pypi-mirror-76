import logging
from .utils.exceptions import IncorrectParameters
__LOGGER__ = logging.getLogger(__name__)



class doohickey(object):
    
    __class_method = None

    def __init__(self):
        pass

    def __private_method(self):
        pass

    def _hidden_method(self):
        pass

    def method(self):
        pass

    @property
    def prop(self):
        return self.__prop
        
    @prop.setter
    def prop(self, value):
        self.__prop = value