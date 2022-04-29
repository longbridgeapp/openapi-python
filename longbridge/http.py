from dataclasses import asdict, dataclass, field
from hashlib import md5
from typing import Any, Dict, Optional

from . import __version__, engine_uniffi
from .engine_uniffi import ApiResponse, RequestOption


class Auth(engine_uniffi.Session):
    """
    认证凭证

    :param app_key: App Key
    :param app_secret: App Key 对应的密钥
    :param access_token: 用户凭证
    """

    def __init__(
        self, app_key: str, app_secret: str, access_token: Optional[str] = None
    ):
        super().__init__()
        self.app_key = app_key
        self.app_secret = app_secret
        self.token = access_token

    def id(self):
        hash = md5(self.app_key.encode("utf-8"))
        if self.token != None:
            hash.update(self.token.encode("utf-8"))
        return hash.hexdigest()

    def get(self, key):
        return getattr(self, key, None)

    def set(self, key, value):
        return setattr(self, key, value)

    def remove(self, key):
        return delattr(self, key)


@dataclass
class Config:
    """
    Http 配置信息

    :param base_url: Open API 服务地址
    :param language: Accept-Language header 对应的值
    :param headers: 所有请求携带的额外请求 Header
    """

    base_url: str = "https://openapi.lbkrs.com"
    env: engine_uniffi.Env = engine_uniffi.Env.PROD
    headers: dict = field(default_factory=dict)
    language: str = "zh-CN"


class OpenapiBinding(engine_uniffi.Binding):
    def skip_validation(self):
        return True

    def timestamp(self, path, timestamp):
        return ""

    def user_agent(self):
        return f"longport/openapi-py({__version__}) "


class HttpClient(engine_uniffi.HttpClient):
    """
    HTTP Client 实现
    """

    def __init__(self, auth: Auth, config: Config = Config()):
        """
        初始化 Http Client

        :param auth: 认证信息
        :param config: 请求配置
        """
        super().__init__(
            engine_uniffi.HttpClientConfig(**asdict(config), session_id=auth.id()),
            OpenapiBinding(),
            auth,
        )

    def set_header(self, key: str, value: str):
        """
        更新请求头

        如果 value 为空，则移除对应的 key
        """
        super().set_header(key, value)

    def set_language(self, language: str):
        """
        重置语言
        """
        super().set_language(language)

    def set_url(self, base_url: str):
        """
        重置 base_url
        """
        super().set_url(base_url, None)

    def get(
        self,
        path: str,
        query: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOption] = None,
    ) -> ApiResponse:
        """
        发起 GET 请求

        :param path: 请求的相对路径
        :param query: 请求额外的 parameter
        :param options: 请求额外的定制信息
        :return: 响应结果
        :rtype: ApiResponse
        :raises ApiError: 通用错误
        :raises RequestError: 本地发起请求失败
        :raises HttpError: 请求响应非 2xx
        """
        return super().get(path, query, options)

    def post(
        self,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOption] = None,
    ) -> ApiResponse:
        """
        发起 POST 请求

        :param path: 请求的相对路径
        :param payload: 请求体，将以 JSON 的方式发送给服务器
        :param options: 请求额外的定制信息
        :return: 响应结果
        :rtype: ApiResponse
        :raises ApiError: 通用错误
        :raises RequestError: 本地发起请求失败
        :raises HttpError: 请求响应非 2xx
        """
        return super().post(path, payload, options)

    def put(
        self,
        path: str,
        payload: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOption] = None,
    ) -> ApiResponse:
        """
        发起 PUT 请求

        :param path: 请求的相对路径
        :param payload: 请求体，将以 JSON 的方式发送给服务器
        :param options: 请求额外的定制信息
        :return: 响应结果
        :rtype: ApiResponse
        :raises ApiError: 通用错误
        :raises RequestError: 本地发起请求失败
        :raises HttpError: 请求响应非 2xx
        """
        return super().put(path, payload, options)

    def delete(
        self,
        path: str,
        query: Optional[Dict[str, Any]] = None,
        options: Optional[RequestOption] = None,
    ) -> ApiResponse:
        """
        发起 DELETE 请求

        :param path: 请求的相对路径
        :param query: 请求额外的 parameter
        :param options: 请求额外的定制信息
        :return: 响应结果
        :rtype: ApiResponse
        :raises ApiError: 通用错误
        :raises RequestError: 本地发起请求失败
        :raises HttpError: 请求响应非 2xx
        """
        return super().delete(path, query, options)


ApiResponse.__module__ = __name__
ApiResponse.__doc__ = """
请求返回的响应

:param dict headers: 响应头
:param dict data: 响应体
"""

RequestOption.__module__ = __name__
RequestOption.__doc__ = """
额外的请求配置

:param dict headers: 单次请求额外的请求头
:param int timeout: 请求超时时间，默认 30 s，设置为 0 则不超时；超时返回 :class:`RequestError <longbridge.error.RequestError>`
"""

__all__ = [
    "ApiResponse",
    "Auth",
    "Config",
    "HttpClient",
    "RequestOption",
]
