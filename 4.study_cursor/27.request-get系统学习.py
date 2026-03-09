"""
requests 库常用用法示例（GET 为主，顺带演示其它常见用法）

【整体说明：如果你是完全小白，建议这么学】
1. 把这个文件从上往下简单看一遍，大致知道有哪几种用法。
2. 到下面的 main() 函数里，只保留一个你想看的函数，比如 basic_get()，然后运行文件，观察输出。
3. 对着输出 + 注释，慢慢体会“我发了什么 → 服务器收到了什么 → 返回了什么”。
4. 每次只学一个小点，比如“今天只搞懂 GET 带参数”，别一次性全记住，容易晕。

【这个文件里都演示了什么】
- 最简单 GET：只传一个网址过去，看服务器返回什么。
- GET 带参数：给网址后面加 ?key=value 的那种请求。
- 自定义请求头：比如伪装浏览器、带 token 等。
- 响应常用属性：状态码、最终 URL、响应头、文本内容、二进制内容、json() 等。
- 超时和异常处理：网不好时怎么避免程序一直卡着，怎么优雅打印错误。
- cookies：模拟浏览器那种“登录一次，后面自动携带登录状态”。
- Session：在多次请求之间“复用”连接和 cookies。
- POST 表单：传统网页登录表单那种请求方式。
- POST JSON：现在大部分接口都用的方式。
- 上传文件：上传头像、附件之类的场景。
- 其它 HTTP 方法：PUT / DELETE 等 REST 接口常用方法。

【关于 httpbin 网站】
- 我们统一使用 `https://httpbin.org` 这个专门用来练习 HTTP 的测试网站。
- 你发什么参数、请求头、cookies 给它，它就会原样再“回显”给你，方便你确认自己到底发出去的是什么。
"""

import json  # 用于演示手动处理 json
import requests  # 第三方 HTTP 库，需要先：pip install requests
from requests import RequestException  # requests 的异常基类


def basic_get():
    """
    最基础的 GET 请求

    场景（真实世界类比）：
    - 就像你在浏览器地址栏里直接输入一个网址，然后按回车。
    - 浏览器会帮你发一个“最普通的 GET 请求”，把网页内容拿回来展示给你。

    在代码里，我们做的事情是：
    1. 准备一个网址（url 字符串）。
    2. 用 requests.get(url) 把这个网址“访问”一下。
    3. 把服务器返回的“状态码、最终地址、部分头信息、正文内容”打印出来。

    关键点：
    - 这里只传了 url，没有额外参数（params）和请求头（headers），属于最简版用法。
    - 通过这个例子，你要认识 Response 对象上最常用的这几个属性：
      - status_code：请求结果是否成功的“信号灯”。
      - url：最终访问到的真实地址（有时会被重定向）。
      - headers：服务器返回的一些“元信息”（比如返回的是 JSON 还是 HTML）。
      - text：服务器返回的“正文内容”（已经帮你解码成字符串）。
    """
    url = "https://httpbin.org/get"
    # 要请求的目标地址（一个字符串）；httpbin 的 /get 接口会把你发过去的信息原样返回，方便你查看自己到底发了什么。

    resp = requests.get(url)
    # 用 requests.get() 发送一个最普通的 GET 请求，只传 url；函数会帮你连服务器、发请求，并把服务器的响应封装成 resp 对象返回。

    print("【basic_get】")
    # 打印一个小标题，方便你在控制台里区分是哪个示例函数的输出。

    print("状态码：", resp.status_code)
    # 打印 HTTP 状态码；200 表示成功，404 表示网址不存在，500 表示服务器内部错误等。

    print("最终请求的 URL：", resp.url)
    # 打印服务器最终看到的 URL；如果发生了重定向（跳转），这里显示的是跳转之后的真实地址。

    print("部分响应头：", resp.headers.get("Content-Type"))
    # 打印响应头里 Content-Type 这一项；它告诉你服务器返回的数据类型是 JSON、HTML 还是其它格式。

    print("文本响应正文前 100 个字符：", resp.text[:100])
    # 打印响应正文（页面/数据内容）前 100 个字符；resp.text 是把服务器返回的字节数据按编码（通常是 utf-8）解码后的字符串。

    print("-" * 60)
    # 打印一条分隔线，让不同示例的输出在控制台里更容易区分。


