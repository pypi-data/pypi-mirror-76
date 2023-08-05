# -*- coding: utf-8 -*-

import argparse
import logging

from .common import config_callback
from .config import Config
from .loader import ConfigLoader
from .loggingconf import configure_logging
from .printconf import PrintConfigAction


__MAIN_CONFIG__ = None

def get_main_config():
    if __MAIN_CONFIG__ is None:
        raise RuntimeError('Main configuration must be done before calling configure_module.')
    return __MAIN_CONFIG__

def clear_main_cofig():
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = None


def configure_main(argparser = None
                   , with_default_args = True
                   , config_arg = 'config.ini'
                   , config_path = []
                   , with_config_logging = True
                   , callback_methods = []):
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = Config(argparser)

    callback_methods = callback_methods if hasattr(callback_methods, '__iter__') else [callback_methods]
    callback_methods = [config_callback()(m) for m in callback_methods]
    
    if with_default_args:
        add_default_argument(__MAIN_CONFIG__.argparser, config_arg)
        PrintConfigAction.set_callback_methods(callback_methods)
        
    __MAIN_CONFIG__.parse(config_path)
    
    if with_config_logging:
        configure_logging(__MAIN_CONFIG__)
    else:
        __MAIN_CONFIG__.logger = logging.getLogger()
        
    for m in callback_methods:
        loader = ConfigLoader.load(m, __MAIN_CONFIG__)
        try:
            loader.configure(True)
        except Exception as e:
            __MAIN_CONFIG__.err.append('モジュール[{}]の設定取得に失敗しました。エラー：{}'.format(loader.section, e))
    for e in __MAIN_CONFIG__.err:
        __MAIN_CONFIG__.logger.warning(e)
    __MAIN_CONFIG__.logger.info('設定が完了しました。設定ファイル：{}'.format(__MAIN_CONFIG__.config_path))
    return __MAIN_CONFIG__

def configure_main_custom(argparser = None):
    global __MAIN_CONFIG__
    __MAIN_CONFIG__ = Config(argparser)
    return __MAIN_CONFIG__

def add_default_argument(argparser, config_path = None):
    if config_path is not None:
        argparser.add_argument('-c', '--config'
                               , metavar='PATH'
                               , default=config_path
                               , help='設定ファイルへのパス')
    argparser.add_argument('--verbose', '-v'
                           , action='count'
                           , default=False
                           , help='詳細なデータを出力')
    argparser.add_argument('--current_dir'
                           , default='.'
                           , help='カレントディレクトリを指定して実行')
    argparser.add_argument('--debug'
                           , action="store_true"
                           , default=False
                           , help='デバグモードで実行')
    argparser.add_argument('--debug_file'
                           , metavar='FILE'
                           , help='デバグモードで実行しファイル出力')
    argparser.add_argument('--print_conf'
                           , action=PrintConfigAction
                           , default=False
                           , help='設定ファイルの内容を出力')
    return argparser

    

