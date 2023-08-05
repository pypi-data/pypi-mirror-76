# -*- coding: utf-8 -*-

from collections import namedtuple

from ifconf.config import Config
from ifconf.common import ConfigBuilder

class ConfigLoader(ConfigBuilder):
    
    @classmethod
    def load(cls, callback_method, config):
        assert callback_method is not None, 'callback_method cannot be null.'
        assert hasattr(callback_method, '__MODULE_NAME__'), 'MODULE_NAME must be set for callback_method.'
        assert hasattr(callback_method, '__SECTION__'), 'SECTION must be set for callback_method.'
        loader = ConfigLoader(callback_method.__SECTION__, callback_method.__MODULE_NAME__, config)
        callback_method(loader)
        return loader

    def __init__(self, section, module_name, config):
        assert section is not None, 'section cannot be null.'
        assert module_name is not None, 'module_name cannot be null.'
        assert config is not None, 'config cannot be null.'
        assert type(config) is Config, 'invalid config type:[{}]'.format(type(config))
        self.section = section
        self.module_name = module_name
        self.main_config = config
        self.names = []
        self.values = []

    def append_name_values(self, loader):
        assert loader is not None, 'configloader ancestor cannot be null.'
        for name, value in zip(loader.names, loader.values):
            while name in self.names:
                name = name + '_'
            self.names.append(name)
            self.vlaues.append(vlaue)
        return self

    def prepend_name_value_dict(self, override_dict):
        if override_dict:
            if not isinstance(override_dict, dict):
                raise ValueError('override_dict was expected an instance of dict but was [{}]'.format(type(override_dict)))
            for key, value in override_dict.items():
                name = key
                while name in self.names:
                    name = name + '_'
                if name != key:
                    index = self.names.index(key)
                    self.names.pop(index)
                    self.names.append(name)
                    self.values.append(self.values.pop(index))
                def get_value(conf):
                    return value
                self.names.append(key)
                self.values.append(get_value)
        return self

    def configure(self, immutable):
        assert self.main_config is not None, 'main_config cannot be null.'
        classname = self.section.replace('.','_')
        ntp = namedtuple(classname, self.names) if immutable else self.load_mutble_namedtuple(classname, self.names)
        args = [f(self.main_config) for f in self.values]
        conf = ntp(*args)
        self.main_config.logger.debug(conf)
        return conf

    def load_mutble_namedtuple(self, classname, names):
        from recordclass import recordclass
        return recordclass(classname, names)
        
    def add_attr(self, name, default=None, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr(self.section, name, default, required))

    def add_attr_boolean(self, name, default=False, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_boolean(self.section, name, default, required))

    def add_attr_int(self, name, default=0, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_int(self.section, name, default, required))

    def add_attr_float(self, name, default=0.0, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_float(self.section, name, default, required))

    def add_attr_dict(self, name, default={}, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_dict(self.section, name, default, required))
        
    def add_attr_list(self, name, default=[], required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_list(self.section, name, default, required))
        
    def add_attr_path(self, name, default=None, required=False, hidden=False, help=''):
        self.names.append(name)
        self.values.append(lambda conf: conf.get_attr_path(self.section, name, default, required))

