# 委托下单
# 购买 700.HK 限价 50 HKD 买 200 股。
# https://open.longbridgeapp.com/docs/trade/order/submit
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

# {
#   "order_id": "707530744027713536"
# }

# 获取当日订单
# https://open.longbridgeapp.com/docs/trade/order/today_orders
resp = http.get("/v1/trade/order/today")
print(json.dumps(resp.data, indent=2))

# 返回结果
# {
#   "orders": [
#     {
#       "currency": "HKD",
#       "executed_price": "0",
#       "executed_quantity": "0",
#       "expire_date": "2022-05-10",
#       "last_done": "",
#       "limit_offset": "",
#       "msg": "",
#       "order_id": "707530744027713536",
#       "order_type": "LO",
#       "outside_rth": "UnknownOutsideRth",
#       "price": "50",
#       "quantity": "200",
#       "side": "Buy",
#       "status": "CanceledStatus",
#       "stock_name": "\u817e\u8baf\u63a7\u80a1",
#       "submitted_at": "1651917274",
#       "symbol": "700.HK",
#       "tag": "Normal",
#       "time_in_force": "Day",
#       "trailing_amount": "",
#       "trailing_percent": "",
#       "trigger_at": "0",
#       "trigger_price": "",
#       "trigger_status": "NOT_USED",
#       "updated_at": "1651917561"
#     }
#   ]
# }