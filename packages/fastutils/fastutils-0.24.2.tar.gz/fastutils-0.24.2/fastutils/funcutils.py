# -*- coding: utf-8 -*-
from inspect import signature
from . import typingutils
import bizerror


def get_default_values(func):
    data = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default != parameter.empty:
            data[name] = parameter.default
    return data

def get_inject_params(func, data):
    params = {}
    parameters = signature(func).parameters
    for name, parameter in parameters.items():
        if parameter.default is parameter.empty: # no default value, this parameter is required
            if not name in data:
                raise bizerror.MissingParameter("Missing required parameter: {0}".format(name))
            value = data[name]
        else:
            value = data.get(name, parameter.default)
        if not parameter.annotation is parameter.empty:
            value = typingutils.smart_cast(parameter.annotation, value)
        params[name] = value
    return params


def call_with_inject(func, data):
    params = get_inject_params(func, data)
    return func(**params)


class classproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()


class chain(object):
    def __init__(self, *args):
        self.funcs = args
    
    def __call__(self, init_result, extra_args=None, extra_kwargs=None):
        extra_args = extra_args or []
        extra_kwargs = extra_kwargs or {}
        result = init_result
        for func in self.funcs:
            result = func(result, *extra_args, **extra_kwargs)
        return result
