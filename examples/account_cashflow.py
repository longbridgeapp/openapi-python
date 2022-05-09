# 获取获取资金流水信息
# https://open.longbridgeapp.com/docs/trade/asset/cashflow
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/asset/cashflow",{"start_time":"1623881671","end_time":"1626881673"})
print(json.dumps(resp.data, indent=2))

# {
#   "code": 0,
#   "data": {
#     "list": [
#       {
#         "transaction_flow_name": "股票买入成交",
#         "direction": 1,
#         "balance": "-248.60",
#         "currency": "USD",
#         "business_time": 1621507957,
#         "symbol": "AAPL.US",
#         "description": "AAPL"
#       },
#       {
#         "transaction_flow_name": "股票买入成交",
#         "direction": 1,
#         "balance": "-125.16",
#         "currency": "USD",
#         "business_time": 1621504824,
#         "symbol": "AAPL.US",
#         "description": "AAPL"
#       }
#     ]
#   }
# }