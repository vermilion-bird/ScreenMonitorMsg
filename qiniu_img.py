#!/usr/bin/python
# -*- coding: utf-8 -*-
import qiniu
import re

#替换为自己的ak和sk
access_key = "hk9Ua94zfqbMUiLi3eOXpjeM-tdpSmRqfN8HV2O_"
secret_key = "OJUT7pzkOOskrYzEp22a4h7MqPpckU33gwaQRm7H"
#替换为自己的域名
url = 'qn.top1.pub'
#替换为自己的仓库名
bucket_name = 'image'
q = qiniu.Auth(access_key, secret_key)

#图片返回地址，http或者https由自己来决定
def qiniu_upload(key, localfile):
    key_ini = str(re.findall(r'[^\\/:*?"<>|\r\n]+$', key))
    key = key_ini.strip("['").strip("']")
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = qiniu.put_file(token, key, localfile)
    if ret:
        return f"http://{url}/{ret['key']}"
    else:
        print('上传失败，请重试')
        return None

if __name__ == '__main__':
    pass