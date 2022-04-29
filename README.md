# Longbridge OpenAPI SDK for Python

[![PyPI Versions](https://img.shields.io/pypi/pyversions/longbridge.svg)](https://pypi.org/project/longbridge)
[![Read the Docs](https://readthedocs.org/projects/longbridge/badge/?version=latest)](https://longbridge.readthedocs.io/en/latest)

SDK 提供了 HTTP / WebSocket Clients，方便地使用 [Longbridge OpenAPI](https://open.longbridgeapp.com)。

Longbridge OpenAPI SDK 基于 Rust 提供标准实现，通过 FFI 提供给 Python 使用。

目前，我们支持如下系统架构：

-  Linux x86_64 & aarch64
-  Mac x86_64 & aarch64
-  Windows x86_64 & i686

## Installation

```bash
$ pip install longbridge protobuf
```

## Get started

从 https://github.com/longbridgeapp/openapi-protobufs 下载 `quote.proto` 文件。

编译 quote.proto：

```bash
$ protoc --python_out=. quote.proto
```

## Usage

```py
from longbridge.http import Auth, Config, HttpClient
from longbridge.ws import ReadyState, WsCallback, WsClient
from quote_pb2 import (
    Command,
    PushQuote,
    SubscribeRequest,
    SubscriptionResponse,
    SubType,
)

auth = Auth("{app_key}", "{app_secret}", access_token=None)
config = Config(base_url="https://openapi.lbkrs.com")
http = HttpClient(auth, config)

# [获取账户资金](https://open.longbridgeapp.com/docs/trade/asset/account)
response = http.get("/v1/trade/asset/account")
print(f"receive response: {response.body}({response.headers})")

# ----- websocket -----
class MyWsCallback(WsCallback):
    def on_push(self, command: int, body: bytes):
        if command == Command.PushQuoteData:
            quote = PushQuote()
            quote.ParseFromString(body)
            print(f"received quote push: {quote}")
        else:
            print(f"received unknown push: {command}")

    def on_state(self, state: ReadyState):
        print(f"received state change: {state}")


ws = WsClient("wss://openapi-quote.lbkrs.com", http, MyWsCallback())

# [订阅行情数据](https://open.longbridgeapp.com/docs/quote/subscribe/subscribe)
req = SubscribeRequest(
    symbol=["700.HK"], sub_type=[SubType.QUOTE], is_first_push=True
)
result = ws.send_request(Command.Subscribe, req.SerializeToString())
resp = SubscriptionResponse()
resp.ParseFromString(result)
print(f"subscribe successfully: {resp.sub_list}")
```

如有其他需求，请提 issue.
