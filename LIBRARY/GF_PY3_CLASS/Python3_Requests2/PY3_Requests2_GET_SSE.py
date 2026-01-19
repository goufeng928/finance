# GF_PY3_CLASS/Python3_Requests2/PY3_Requests2_GET_SSE.py
# Create by GF 2025-04-23 23:05

# Python 3 Standard Libraries.
import json
import sys
# ..................................................
import requests  # Requests 2.32.3

# ##################################################

class PY3_Requests2_GET_SSE:

    # Examples:
    # >>> Requests2_GET_SSE = PY3_Requests2_GET_SSE()
    # >>> URL = "http://127.0.0.1:8080/GF_PHP5_SCRIPT_HTTP_Server_GET_SSE.php?stream=true"
    # >>> Requests2_GET_SSE.GET_SSE(URL)
    # [DEBUG] RECEIVING: 63 Char, TOTAL RECEPTION: 225 Char
    # >>> print(Requests2_GET_SSE.Logs)
    # ['[DEBUG] Original Data -> data: {"id": "68ff36f4cdcf5", "content": "How\'s it going?"}',
    #  '[DEBUG] Original Data -> data: {"id": "68ff36f5cddb8", "content": "What have you been up to?"}',
    #  '[DEBUG] Original Data -> data: {"id": "68ff36f6ce014", "content": "Long time no see!"}',
    #  '[DEBUG] Original Data -> data: {"id": "68ff36f7ce2ae", "content": "It\'s great to see you again."}',
    #  '[DEBUG] Original Data -> event: end']
    # >>> print(Requests2_GET_SSE.JSON_Records)
    # [{'id': '68ff36f4cdcf5', 'content': "How's it going?"},
    #  {'id': '68ff36f5cddb8', 'content': 'What have you been up to?'},
    #  {'id': '68ff36f6ce014', 'content': 'Long time no see!'},
    #  {'id': '68ff36f7ce2ae', 'content': "It's great to see you again."}]

    def __init__(self):

        self.Logs:list = []
        self.JSON_Records:list = []

    def Process_Message(self, Message:str) -> int:

        Processed_Message = json.loads(Message)  # 解析 JSON 数据
        # ..........................................
        self.JSON_Records.append(Processed_Message)
        # ..........................................
        return 1

    def GET_SSE(self, URL:str) -> int:

        self.Logs.clear()
        self.JSON_Records.clear()
        # ..........................................
        Headers:dict = {
            "Accept":        "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection":    "keep-alive"
        }
        # ..........................................
        Response = requests.get(URL, headers = Headers, stream = True, timeout = None)
        # ..........................................
        Char_Total:int = 0
        # ..........................................
        for Line in Response.iter_lines(decode_unicode = True):
            if (not Line):  # 跳过空行 (空行也表示事件结束)
                continue
            # ......................................
            self.Logs.append(f"[DEBUG] Original Data -> {Line}")
            # ......................................
            try:
                if (Line.startswith("data: ") == True):
                    Message:str = Line[6:]  # 移除 "data: " 前缀
                    Message:str = Message.strip()  # 去除首尾空白
                    # ..............................
                    if (not Message or Message == "[DONE]"):
                        break  # 收到结束消息后停止接收
                    # ..............................
                    self.Process_Message(Message)
                    # ..............................
                    Char_Count:int = len(Message)
                    Char_Total     = Char_Total + Char_Count
                    sys.stdout.write(f"""\r[DEBUG] RECEIVING: {Char_Count} Char, TOTAL RECEPTION: {Char_Total} Char""")
                    sys.stdout.flush()
                # ..................................
                if (Line.startswith("event: ") == True):
                    Message:str = Line[7:]  # 移除 "event: " 前缀
                    Message:str = Message.strip()  # 去除首尾空白
                    # ..............................
                    if (Message == "end"):
                        break  # 收到结束事件后停止接收
            except json.JSONDecodeError:
                self.Logs.append(f"[DEBUG] JSON parsing error: {Message}")
        # ..........................................
        return Char_Total

# EOF Signed by GF.
