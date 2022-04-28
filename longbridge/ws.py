from datetime import timedelta
from typing import Optional, Sequence
from . import engine_uniffi
from .engine_uniffi import WsCallback, ReadyState
from .http import HttpClient


class WsClient(engine_uniffi.WsClient):
    """
    WS Client 实现
    """
    def __init__(self, url: str, http: HttpClient, callback: WsCallback):
        """
        初始化 WS Client

        :param url: 连接服务端最低值
        :param http: HTTP 客户端，为了获取 token，自动重连
        :param callback: 用户提供的状态和推送回调函数
        """
        super().__init__(url, http, callback)

    def send_request(
        self,
        command: int,
        payload: bytes,
        timeout: Optional[timedelta] = None,
    ) -> bytes:
        """
        发送请求

        :param command: 请求命令，请参阅 pb 文件
        :param payload: protobuf 序列化后的请求体，请参阅 pb 文件
        :param timeout: 超时时间
        :return: 返回的 protobuf 数据，类型为 command 对应的 response type，请参阅 pb 文件
        :raises ApiError: 通用错误，如连接不在 OPEN 状态
        :rtype: bytes
        """
        return super().send_request(command, payload, timeout)

    def ready_state(self) -> ReadyState:
        """
        当前连接状态

        :return: 连接状态
        :rtype: ReadyState
        """
        return super().ready_state()

    def close(self):
        """
        关闭当前连接，不再尝试重连
        """
        return super().close()

    def reconnect(self):
        """
        从关闭状态重新连接
        """
        return super().reconnect()

WsCallback.__module__ = __name__
WsCallback.__doc__ = """
WS 回调函数，用户需自行实现如下两个方法：

* on_push: 接收 command(int) 和 payload(bytes)
* on_state: 接收 state(ReadyState)
"""

ReadyState.__module__ = __name__
ReadyState.__doc__ = """
连接状态

1. OPENING: 开始连接（用户不会收到，首次启动 SDK 自动等待到可用状况）
2. OPEN: 连接正常，可以接收和发送数据
3. RECONNECTING: 连接异常，自动重连中
4. CLOSED: 连接用户主动关闭，不再重连
"""
ReadyState.OPENING.__doc__ = """
开始启动，用户不会收到，首次启动 SDK 自动等待到可用状态
"""
ReadyState.OPEN.__doc__ = """
连接正常，可以接收和发送数据
"""
ReadyState.RECONNECTING.__doc__ = """
连接异常，自动重连中
"""
ReadyState.CLOSED.__doc__ = """
连接用户主动关闭，不再重连
"""


__all__ = ["WsCallback", "WsClient", "ReadyState"]
