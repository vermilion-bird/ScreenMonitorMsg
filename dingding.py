import requests

# WebHook = "https://oapi.dingtalk.com/robot/send?access_token=69d636b422630af6c885c0af614633136ce761aa8c711a9f58b4f6e0436f9649"

import time
import hmac
import hashlib
import base64
import urllib.parse


# 加签
def get_url(token, secret):
    timestamp = str(round(time.time() * 1000))
    # secret = 'SECec415108aafafc268441f5e0be082a6178008492b63c44152105396750cb875b'
    # token = '69d636b422630af6c885c0af614633136ce761aa8c711a9f58b4f6e0436f9649'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc,
                         string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    webhook = f"https://oapi.dingtalk.com/robot/send?access_token={token}&timestamp={timestamp}&sign={sign}"
    return webhook


def decorate_message(msg_type, image_url, host_name, today_time_str):
    if msg_type == 'markdown':
        text=''
        if image_url :
            text= f"**录井队: ** {host_name} </br> **时间:** {today_time_str} </br> **图片:** ![]({image_url})"
        else:
            text=f"**录井队: ** {host_name} </br> **时间:** {today_time_str} </br> 图片上传失败"
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"截图",
                "text":text
                    }
            }
    return data


def send_dingding_message(image_url, host_name, today_time_str, token, secret):
    webhook = get_url(token, secret)
    header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    data = decorate_message('markdown', image_url, host_name, today_time_str)
    r = requests.post(webhook, headers=header, json=data, verify=False)
    return r.json()

def send_dingding_text_message(text, token, secret):
    webhook = get_url(token, secret)
    header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        }
    }
    r = requests.post(webhook, headers=header, json=data, verify=False)
    return r.json()

if __name__ == "__main__":
    pass
    # secret = 'SEC6fa66b7cacf24b1ff84dc1c3a5b68a213a3fc24cefc3efa06549513b78cd2dda'
    # token = '92562e13c1d0857b459ca932f989e5255cb7264092902aaa6f9997880b878db8'
    # send_dingding_text_message('AAAA', token, secret)

