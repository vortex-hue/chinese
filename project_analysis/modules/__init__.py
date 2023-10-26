# -*- coding: utf-8 -*-
from importlib import import_module


def import_module_func(project_name, bind_module_name):
    import_path = f'{project_name}.module_register'
    registed_modules = import_module(import_path)
    if not getattr(registed_modules, 'REGIST_MODULES'):
        return False
    REGIST_MODULES = getattr(registed_modules, 'REGIST_MODULES')
    module_CLS = REGIST_MODULES.get(bind_module_name)
    return module_CLS

def import_module_name(project_name, module_name):
    import_path = f'{project_name}.module_name'
    registed_modules = import_module(import_path)
    if not getattr(registed_modules, module_name):
        return False
    MODULE_NAME = getattr(registed_modules, module_name)
    return MODULE_NAME