def get_with_params():
    """
    GET 携带查询参数（?key=value）

    场景（真实世界类比）：
    - 你在网站上“搜索商品”、“按条件筛选数据”、“翻页查看下一页列表”时，
      浏览器其实会在网址后面加上一堆 ?key=value&key2=value2 这样的内容。

    在代码里，我们做的事情是：
    1. 把这些“搜索条件 / 分页参数”放进一个 Python 字典里。
    2. 把这个字典通过 params= 传给 requests.get()。
    3. requests 会自动帮你把字典转成查询字符串拼到 URL 后面。

    关键点：
    - params 参数一定是一个“普通的 Python 字典”。
    - 最终实际访问的 URL 可以通过 resp.url 看到，非常直观。
    """
    url = "https://httpbin.org/get"
    # 还是使用 httpbin 的 /get 接口；这一次我们会往里面加查询参数（?key=value 的那种）。

    params = {
        "name": "侯金双",
        "city": "广东",
        "page": 1,
        "size": 10,
    }
    # 定义一个字典，里面放要拼到 URL 后面的查询参数；键是参数名，值是参数值（包括中文和数字，requests 会自动帮你转成字符串并做 URL 编码）。

    resp = requests.get(url, params=params)
    # 发送 GET 请求，这次额外传入 params=params；requests 会自动把这个字典转成 ?name=...&city=... 这样的查询字符串拼到 URL 后面。

    print("【get_with_params】")
    # 打印一个小标题，标记这是“GET 带参数”的示例输出。

    print("最终 URL：", resp.url)
    # 打印最终访问的完整 URL；你会看到类似 https://httpbin.org/get?name=...&city=...&page=1&size=10 这样的结果。

    print("JSON 形式返回的数据：", resp.json())
    # 打印服务器返回的 JSON 数据（已经被 .json() 解析成 Python 对象）；httpbin 会把它解析到 args 字段里，你可以展开看看里面的参数是否和你发的一致。

    print("-" * 60)
    # 打印分隔线，方便和其他示例区分。


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
    - 真实开发中，网络情况不稳定，有时候接口半天不返回。
    - 如果你不设置超时，程序可能会一直等，感觉像“卡死了”。
    - 所以我们要：
      1. 给请求设置一个“最长等待时间”（timeout）。
      2. 如果超时或其它错误发生，用 try/except 把它优雅地捕获并打印出来。
    """
    # /delay/3：httpbin 提供的一个接口，会故意延迟 3 秒再返回响应
    url = "https://httpbin.org/delay/3"

    try:
        # timeout=1 表示：
        # - 最多只愿意为这次请求等待 1 秒钟。
        # - 如果 1 秒内没连上 / 没拿到响应，就会抛出 requests.Timeout 异常。
        # 注意：timeout 控制的其实是“连接 + 读取”的时间，而不是程序总运行时间。
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
    session.get("https://httpbin.org/cookies/set?token=hjs")

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
    # .get 其实是 dict 的方法，这里常见用法是传 key，比如 json_data.get("form")
    # 不传参数的话，等价于 json_data.get(None)，通常没有意义
    # 所以应该指定 key，例如 "form"，如下：
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
        "skills": ["足球", "游戏"],  # 列表字段
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
    # 上传自己本地的文件，然后请求回来
    file_path = "study_cursor/我爱你.txt"
    # "rb" 是 read binary 的缩写，表示以二进制模式读取文件
    # 打开指定路径的文件（以二进制模式），这样可以实现类似“上传附件”功能
    with open(file_path, "rb") as f:
        # files 是 requests 上传文件时推荐的参数格式
        # files 字典的 key 是表单字段名，这里假设叫 "file"
        # value 是一个元组，含义依次为：文件名、文件内容（二进制）、文件类型(MIME)
        files = {
            "file": (file_path, f, "text/plain"),
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
    get_with_params()
    get_with_headers()
    response_common_attrs()
    get_timeout_and_error()
    get_with_cookies()
    use_session()
    post_form_data()
    post_json_data()
    file_upload_example()
    other_http_methods()


if __name__ == "__main__":
    # 运行 main()，依次演示上面所有函数的效果
    # 如果你只想看某一个功能，可以临时注释掉其他函数调用
    main()