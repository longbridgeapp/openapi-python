# 获取股票持仓信息
# https://open.longbridgeapp.com/docs/trade/asset/stock
import os
import json
from longbridge.http import Auth, Config, HttpClient

auth = Auth(os.getenv("LONGBRIDGE_APP_KEY"), os.getenv("LONGBRIDGE_APP_SECRET"), access_token=os.getenv("LONGBRIDGE_ACCESS_TOKEN"))
http = HttpClient(auth, Config(base_url="https://openapi.lbkrs.com"))

resp = http.get("/v1/asset/stock?symbol=700.HK&symbol=BABA.US")
print(json.dumps(resp.data, indent=2))

# {
#   "code": 0,
#   "data": {
#     "list": [
#       {
#         "account_channel": "lb",
#         "stock_info": [
#           {
#             "symbol": "700.HK",
#             "symbol_name": "腾讯控股",
#             "currency": "HK",
#             "quality": "650",
#             "available_quality": "-450",
#             "cost_price": "457.53"
#           },
#           {
#             "symbol": "9991.HK",
#             "symbol_name": "宝尊电商-SW",
#             "currency": "HK",
#             "quality": "200",
#             "available_quality": "0",
#             "cost_price": "32.25"
#           },
#           {
#             "symbol": "TCEHY.US",
#             "symbol_name": "腾讯控股 (ADR)",
#             "currency": "US",
#             "quality": "10",
#             "available_quality": "10"
#           },
#           {
#             "symbol": "2628.HK",
#             "symbol_name": "中国人寿",
#             "currency": "HK",
#             "quality": "9000",
#             "available_quality": "0"
#           },
#           {
#             "symbol": "5.HK",
#             "symbol_name": "汇丰控股",
#             "currency": "HK",
#             "quality": "2400",
#             "available_quality": "2000"
#           },
#           {
#             "symbol": "BABA.US",
#             "symbol_name": "阿里巴巴",
#             "currency": "US",
#             "quality": "2000209",
#             "available_quality": "2000209"
#           },
#           {
#             "symbol": "2.HK",
#             "symbol_name": "中电控股",
#             "currency": "HK",
#             "quality": "2000",
#             "available_quality": "2000"
#           },
#           {
#             "symbol": "NOK.US",
#             "symbol_name": "诺基亚",
#             "currency": "US",
#             "quality": "1",
#             "available_quality": "0"
#           }
#         ]
#       }
#     ]
#   }
# }