# Longbridge OpenAPI SDK for Python

[![PyPI Versions](https://img.shields.io/pypi/pyversions/longbridge.svg)](https://pypi.org/project/longbridge)
[![Read the Docs](https://readthedocs.org/projects/longbridge/badge/?version=latest)](https://longbridge.readthedocs.io/en/latest)

SDK 提供了 HTTP / WebSocket Clients，方便地使用 [Longbridge OpenAPI](https://open.longbridgeapp.com)。

Longbridge OpenAPI SDK 基于 Rust 提供标准实现，通过 FFI 提供给 Python 使用。

目前，我们支持如下系统架构：

- Linux x86_64 & aarch64
- Mac x86_64 & aarch64
- Windows x86_64 & i686

## Installation

```bash
$ pip3 install longbridge protobuf
```

## Get started

下面我们以获取资产为例，演示一下如何使用 SDK。

### 开始需求

1. 在 Longbridge 开户
2. 完成 Python3 环境安装，并安装 Pip
3. 从 [Longbridge OpenAPI](https://open.longbridgeapp.com) 官网获取 `APP_KEY`, `APP_SECRET`, `ACCESS_TOKEN` 等信息。

### 获取 APP_KEY, APP_SECRET, ACCESS_TOKEN

访问 [Longbridge OpenAPI](https://open.longbridgeapp.com) 网站，登录后，进入 “个人中心”。

在页面上会给出 “应用凭证” 凭证信息，我们拿到以后设置环境变量，便于后面开发使用方便。

```bash
$ export LONGBRIDGE_APP_KEY=从页面上获取到的 App Key
$ export LONGBRIDGE_APP_SECRET=从页面上获取到的 App Secret
$ export LONGBRIDGE_ACCESS_TOKEN=从页面上获取到的 Access Token
```

### API Host

- HTTP API - https://openapi.lbkrs.com
- WebSocket - wss://openapi-quote.longbridge.global

> NOTE: 为了便于演示，我们的例子里面均通过 `LONGBRIDGE_APP_KEY`、`LONGBRIDGE_APP_SECRET`、`LONGBRIDGE_ACCESS_TOKEN` 这样的环境变量来获取配置信息。如您在 Windows 环境不方便使用环境变量。可根据个人需要，修改 Python 代码。

### 调用 HTTP 请求

创建一个 `main.py` 贴入下面的代码：

```py
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/asset/account")
print(json.dumps(resp.data, indent=2))
```

运行 `main.py` 后，会输出如下：

```bash
python3 main.py
```

```json
{
  "list": [
    {
      "cashInfos": [
        {
          "available_cash": "32966.49",
          "currency": "HKD",
          "frozen_cash": "0.00",
          "redemption_cash": "0",
          "settling_cash": "0.00",
          "withdraw_cash": "32966.49"
        },
        {
          "available_cash": "-6582.61",
          "currency": "USD",
          "frozen_cash": "5.76",
          "redemption_cash": "0",
          "settling_cash": "0.00",
          "withdraw_cash": "-6582.61"
        }
      ],
      "currency": "HKD",
      "margin_call": "3105871.08",
      "max_finance_amount": "1093000",
      "remaining_finance_amount": "702.348304552590266876",
      "risk_level": "3",
      "total_cash": "-2829.14"
    }
  ]
}
```

### 订阅实时行情

创建一个 `subscribe_quote.py` 并写入下面的代码：

```py
import os
import json
from longbridge.http import Auth, Config, HttpClient
from longbridge.ws import ReadyState, WsCallback, WsClient
from longbridge.quote.quote_pb2 import ( Command, PushQuote, SubscribeRequest, SubscriptionResponse, SubType)

class MyWsCallback(WsCallback):
    def on_push(self, command: int, body: bytes):
        if command == Command.PushQuoteData:
            quote = PushQuote()
            quote.ParseFromString(body)
            print(f"Received -> {quote}")
        else:
            print(f"Received unknown -> {command}")

    def on_state(self, state: ReadyState):
        print(f"Received state -> {state}")

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))
ws = WsClient("wss://openapi-quote.longbridge.global", http, MyWsCallback())

req = SubscribeRequest(symbol=["700.HK"], sub_type=[SubType.QUOTE], is_first_push=True)
result = ws.send_request(Command.Subscribe, req.SerializeToString())
resp = SubscriptionResponse()
resp.ParseFromString(result)

print(json.dumps(resp.sub_list))
```

### 做一次下单动作

下面我们做一次 [委托下单](https://open.longbridgeapp.com/docs/trade/order/submit) 动作，我们假设要以 50 HKD 买入 `700.HK` 的数量为 `100`。

> NOTE: 为了防止测试买入成功，这里演示给了一个较低的价格，避免成交。OpenAPI 操作均等同与线上交易，请谨慎操作，开发调试注意参数细节。

创建一个 `submit_order.py` 并写入下面的代码：

```py
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

payload = {
    "side": "Buy",
    "symbol": "700.HK",
    "order_type": "LO",
    "submitted_price": "50",
    "submitted_quantity": "200",
    "time_in_force": "Day",
    "remark": "Hello from Python SDK"
}

try:
  resp = http.post("/v1/trade/order", payload=payload)
  print(json.dumps(resp.data, indent=2))
except Exception as e:
  print(f"Submit order error\ncode: {e.code}\nmessage: {e.message}")
```

执行 `python3 submit_order.py` 后，会输出如下：

```json
{
  "order_id": "707530744027713536"
}
```

加入下单失败，你可能会看到这样的错误信息：

```
Submit order error
code: 602035
message: 委托价不符合最小价格变动单位
```

### 获取当日订单

```py
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/trade/order/today")
print(json.dumps(resp.data, indent=2))
```

如果前面你有提交订单，你应该会看到这样的结果：

```json
{
  "orders": [
    {
      "currency": "HKD",
      "executed_price": "0",
      "executed_quantity": "0",
      "expire_date": "2022-05-10",
      "last_done": "",
      "limit_offset": "",
      "msg": "",
      "order_id": "707530744027713536",
      "order_type": "LO",
      "outside_rth": "UnknownOutsideRth",
      "price": "50",
      "quantity": "200",
      "side": "Buy",
      "status": "CanceledStatus",
      "stock_name": "\u817e\u8baf\u63a7\u80a1",
      "submitted_at": "1651917274",
      "symbol": "700.HK",
      "tag": "Normal",
      "time_in_force": "Day",
      "trailing_amount": "",
      "trailing_percent": "",
      "trigger_at": "0",
      "trigger_price": "",
      "trigger_status": "NOT_USED",
      "updated_at": "1651917561"
    },
    {
      // ...
    }
  ]
}
```

上面例子已经完整演示了如何使用 SDK 访问 OpenAPI 的接口，更多其他接口请详细阅读 [Longbridge OpenAPI 文档](https://open.longbridgeapp.com/docs)，根据不同的接口使用。

### 更多例子

https://github.com/longbridgeapp/openapi-python/tree/main/examples

### Python SDK API 文档

https://longbridge.readthedocs.io/en/latest/api.html
