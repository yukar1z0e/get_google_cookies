import json
import requests
import websocket

def get_browser_info():
    remote_debugging_url = 'http://127.0.0.1:8091/json/version'
    try:
        response = requests.get(remote_debugging_url)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print("发生错误：", str(e))

def get_page_info():
    remote_debugging_url = 'http://127.0.0.1:8091/json/list'
    try:
        response = requests.get(remote_debugging_url)
        data = json.loads(response.text)
        page_info = []
        for i, page in enumerate(data, start=1):
            page_url = page['url']
            page_title = page['title']
            page_info.append({'id': page['id'], 'url': page_url, 'title': page_title})
            print(f"{i}. {page_title} - {page_url}")
        return page_info
    except Exception as e:
        print("发生错误：", str(e))

def get_storage_info(page_id, storage_type):
    remote_debugging_url = 'http://127.0.0.1:8091/json/list'
    try:
        response = requests.get(remote_debugging_url)
        data = json.loads(response.text)
        target = None
        for page in data:
            if page['id'] == page_id:
                target = page['webSocketDebuggerUrl']
                break
        if target:
            ws = websocket.create_connection(target)
            command = json.dumps({"id": 1, "method": "Runtime.evaluate", "params": {"expression": f"JSON.stringify({storage_type})"}})
            ws.send(command)
            response = ws.recv()
            data = json.loads(response)
            result = data.get('result', {}).get('result', {}).get('value', '')
            storage_info = []
            if result:
                storage_data = json.loads(result)
                for key, value in storage_data.items():
                    storage_info.append({'key': key, 'value': value})
            ws.close()
            return storage_info
    except Exception as e:
        print("发生错误：", str(e))

def get_cookies(page_id):
    remote_debugging_url = 'http://127.0.0.1:8091/json/list'
    try:
        response = requests.get(remote_debugging_url)
        data = json.loads(response.text)
        target = None
        for page in data:
            if page['id'] == page_id:
                target = page['webSocketDebuggerUrl']
                break
        if target:
            ws = websocket.create_connection(target)
            command = json.dumps({"id": 1, "method": "Network.getCookies"})
            ws.send(command)
            response = ws.recv()
            data = json.loads(response)
            cookies = data.get('result', {}).get('cookies', [])
            ws.close()
            return cookies
    except Exception as e:
        print("发生错误：", str(e))

def generate_js_code(storage_info, storage_type):
    js_commands = []
    for item in storage_info:
        if storage_type == 'cookies':
            key = item['name']
            value = item['value']
        else:
            key = item['key']
            value = item['value']
        formatted_key = json.dumps(key)
        formatted_value = json.dumps(value)
        if storage_type == 'cookies':
            js_command = f'document.cookie = {formatted_key} + "=" + {formatted_value} + ";path=/";'
        else:
            js_command = f'{storage_type}.setItem({formatted_key}, {formatted_value});'
        js_commands.append(js_command)
    return js_commands

def print_specific_cookies(cookies):
    specific_cookies = ['OSID', 'SID', 'HSID', 'SSID','__Secure-1PSIDTS']
    for cookie in cookies:
        if cookie['name'] in specific_cookies:
            print(f"{cookie['name']}={cookie['value']};", end='')

pages = get_page_info()

if pages:
    page_index = input("选择要获取本地存储信息的页面编号：")
    page_index = int(page_index) - 1

    if page_index >= 0 and page_index < len(pages):1
        selected_page = pages[page_index]
        page_id = selected_page['id']
        page_url = selected_page['url']

        print(f"选择的页面：{selected_page['title']} - {page_url}")

        local_storage_info = get_storage_info(page_id, "localStorage")
        session_storage_info = get_storage_info(page_id, "sessionStorage")
        cookies_info = get_cookies(page_id)

        if local_storage_info or session_storage_info or cookies_info:
            print("本地存储信息：")
            for item in local_storage_info:
                print("键:", item['key'])
                print("值:", item['value'])
                print()
            print("会话存储信息：")
            for item in session_storage_info:
                print("键:", item['key'])
                print("值:", item['value'])
                print()
            print("Cookies信息：")
            for item in cookies_info:
                print("键:", item['name'])
                print("值:", item['value'])
                print()

            print("复制以下 JavaScript 代码到新浏览器的 console 中：")
            js_code_local = generate_js_code(local_storage_info, "localStorage")
            js_code_session = generate_js_code(session_storage_info, "sessionStorage")
            js_code_cookies = generate_js_code(cookies_info, "cookies")
            print("\n".join(js_code_local))
            print("\n".join(js_code_session))
            print("\n".join(js_code_cookies))

            print("下面是特定的Cookies值：")
            print_specific_cookies(cookies_info)
        else:
            print("无本地存储信息。")
    else:
        print("无效的页面编号。")
else:
    print("没有找到打开的页面。")

print("下面是User-Agent部分\n")
browser_info = get_browser_info()
print("User-Agent是：", browser_info.get('User-Agent', ''))
