"""
requests 库常用用法示例（GET 为主，顺带演示其它常见用法）

说明（如何使用这个文件）：
- 每个函数都演示一个典型场景：最简单 GET、带参数、带请求头、异常处理、Session、POST、上传文件等
- 所有示例都写成了独立的小函数，方便你在 main() 里按需注释 / 取消注释来单独运行、观察效果
- 关键代码几乎每一行都加了中文注释，方便你逐行对照理解
- 统一使用 `https://httpbin.org` 这个测试网站，它会把你发过去的内容原样返回，非常适合练习 HTTP
"""

import json  # 用于演示手动处理 json
import requests  # 第三方 HTTP 库，需要先：pip install requests
from requests import RequestException  # requests 的异常基类


def basic_get():
    """
    最基础的 GET 请求

    场景：像浏览器一样，请求一个页面，不带任何参数，查看返回的内容和状态。
    关键点：
    - 只传 url，不带 params / headers
    - 认识 Response 对象的几个最常用属性：status_code / url / headers / text
    """
    # 要请求的目标地址（url 字符串必须是完整的 http/https 地址）
    url = "https://httpbin.org/get"  # httpbin 是一个“回声”网站，会把你请求的信息原样返回，方便调试

    # 直接发送最简单的 GET 请求
    # requests.get(...) 返回的是一个 Response 对象，里面封装了所有响应相关的信息
    resp = requests.get(url)

    print("【basic_get】")
    # resp.status_code：HTTP 状态码，200 表示成功，4xx/5xx 表示客户端或服务端错误
    print("状态码：", resp.status_code)
    # resp.url：服务器实际收到的 URL（有时会被重定向，这里能看到最终地址）
    print("最终请求的 URL：", resp.url)
    # resp.headers：一个类似字典的对象，保存所有响应头；这里取出常见的 Content-Type 类型，看看是 json 还是 html 等
    print("部分响应头：", resp.headers.get())
    # resp.text：把响应体按编码解码成字符串；这里只打印前 100 个字符，避免太长
    print("文本响应正文前 100 个字符：", resp.text[:100])
    print("-" * 60)


def get_with_params():
    """
    GET 携带查询参数（?key=value）

    场景：常见的“列表分页”、“搜索条件”等都会放在 URL 的查询字符串里。
    关键点：
    - 使用 params 参数传入字典，requests 会自动帮你拼接成 ?key=value&...
    - 可以通过 resp.url 看看最终拼出来的完整 URL 是什么样子
    """
    url = "https://httpbin.org/get"  # 依旧使用 httpbin 的 /get 接口进行演示

    # params：查询参数字典，会被自动编码到 URL 查询字符串中
    # 最终效果类似：https://httpbin.org/get?name=侯金双&city=广东&page=1&size=10
    params = {
        "name": "侯金双",  # 普通字符串参数
        "city": "广东",  # 非 ASCII 字符会被自动进行 URL 编码
        "page": 1,  # 数字也可以，requests 会自动转为字符串
        "size": 10,  # 一般分页时用于“每页条数”
    }

    # 发送 GET 请求时，把 params=... 传进去即可
    resp = requests.get(url, params=params)

    print("【get_with_params】")
    # 最终 URL 中会包含编码之后的查询参数（可以用浏览器粘贴过去看看效果）
    print("最终 URL：", resp.url)
    # httpbin 会把解析出来的查询参数放到 json 结果中的 args 字段里
    # resp.json()：把响应体按 JSON 格式解析成 Python 字典，如果不是合法 JSON 会抛异常
    print("JSON 形式返回的数据：", resp.json())
    print("-" * 60)


def get_with_headers():
    """
    GET 自定义请求头（headers）

    场景：
    - 模拟浏览器访问，需要带特定的 User-Agent
    - 调某些接口需要在请求头里带 Token / 版本号等信息
    """
    url = "https://httpbin.org/get"  # 依旧使用 /get 接口

    # 常见的自定义请求头写在一个普通字典里即可
    headers = {
        # User-Agent：告诉服务器“我是哪个客户端”，很多网站会根据这个做适配或限制
        "User-Agent": "MySimpleClient/1.0",
        # Accept：告诉服务器“我希望你返回哪种类型的数据”，比如 application/json、text/html 等
        "Accept": "application/json",
    }

    # 把 headers=... 传给 get 方法即可，requests 会自动带上这些请求头
    resp = requests.get(url, headers=headers)

    print("【get_with_headers】")
    # 本地打印一下我们设置的 User-Agent
    print("请求头中 User-Agent：", headers["User-Agent"])
    # httpbin 会把它“看到的请求头”放到 json 里的 headers 字段中，方便我们对比验证
    print("服务器看到的 headers（部分）：", resp.json().get("headers"))
    print("-" * 60)


