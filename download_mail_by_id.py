import requests
import re
import json
import os

import email
from email.message import EmailMessage

def get_download_mail_url(cookies, permmsgid):

    url = f'https://mail.google.com/mail/u/0/?ik=xxxxxx&view=att&permmsgid={permmsgid}&disp=comp&safe=1'
    headers = {
        'Host': 'mail.google.com',
        'Cookie': f'{cookies}'
    }

    response = requests.get(url, headers=headers,allow_redirects=False)

    if response.status_code == 302:
        location_header = response.headers.get('Location')
        print('Location:', location_header)
        return location_header
    else:
        print('Failed to retrieve data:', response.status_code)


def download_eml(url,filepath):
    filepath = f"{filepath[10:]}.eml"
    print(filepath)
    try:
        # 发送GET请求获取eml文件内容
        response = requests.get(url, stream=True)

        # 确认请求成功
        if response.status_code == 200:
            # 获取当前脚本所在目录
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # 创建一个名为eml_files的文件夹（如果不存在）
            save_folder = os.path.join(script_dir, 'eml_files')
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)

            # 拼接保存文件的完整路径
            save_path = os.path.join(save_folder, filepath)

            # 打开文件并保存响应内容
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Eml文件已下载到：{save_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"下载出错：{e}")

if __name__ == '__main__':

    cookies_str2 = "SSID=xxxxxx;HSID=xxxxxxxx;__Secure-1PSIDTS=xxxxxxxxxx;SID=xxxxxxxxxxxx;OSID=xxxxxxxxxxxxx;"
    with open('mail_id.txt', 'r') as f:
        mail_ids = [line.strip() for line in f.readlines()]
    for mail_id in mail_ids:
        url = get_download_mail_url(cookies_str2,mail_id)
        download_eml(url,mail_id)
