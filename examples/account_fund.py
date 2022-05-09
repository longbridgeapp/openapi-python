# 获取基金持仓信息
# https://open.longbridgeapp.com/docs/trade/asset/fund
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/asset/fund")
print(json.dumps(resp.data, indent=2))

# {
#     "code": 0,
#     "data": {
#       "list": [
#         {
#           "account_channel": "lb",
#           "fund_info": [
#             {
#               "symbol": "HK0000447943",
#               "symbol_name": "高腾亚洲收益基金",
#               "currency": "USD",
#               "holding_units": "5.000",
#               "current_net_asset_value": "0",
#               "cost_net_asset_value": "0.00",
#               "net_asset_value_day": 1649865600
#             }
#           ]
#         }
#       ]
#     }
#   }