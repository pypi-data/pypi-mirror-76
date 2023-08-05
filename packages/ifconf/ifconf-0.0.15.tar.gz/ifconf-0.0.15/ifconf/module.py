# -*- coding: utf-8 -*-

from functools import reduce

from .common import config_callback
from .main import get_main_config
from .loader import ConfigLoader

def configure_module(*callback_methods, override = {}, immutable = True):
    config = get_main_config()
    loaders = [ConfigLoader.load(config_callback()(callback), config) for callback in callback_methods]
    loaders[0].prepend_name_value_dict(override)
    return reduce(lambda a,b: a.append_name_values(b), loaders).configure(immutable)

