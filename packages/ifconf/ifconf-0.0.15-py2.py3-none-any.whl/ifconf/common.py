# -*- coding: utf-8 -*-

import os
import sys
import abc

def get_module_name_for(obj):
    if obj.__module__  == '__main__':
        try:
            return os.path.splitext(os.path.basename(sys.modules['__main__'].__file__))[0]
        except:
            return os.path.splitext(os.path.basename(sys.executable))[0]
    else:
        return obj.__module__
    
def config_callback(section = None):
    def _decorator(func):
        if hasattr(func, '__SECTION__'):
            return func
        func.__MODULE_NAME__ = get_module_name_for(func)
        func.__SECTION__ = section if type(section) == str and section else '{}_{}'.format(func.__MODULE_NAME__, func.__name__)
        return func
    return _decorator(section) if callable(section) else _decorator


class ConfigBuilder(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_attr(self, name, default=None, required=False, hidden=False, help=''):
        pass

    @abc.abstractmethod
    def add_attr_boolean(self, name, default=False, required=False, hidden=False, help=''):
        pass

    @abc.abstractmethod
    def add_attr_int(self, name, default=0, required=False, hidden=False, help=''):
        pass

    @abc.abstractmethod
    def add_attr_float(self, name, default=0.0, required=False, hidden=False, help=''):
        pass

    @abc.abstractmethod
    def add_attr_dict(self, name, default={}, required=False, hidden=False, help=''):
        pass
        
    @abc.abstractmethod
    def add_attr_list(self, name, default=[], required=False, hidden=False, help=''):
        pass
        
    @abc.abstractmethod
    def add_attr_path(self, name, default=None, required=False, hidden=False, help=''):
        pass
    
