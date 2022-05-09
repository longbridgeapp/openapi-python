# 获取券商席位 id
# https://open.longbridgeapp.com/docs/quote/pull/broker-ids
import os
import time
from google.protobuf import text_format
from longbridge.http import Auth, Config, HttpClient
from longbridge.ws import ReadyState, WsCallback, WsClient
# Protobuf 变量定义参见：https://github.com/longbridgeapp/openapi-protobufs/blob/main/quote/api.proto
from longbridge.proto.quote_pb2 import (Command, ParticipantBrokerIdsResponse)

class MyWsCallback(WsCallback):
    def on_state(self, state: ReadyState):
        print(f"-> state: {state}")

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))
ws = WsClient("wss://openapi-quote.longbridge.global", http, MyWsCallback())

# 运行前请访问 “开发者中心“ 确保账户有正确的行情权限。
# 如没有开通行情权限，可以通过 "长桥" 手机客户端，并进入 “我的 - 我的行情 - 行情商城“ 购买开通行情权限。
result = ws.send_request(Command.QueryParticipantBrokerIds, "")
resp = ParticipantBrokerIdsResponse()
resp.ParseFromString(result)

print(f"Broker ids:\n\n")
for broker_number in resp.participant_broker_numbers:
    print(f"{text_format.MessageToString(broker_number, as_utf8=True)}")