def response_common_attrs():
    """
    常用响应属性演示：
    - status_code：状态码
    - ok：是否 200~399
    - url：最终访问地址
    - headers：响应头
    - text：按编码解码后的字符串
    - content：原始字节
    - json()：按 JSON 解析后的 Python 对象
    """
    url = "https://httpbin.org/get"
    # 这里额外带一个简单的查询参数 q=python，方便在结果中观察
    resp = requests.get(url, params={"q": "python"})

    print("【response_common_attrs】")
    # 状态码：int 类型，例如 200 / 404 / 500 等
    print("状态码：", resp.status_code)
    # resp.ok：requests 帮我们做的一个“语法糖”，200~399 返回 True，其它返回 False
    print("是否请求成功（requests 自带判断）：", resp.ok)
    # 最终访问的 URL，包含查询字符串
    print("最终 URL：", resp.url)
    # 响应头是一个类似字典的对象，包含服务器返回的各种元信息
    print("响应头：", resp.headers)
    # text：把响应体按推断出来的编码（或指定 encoding）解码成字符串
    print("文本内容 text（str）：", type(resp.text), resp.text[:80])
    # content：原始的字节数据，适合下载图片、文件等二进制内容
    print("二进制内容 content（bytes）：", type(resp.content), resp.content[:20])

    # 如果确定返回的是 json，可以直接 resp.json() 得到 Python 对象（通常是 dict）
    data = resp.json()
    print("json() 解析后类型：", type(data))
    # httpbin 会把解析到的查询参数放到 args 字段里，这里可以看到 {"q": "python"}
    print("json() 中 args 字段：", data.get("args"))
    print("-" * 60)


def get_timeout_and_error():
    """
    设置超时时间 + 基本异常处理

    场景：
    - 接口很慢 / 网络不稳定时，不希望一直卡住等待，需要设置超时时间
    - 请求失败时要能捕获异常，避免程序直接崩掉
    """
    # /delay/3：httpbin 提供的一个接口，会故意延迟 3 秒再返回响应
    url = "https://httpbin.org/delay/3"

    try:
        # timeout=1 表示最多等 1 秒，如果 1 秒内没返回，就抛出 requests.Timeout 异常
        # 注意：timeout 控制的是“连接 + 读取”的时间，不是整个程序的绝对时间
        resp = requests.get(url, timeout=1)
        print("【get_timeout_and_error】")
        print("请求成功，状态码：", resp.status_code)
    except requests.Timeout:
        # 捕获超时错误
        print("【get_timeout_and_error】请求超时（Timeout）")
    except RequestException as e:
        # 所有 requests 的异常基类，兜底处理
        print("【get_timeout_and_error】请求出错：", e)
    print("-" * 60)


def get_with_cookies():
    """
    发送和读取 cookies

    场景：
    - 模拟浏览器登录后带上 sessionid 等 cookie 访问页面
    - 有些简单接口会直接把用户信息放在 cookie 里
    """
    # httpbin 的 /cookies 接口会把它“看到的 cookies”原样返回，适合用来测试
    url = "https://httpbin.org/cookies"

    # cookies 参数同样传入一个字典即可，每个键值对就是一个 cookie 项
    cookies = {
        "sessionid": "abc123",  # 模拟一个 session id
        "user": "hjs",  # 模拟一个用户名
    }

    resp = requests.get(url, cookies=cookies)

    print("【get_with_cookies】")
    print("服务端返回的 cookies 字段：", resp.json().get("cookies"))
    print("-" * 60)


def use_session():
    """
    使用 Session 复用连接、自动携带 cookies

    场景：
    - 登录一次后，后续所有请求都自动带上 cookie / headers
    - 与服务器保持长连接，减少握手开销（比每次 new 一个 requests.get 更高效）
    """
    # Session 对象可以在多个请求之间共享：cookies、部分 headers、连接等
    session = requests.Session()

    # 为整个 session 设置默认请求头：之后 session.get / post 都会自动带上这个 User-Agent
    session.headers.update({"User-Agent": "SessionClient/1.0"})

    # 第一次请求：访问一个专门“设置 cookie”的接口，相当于登录行为
    session.get("https://httpbin.org/cookies/set?token=hello")

    # 第二次请求：查看当前携带的 cookie（注意，这里我们没有手动传 cookies 参数）
    resp = session.get("https://httpbin.org/cookies")

    print("【use_session】")
    print("Session 自动携带的 cookies：", resp.json().get("cookies"))
    print("-" * 60)


