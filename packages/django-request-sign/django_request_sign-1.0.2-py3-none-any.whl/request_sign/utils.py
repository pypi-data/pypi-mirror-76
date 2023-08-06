"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/16 4:52 下午
"""

import time
import datetime

from django.http import HttpResponse


def try_safe_eval(value):
    value = str(value)
    if all([value]):
        if value.startswith('[') and value.endswith(']') or \
                value.startswith('{') and value.endswith('}'):
            value = eval(value, {'datetime': datetime, 'time': time})

        elif value.lower() in ['true', 'false']:
            return {
                'true': True,
                'false': False,
            }.get(value.lower())
    else:
        raise ValueError('value can not be null')

    return value


def default_response():
    """
        Must return django HttpResponse type
    :return: HttpResponse
    """
    return HttpResponse()
