# 获取轮证筛选列表
# https://open.longbridgeapp.com/docs/quote/pull/warrant-filter
import os
import time
from longbridge.http import Auth, Config, HttpClient
from longbridge.ws import ReadyState, WsCallback, WsClient
# Protobuf 变量定义参见：https://github.com/longbridgeapp/openapi-protobufs/blob/main/quote/api.proto
from longbridge.proto.quote_pb2 import (Command, FilterConfig, WarrantFilterListRequest, WarrantFilterListResponse)

class MyWsCallback(WsCallback):
    def on_state(self, state: ReadyState):
        print(f"-> state: {state}")

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))
ws = WsClient("wss://openapi-quote.longbridge.global", http, MyWsCallback())

# 运行前请访问 “开发者中心“ 确保账户有正确的行情权限。
# 如没有开通行情权限，可以通过 "长桥" 手机客户端，并进入 “我的 - 我的行情 - 行情商城“ 购买开通行情权限。
filterConfig = FilterConfig(sort_by=0, sort_order=1, sort_offset=0, sort_count=10)
req = WarrantFilterListRequest(symbol="700.HK", filter_config=filterConfig, language=1)
result = ws.send_request(Command.QueryWarrantFilterList, req.SerializeToString())
resp = WarrantFilterListResponse()
resp.ParseFromString(result)

print(f"Filtered warrant:\n\n {resp}")