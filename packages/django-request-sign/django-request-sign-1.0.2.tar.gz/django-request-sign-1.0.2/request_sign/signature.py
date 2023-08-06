"""
@author: liyao
@contact: liyao2598330@126.com
@time: 2020/8/14 4:39 下午
"""

import hashlib
from datetime import datetime

from request_sign.utils import try_safe_eval
from request_sign.settings import SIGNATURE_SECRET, SIGNATURE_ALLOW_TIME_ERROR


def signature_request(parameters):
    # 列表生成式，生成key=value格式
    parameters_list = ["".join(i) for i in parameters.items() if i[1] and i[0] != "sign"]
    # 参数名ASCII码从小到大排序
    sort_parameters = "".join(sorted(parameters_list))
    # 在strA后面拼接上SIGNATURE_SECRET得到signature_str字符串
    signature_str = sort_parameters + SIGNATURE_SECRET
    # MD5加密
    m = hashlib.md5()
    m.update(signature_str.lower().encode('UTF-8'))

    return m.hexdigest()


def check_signature(request):
    timestamp = request.META.get("HTTP_TIMESTAMP")
    nonce = request.META.get("HTTP_NONCE")
    sign = request.META.get("HTTP_SIGN")

    if not all([timestamp, nonce, sign]):
        return False

    try:
        timestamp = float(timestamp)
    except:
        raise ValueError('timestamp must be int or float')

    now_timestamp = datetime.now().timestamp()
    if (now_timestamp-SIGNATURE_ALLOW_TIME_ERROR) > timestamp or timestamp > (now_timestamp+SIGNATURE_ALLOW_TIME_ERROR):
        return False

    parameters = {
        'nonce': nonce
    }
    get_parameters = request.GET.urlencode()
    post_parameters = request.POST.urlencode()
    body_parameters = str(request.body, encoding='utf-8')
    for parameter in ("&".join([get_parameters, post_parameters, body_parameters])).split('&'):
        if parameter:
            parameter = try_safe_eval(parameter)
            if isinstance(parameter, dict):
                parameters = dict(parameters, **parameter)
            else:
                if len(str(parameter).split('=')) == 2:
                    key, value = str(parameter).split('=')
                    if key not in parameters:
                        parameters[key] = value
    return sign == signature_request(parameters)
