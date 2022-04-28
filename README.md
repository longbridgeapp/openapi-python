# Welcome to longbridge's documentation!

[![Supported Versions](https://img.shields.io/pypi/pyversions/longbridge.svg)](https://pypi.org/project/longbridge)
[![Read the Docs](https://readthedocs.org/projects/longbridge/badge/?version=latest)](https://longbridge.readthedocs.io/zh_CN/latest)

Longbridge OpenSDK 提供了 Http/Ws Clients，方便地使用 Longbridge OpenAPI。

### 示例

1. 从 https://github.com/longbridgeapp/openapi-protobufs 下载 quote.proto 文件

2. 编译 quote.proto： `protoc --python_out=. quote.proto`

3. 项目安装依赖：`pip install longbridge protobuf`

4. Happy Coding:

```python
from longbridge.http import Auth, Config, HttpClient
from longbridge.ws import ReadyState, WsCallback, WsClient
from quote_pb2 import Command, SubscribeRequest, SubType

auth = Auth("{app_key}", "{app_secret}", access_token=None)
config = Config(base_url="https://openapi.lbkrs.com")
http = HttpClient(auth, config)
response = http.get("/v1/test")


class MyWsCallback(WsCallback):
    def on_push(self, command: int, body: bytes):
        print(f"received push message: {command} {body}")

    def on_state(self, state: ReadyState):
        print(f"received state change: {state}")


ws = WsClient("wss://openapi-quote.lbkrs.com", MyWsCallback())
resp = ws.send_request(
    Command.Subscribe,
    SubscribeRequest(
        symbol=["00700.HK"], sub_type=[SubType.QUOTE, SubType.DEPTH], is_first_push=True
    ),
)
```

### We Love Rust

Longbridge OpenSDK 基于 Rust 提供标准实现，通过 FFI 提供给 Python 使用。

目前，我们支持如下系统架构：

-   Windows x86
-   Windows x86_64
-   Linux x86_64
-   Linux arm64
-   Mac x86_64 & arm64

如有其他需求，请联系 jifeng.yin # longbridge.sg
