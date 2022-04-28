from . import engine_uniffi

ApiError = engine_uniffi.ApiError.Other
ApiError.__module__ = __name__
ApiError.__name__ = "ApiError"
ApiError.__doc__ = """
通用错误

:param int code: 错误码，由 SDK 定义
:param str message: 错误描述
"""

RequestError = engine_uniffi.ApiError.Request
RequestError.__module__ = __name__
RequestError.__name__ = "RequestError"
RequestError.__doc__ = """
客户端请求失败

:param int code: 错误码，由 SDK 定义
:param str message: 错误描述
"""


HttpError = engine_uniffi.ApiError.Http
HttpError.__module__ = __name__
HttpError.__name__ = "HttpError"
HttpError.__doc__ = """
服务端处理失败

:param int status: 响应状态码
:param int code: 返回的错误码，由服务端定义
:param dict headers: 返回的响应头
:param str message: 错误描述
:param str detail: 错误详细原因
:param str trace_id: 当前请求 ID
"""

__all__ = ["ApiError", "HttpError", "RequestError"]
