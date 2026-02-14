# proxy_openai_api_202505.py
# Create by GF 2025-05-10 01:34

import json
import re
# ..................................................
import requests

# ##################################################
# OpenAI API Verion: 202505

# GET /v1/models -> Return: If Successful:
# - {'object': 'list',
# -  'data': [{'id': 'qwen-vl-max-2025-04-02',
# -    'object': 'model',
# -    'created': 1744009868,
# -    'owned_by': 'system'},
# -   {'id': 'deepseek-v3',
# -    'object': 'model',
# -    'created': 1740023101,
# -    'owned_by': 'system'},
# -   ......
# -   {'id': 'qwen-plus',
# -    'object': 'model',
# -    'created': 1714377100,
# -    'owned_by': 'system'}]}
#
# POST -> Return: If Successful:
# - {'code': 0,
# -  'message': 'Success',
# -  'sid': 'cha000bc275@dx196bad449ab9a4b532',
# -  'choices': [{'message': {'role': 'assistant', 'content': 'Hello! Is there anything I can help you with?'},
# -               'index': 0}],
# -  'usage': {'prompt_tokens': 1, 'completion_tokens': 7, 'total_tokens': 8}}
#
# POST -> Return: If Error (invalid param):
# - {'error': {'message': 'invalid param model:gpt-4x (sid: cha000b9019@dx196bacca051b8f2532)',
# -            'type': 'invalid_request_error',
# -            'param': None,
# -            'code': '10005'}}
#
# 流式请求 (Stream) 响应成功时返回 text/event-stream 类型:
# OpenAI 202505 的流式响应通常使用 Server-Sent Events (SSE), 即 text/event-stream 类型, 每个数据块以 "data: " 开头, 后跟 JSON 数据, 并以两个换行符结束, 例如: data: {json}\n\n
# - data:{"code":0,"message":"Success","sid":"cha000b000c@dx1905cf38fc8b86d552","id":"cha000b000c@dx1905cf38fc8b86d552","created":1719546385,"choices":[{"delta":{"role":"assistant","content":"Can"},"index":0}]}
# - data:{"code":0,"message":"Success","sid":"cha000b000c@dx1905cf38fc8b86d552","id":"cha000b000c@dx1905cf38fc8b86d552","created":1719546385,"choices":[{"delta":{"role":"assistant","content":" I"},"index":0}]}
# - data:{"code":0,"message":"Success","sid":"cha000b000c@dx1905cf38fc8b86d552","id":"cha000b000c@dx1905cf38fc8b86d552","created":1719546385,"choices":[{"delta":{"role":"assistant","content":" help"},"index":0}]}
# - data:{"code":0,"message":"Success","sid":"cha000b000c@dx1905cf38fc8b86d552","id":"cha000b000c@dx1905cf38fc8b86d552","created":1719546385,"choices":[{"delta":{"role":"assistant","content":" you"},"index":0}]}
# - data:{"code":0,"message":"Success","sid":"cha000b000c@dx1905cf38fc8b86d552","id":"cha000b000c@dx1905cf38fc8b86d552","created":1719546389,"choices":[{"delta":{"role":"assistant","content":""},"index":0}],"usage":{"prompt_tokens":4,"completion_tokens":4,"total_tokens":10}}
# - data:[DONE]

# ##################################################

class set_url:
    
    def __init__(self):
        
        # OpenAI API Verion: 202505
        self.url = "http://127.0.0.1/v1/chat/completions"

    def update(self, url_str:str):

        """ 更新键值对到 url 中 """

        self.url = url_str
        # ..........................................
        return self  # 返回 self 以实现链式调用

class set_headers:
    
    def __init__(self):
        
        # OpenAI API Verion: 202505
        self.headers = {"Authorization": "Bearer please-enter-openai-api-key", "Content-Type": "application/json"}

#   def update(self, key, value):
#
#       """ 更新键值对到 headers 中 """
#
#       self.headers[key] = value
#       # ..........................................
#       return self  # 返回 self 以实现链式调用

    def update(self, *args, **kwargs):

        """ 更新键值对到 headers 中 """
        """ 支持 update(key=value) 和 update({'key': 'value'}) 两种调用方式 """

        if args and isinstance(args[0], dict):
            self.headers.update(args[0])
        # ..........................................
        self.headers.update(kwargs)
        # ..........................................
        return self  # 返回 self 以实现链式调用

# ##################################################

class set_data:
    
    # HTTP 请求目标:
    # - Content-Type: application/x-www-form-urlencoded
    # - http://127.0.0.1/login?username=admin&password=123456
    # CURL 命令:
    # - curl -X POST --data "username=admin&password=123456" http://127.0.0.1/login
    # Python 3 Requests 2 方法:
    # - >>> import requestst
    # - >>> payload = {"username": "admin", "password": "123456"}
    # - >>> response = requests.post("http://127.0.0.1/login", data=payload)
    
    def __init__(self):

        self.data = {"username": "admin", "password": "123456"}

    def update(self, *args, **kwargs):

        """ 更新键值对到 data 中 """
        """ 支持 update(key=value) 和 update({'key': 'value'}) 两种调用方式 """

        if args and isinstance(args[0], dict):
            self.data.update(args[0])
        # ..........................................
        self.data.update(kwargs)
        # ..........................................
        return self  # 返回 self 以实现链式调用

