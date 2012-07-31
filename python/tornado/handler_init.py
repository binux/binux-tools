# -*- encoding: utf8 -*-

handlers = []
ui_modules = {}
ui_methods = {}
modules = []

for module in modules:
    module = __import__("handlers."+module, fromlist=["handlers"])
    handlers.extend(module.handlers)
    ui_modules.update(module.ui_modules)
    ui_methods.update(module.ui_methods)
