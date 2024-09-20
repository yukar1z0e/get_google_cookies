import requests
import re
import json

import email
from email.message import EmailMessage
import webbrowser

def extract_value(script_content):
    # 定义正则表达式模式
    pattern = r':\["sdpc","([^"]+)"'

    # 搜索匹配的内容
    match = re.search(pattern, script_content)

    # 如果找到匹配的内容，返回提取的值
    if match:
        return match.group(1)
    else:
        return None
def get_xsrf_token(cookies):
    url = 'https://mail.google.com/mail/u/0/?sw=2'
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            text = response.text
            xsrf_token = extract_value(text)
            return xsrf_token

        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")
    return None

def get_gmail_header1(cookies):
    url = 'https://mail.google.com/mail/u/0/?sw=2'
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            return response.headers.get('X-Gmail-Sw-Cache-Current-Version-Token')[9:19]

        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")

    return None
def get_gmail_header2(cookies):
    url = 'https://mail.google.com/mail/u/0/?sw=2'
    try:
        response = requests.get(url, cookies=cookies)
        if response.status_code == 200:
            text = response.text
            pattern = r"GLOBALS=\[null,null,(\d+),"
            matches = re.findall(pattern, text)
            return matches[0]
        else:
            print(f"Request failed with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"Request exception: {e}")
def get_mail_content(cookies, xsrf_token, cd53f91d3d_value, value_646086362):
    print(cookies)
    print(xsrf_token)
    print(cd53f91d3d_value)
    print(value_646086362)
    url = 'https://mail.google.com/sync/u/0/i/bv?hl=en&c=31&rt=r&pt=ji'
    headers = {
        'X-Gmail-Storage-Request': '',
        'X-Framework-Xsrf-Token': f'{xsrf_token}',
        'Sec-Ch-Ua-Mobile': '?0',
        'Content-Type': 'application/json',
        'X-Gmail-Btai': f'[null,null,[1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,"en","",1,1,24,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,0,0,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,0,0,1,1,1,1,100,1,1,0,1,0,1,0,1,0,0,1,1,1,0,0,0,0,0,0],1,"{cd53f91d3d_value}",111,25,"",11,1,"",1,"1",1,null,{value_646086362},"","",11]',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    data = [[49,100,None,"((in:^i ((in:^smartlabel_personal) OR (in:^t))) OR (in:^i -in:^smartlabel_promo -in:^smartlabel_social))",[None,None,None,None,0],"itemlist-ViewType(49)-11",1,2000,None,0,None,None,None,1,None,None,None,None,0],None,[0,5,None,None,1,1,1]]

    response = requests.post(url, cookies=cookies, headers=headers, json=data)

    if response.status_code == 200:
        data = response.text
        ppattern = r'"(msg-[^"]*)"'
        matches = re.findall(pattern, data)
        unique_matches = list(set(matches))
        for match in unique_matches:
            with open('msg_id.txt', 'a') as f:
                f.write(match + '\n')
        return unique_matches
    else:
        print(f"请求失败，状态码：{response.status_code}")

if __name__ == '__main__':
    # cookies_str = input("请输入cookies字符串：")
    cookies_str = "__Secure-3PSID=xxxxxxx;__Secure-1PSIDTS=xxxxxxxxxxxxxxxx;SID=xxxxxxxx;OSID=xxxxxxxxxx;"
    cookies = {}

    # 按分号分割成每个 cookie 部分，然后处理每个部分
    for cookie in cookies_str.split(';'):
        # 如果字符串为空，则跳过
        if not cookie.strip():
            continue
        # 按等号分割成键值对，并去除两边的空格
        key, value = cookie.split('=', 1)
        key = key.strip()
        value = value.strip()
        # 添加到字典中
        cookies[key] = value

    xsrf_token = get_xsrf_token(cookies)
    cd53f91d3d_value = get_gmail_header1(cookies)
    value_646086362 = get_gmail_header2(cookies)
    mail_datas = get_mail_content(cookies, xsrf_token, cd53f91d3d_value, value_646086362)
