from django.conf import settings

__all__ = ['ENABLE_REQUEST_SIGNATURE', 'SIGNATURE_SECRET', 'SIGNATURE_ALLOW_TIME_ERROR', 'SIGNATURE_RESPONSE']

ENABLE_REQUEST_SIGNATURE = settings.ENABLE_REQUEST_SIGNATURE if \
    hasattr(settings, 'ENABLE_REQUEST_SIGNATURE') else False  # 开启签名校检

SIGNATURE_SECRET = settings.SIGNATURE_SECRET if \
    hasattr(settings, 'SIGNATURE_SECRET') else None  # 私钥

SIGNATURE_ALLOW_TIME_ERROR = settings.SIGNATURE_ALLOW_TIME_ERROR if \
    hasattr(settings, 'SIGNATURE_ALLOW_TIME_ERROR') else 600  # 允许时间误差

SIGNATURE_RESPONSE = settings.SIGNATURE_RESPONSE if \
    hasattr(settings, 'SIGNATURE_RESPONSE') else 'request_sign.utils.default_response'  # 签名不通过返回方法