# ##################################################

class set_json:
    
    # HTTP 请求目标:
    # - Content-Type: application/json
    # CURL 命令:
    # - curl -X -H "Content-Type: application/json" POST --data '{"username": "admin", "password": "123456"}' http://127.0.0.1/login
    # - curl -X -H "Content-Type: application/json" POST --data @payload.json http://127.0.0.1/login
    # Python 3 Requests 2 方法:
    # - >>> import requestst
    # - >>> payload = {"username": "admin", "password": "123456"}
    # - >>> response = requests.post("http://127.0.0.1/login", json=payload)
    
    def __init__(self):

        # OpenAI API Verion: 202505
        self.json = {"model": "gpt-4",
                     "messages": [{"role": "user", "content": "can you hear me"}],
                     "stream": False,
                     "temperature": 0.7}  # temperature 值越高, 模型回答越有创意

    def update(self, *args, **kwargs):

        """ 更新键值对到 json 中 """
        """ 支持 update(key=value) 和 update({'key': 'value'}) 两种调用方式 """

        if args and isinstance(args[0], dict):
            self.json.update(args[0])
        # ..........................................
        self.json.update(kwargs)
        # ..........................................
        return self  # 返回 self 以实现链式调用

# ##################################################

class proxy_openai_api(object):

    # Example:
    # - proxy = proxy_openai_api()
    # - proxy.set_header.update({"Content-Type": "application/json"}).update(Authorization = "Bearer token")

    def __init__(self):

        self.url:object     = set_url()
        self.headers:object = set_headers()
        self.json:object    = set_json()
        # ..........................................
#       self.choice:list  = []
#       self.message:dict = {}

    def get(self):

        response = requests.get(url=self.url.url, headers=self.headers.headers)
        # ..........................................
        json_str = response.text
        # ..........................................
        rps_dict = json.loads(json_str)
        # ..........................................
        return rps_dict

    def post(self):

        if (self.json.json["stream"] == True):
            response = requests.post(url=self.url.url, headers=self.headers.headers, json=self.json.json, stream=True)
            # ......................................
            return response.iter_content(chunk_size=None)  # 流式请求 (Stream) 直接返回迭代器
        else:
            response = requests.post(url=self.url.url, headers=self.headers.headers, json=self.json.json, stream=False)
            # ......................................
            json_str = response.text
            # ......................................
            rps_dict = json.loads(json_str)
            # ......................................
            return rps_dict

    def integrate_iter_content(self, iter_content):
    
        iter_line_list = []
        for chunk in iter_content:
            if chunk:
                line = chunk.decode("utf-8")
                # Line be Similar to (20250505):
                # - data: {"choices":[{"finish_reason":null,"delta":{"content":null,"reasoning_content":"Hello"}, ... }
                # - data: {"choices":[{"finish_reason":null,"delta":{"content":null,"reasoning_content":"World"}, ... }
                # - ......
                # - data: [DONE]
                extract_data = re.findall("data:.*", line)
                iter_line_list.extend(extract_data)
    
        iter_dict_list = []
        if (iter_line_list != []):
            for line in iter_line_list:
                if ("[DONE]" not in line and "data:" in line[0:5]):
                    iter_dict_list.append(json.loads(line[5:]))
        
        integeration = {
            "choices": [
                {"delta": {"role": "assistant", "content": None, "reasoning_content": None},
                "index": 0,
                "logprobs": None,
                "finish_reason": None}
            ],
            "object": 'chat.completion.chunk',
            "usage": None,
            "created": 1748350107,
            "system_fingerprint": None,
            "model": "qwen3-32b",
            "id": "chatcmpl-822cad44-8a68-91d4-97eb-d21317a64a26"
        }
        integeration["choices"][0]["delta"]["content"] = ''
        integeration["choices"][0]["delta"]["reasoning_content"] = ''
        for i in range(0, len(iter_dict_list), 1):
            choices_0_delta_content           = iter_dict_list[i]["choices"][0]["delta"]["content"]
            choices_0_delta_reasoning_content = iter_dict_list[i]["choices"][0]["delta"]["reasoning_content"]
            if (choices_0_delta_content           != None):
                integeration["choices"][0]["delta"]["content"] += choices_0_delta_content
            if (choices_0_delta_reasoning_content != None):
                integeration["choices"][0]["delta"]["reasoning_content"] += choices_0_delta_reasoning_content
    
        return integeration

# Signed by GF.
