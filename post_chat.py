# -*- encoding:utf-8 -*-
# ==============================================
# Created on 
# Author: 王高亮
# Description:
# Time: 2021/8/31 4:08
# ==============================================


import requests
import json
import hashlib
import random
import string
import time


def post_chat(app_id, app_key, messages, model, max_tokens, temperature, top_p, stop, presence_penalty, frequency_penalty):
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

    response = requests.post(f'https://aigc-api-trial.hz.netease.com/openai/api/v2/text/chat', headers=headers, data=json.dumps(data))
    return response.json()


