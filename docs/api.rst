.. _api:

Developer Interface
===================
长桥 OpenSDK 提供了 HTTP 客户端和 Websocket 客户端的实现。

Error
-----
.. module:: longbridge.error

此 SDK 所抛出的异常

.. autoclass:: ApiError()

.. autoclass:: HttpError()

.. autoclass:: RequestError()

Http Client
-----------
.. module:: longbridge.http

HTTP 客户端实现了加签逻辑，提供了 GET/POST/PUT/DELETE 方法，正常响应返回 ApiResponse 对象，异常响应抛出 ApiError 异常。

.. autoclass:: HttpClient()
   :members:
   :special-members: __init__

.. autoclass:: Auth

.. autoclass:: Config

.. autoclass:: ApiResponse()

.. autoclass:: RequestOption


Websocket Client
----------------
.. module:: longbridge.ws

Websocket 客户端实现了对连接的自动保活，提供了 send_request 方法，及对 push 数据 / state 变更的回调。

.. autoclass:: WsClient()
   :members:
   :special-members: __init__

.. autoclass:: WsCallback

.. autoclass:: ReadyState()