def post_form_data():
    """
    POST 表单（application/x-www-form-urlencoded）

    场景：
    - 传统网页表单提交，比如登录表单、注册表单
    - 很多老接口默认就是这种格式
    """
    url = "https://httpbin.org/post"  # httpbin 的 /post 接口会把各种请求体原样返回

    # data 字典会自动编码为 application/x-www-form-urlencoded 表单格式
    data = {
        "username": "hjs",  # 表单中“用户名”字段
        "password": "123456",  # 表单中“密码”字段（这里只是演示，真实场景不要明文）
    }

    resp = requests.post(url, data=data)

    print("【post_form_data】")
    json_data = resp.json()
    print("form 字段（服务器解析出来的表单数据）：", json_data.get("form"))
    print("-" * 60)


def post_json_data():
    """
    POST JSON 数据（application/json）

    场景：
    - 现在大部分 RESTful / 前后端分离接口都使用 JSON 作为请求体格式
    - 后端一般通过 request.body / request.json() 等方式来读取
    """
    url = "https://httpbin.org/post"

    # 准备要发送的 Python 字典（会被序列化成 JSON 字符串）
    payload = {
        "name": "侯金双",  # 普通字符串字段
        "age": 18,  # 数字字段
        "skills": ["python", "requests"],  # 列表字段
    }

    # 使用 json= 参数更方便，requests 会自动：
    # 1. 把字典转成 JSON 字符串
    # 2. 加上 Content-Type: application/json 请求头
    resp = requests.post(url, json=payload)

    print("【post_json_data】")
    print("请求体（服务器看到的 json）：", resp.json().get("json"))

    # 等价的写法：手动 dumps + 指定 headers
    resp2 = requests.post(
        url,
        data=json.dumps(payload),  # 手动把字典转成 JSON 字符串
        headers={"Content-Type": "application/json"},
    )
    print("等价写法的 json 字段：", resp2.json().get("json"))
    print("-" * 60)


def file_upload_example():
    """
    演示文件上传（multipart/form-data）

    场景：
    - 常见的“上传头像”、“上传附件”等功能
    - 表单中既有普通字段，又有文件字段
    说明：
    - 这里只演示构造 files 参数的方式，不依赖真实文件，方便你直接运行
    """
    url = "https://httpbin.org/post"

    # 一般写法是：
    # with open("test.txt", "rb") as f:
    #     files = {"file": ("test.txt", f, "text/plain")}
    #     resp = requests.post(url, files=files)
    #
    # 这里用内存中的 bytes 模拟一个“文件”，避免必须存在真实文件
    # 第一个元素是文件名，第二个是二进制内容，第三个是 MIME 类型
    files = {
        "file": ("hello.txt", b"hello world", "text/plain"),
    }

    resp = requests.post(url, files=files)

    print("【file_upload_example】")
    print("服务器解析出的 files 字段：", resp.json().get("files"))
    print("-" * 60)


def other_http_methods():
    """
    PUT / DELETE 等其它常见 HTTP 方法

    场景：
    - RESTful 风格接口中：
      - GET    -> 查询
      - POST   -> 新增
      - PUT    -> 整体更新
      - PATCH  -> 部分更新
      - DELETE -> 删除
    """
    url = "https://httpbin.org/put"

    # PUT 请求
    put_resp = requests.put(url, json={"key": "value"})

    # DELETE 请求
    delete_resp = requests.delete("https://httpbin.org/delete")

    print("【other_http_methods】")
    print("PUT 状态码：", put_resp.status_code)
    print("DELETE 状态码：", delete_resp.status_code)
    print("-" * 60)


def main():
    """统一调用上面的演示函数，方便一次性运行查看效果"""
    # 你可以根据需要注释 / 取消注释某些函数调用
    basic_get()
    # get_with_params()
    # get_with_headers()
    # response_common_attrs()
    # get_timeout_and_error()
    # get_with_cookies()
    # use_session()
    # post_form_data()
    # post_json_data()
    # file_upload_example()
    # other_http_methods()


if __name__ == "__main__":
    # 运行 main()，依次演示上面所有函数的效果
    # 如果你只想看某一个功能，可以临时注释掉其他函数调用
    main()

    # 下面保留一个“最简版”的 GET 示例，方便快速回顾最核心用法
    # 等价于一开始你写的那段代码，只是加上了更详细的注释

    # 导入 requests 库
    import requests

    # 要请求的 URL
    url = "https://httpbin.org/get"

    # 通过 params 传查询参数，它们会出现在 URL 的 ? 后面
    resp = requests.get(url, params={"name": "侯金双", "city": "广东"})

    # Response.status_code：状态码
    print("状态码：", resp.status_code)
    # Response.text：把响应正文解码成字符串
    print("响应正文：", resp.text)
    # Response.url：最终访问的 URL（包含编码后的查询参数）
    print("最终请求的 URL：", resp.url)
