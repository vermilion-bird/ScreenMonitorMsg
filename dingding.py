import requests

# WebHook = "https://oapi.dingtalk.com/robot/send?access_token=69d636b422630af6c885c0af614633136ce761aa8c711a9f58b4f6e0436f9649"

import time
import hmac
import hashlib
import base64
import urllib.parse


# 加签
def get_url():
    timestamp = str(round(time.time() * 1000))
    secret = 'SECec415108aafafc268441f5e0be082a6178008492b63c44152105396750cb875b'
    token = '69d636b422630af6c885c0af614633136ce761aa8c711a9f58b4f6e0436f9649'
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
            text= f"**主机名:** {host_name} </br> **时间:** {today_time_str} </br> **图片:** ![]({image_url})"
        else:
            text=f"**主机名:** {host_name} </br> **时间:** {today_time_str} </br> 图片上传失败"
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"截图",
                "text":text
                    }
            }
    return data


def send_dingding_message(image_url, host_name, today_time_str):
    webhook = get_url()
    header = {"Content-Type": "application/json", "Charset": "UTF-8"}
    data = decorate_message('markdown', image_url, host_name, today_time_str)
    r = requests.post(webhook, headers=header, json=data, verify=False)
    return r.text


if __name__ == "__main__":
    pass