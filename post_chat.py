# -*- encoding:utf-8 -*-
# ==============================================
# Created on 
# Author: 王高亮
# Description:
# Time: 2021/8/31 4:08
# ==============================================


import threading
import requests
import json
import hashlib
import random
import string
import time


def post_chat(app_id, app_key, messages, model, max_tokens, temperature, top_p, stop, presence_penalty,
              frequency_penalty, callback):
    nonce = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    timestamp = str(int(time.time()))
    str2sign = f'appId={app_id}&nonce={nonce}&timestamp={timestamp}&appkey={app_key}'
    sign = hashlib.md5(str2sign.encode('utf-8')).hexdigest().upper()

    headers = {
        'sign': sign,
        'nonce': nonce,
        'version': 'v2',
        'appId': app_id,
        'timestamp': timestamp,
        'Content-Type': 'application/json',
    }

    data = {
        'messages': messages,
        'model': model,
        'maxTokens': max_tokens,
        'temperature': temperature,
        'topP': top_p,
        'stop': stop,
        'presencePenalty': presence_penalty,
        'frequencyPenalty': frequency_penalty
    }

    url = f'https://aigc-api-trial.hz.netease.com/openai/api/v2/text/chat'

    # 开启线程调用post请求
    def post_request():
        response = requests.post(url, headers=headers, data=json.dumps(data))
        callback(response.json())

    threading.Thread(target=post_request).start()
