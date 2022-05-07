# 获取账户资金信息
# https://open.longbridgeapp.com/docs/trade/asset/account
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/asset/account")
print(json.dumps(resp.data, indent=2))

# {
#   "list": [
#     {
#       "cashInfos": [
#         {
#           "available_cash": "32966.49",
#           "currency": "HKD",
#           "frozen_cash": "0.00",
#           "redemption_cash": "0",
#           "settling_cash": "0.00",
#           "withdraw_cash": "32966.49"
#         },
#         {
#           "available_cash": "-6582.61",
#           "currency": "USD",
#           "frozen_cash": "5.76",
#           "redemption_cash": "0",
#           "settling_cash": "0.00",
#           "withdraw_cash": "-6582.61"
#         }
#       ],
#       "currency": "HKD",
#       "margin_call": "3105871.08",
#       "max_finance_amount": "1093000",
#       "remaining_finance_amount": "702.348304552590266876",
#       "risk_level": "3",
#       "total_cash": "-2829.14"
#     }
#   ]
# }