import requests


resp = requests.get("https://httpbin.org/get")

print("状态码：", resp.status_code)
print("响应正文：", resp.text)
