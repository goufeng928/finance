# PY3_Requests2_POST_OpenAI_20250510.py
# Create by GF 2025-12-26 14:13

import base64
import pathlib
# ..................................................
import requests

# ##################################################

class PY3_Requests2_POST_OpenAI_20250510():

    # OpenAI Style URL (20250505):
    # - http://127.0.0.1/v1/chat/completions

    def __init__(self):

        self.Pub_URL:str = "http://127.0.0.1/v1/chat/completions"
        self.Pub_Model:str = "gpt4"
        self.Pub_Key:str = ''

    def Image_File_Encode_to_Base64(self, Image_Path:str, Image_Extension:str = "auto") -> str:

        Image_Extension_Auto:str = pathlib.Path(Image_Path).suffix
        Image_File               = open(Image_Path, "rb")
        Image_Encoded:str        = base64.b64encode(Image_File.read()).decode("utf-8")
        Image_Encoded_Prefix:str = ''
        Image_File.close()
        # ..........................................
        if (Image_Extension != "auto"):
            Image_Extension_Auto = Image_Extension
        # ..........................................
        if (Image_Extension_Auto == ".bmp"):
            Image_Encoded_Prefix = "data:image/bmp;base64,"
        # ..........................................
        if (Image_Extension_Auto == ".gif"):
            Image_Encoded_Prefix = "data:image/gif;base64,"
        # ..........................................
        if (Image_Extension_Auto == ".jpg"):
            Image_Encoded_Prefix = "data:image/jpeg;base64,"
        # ..........................................
        if (Image_Extension_Auto == ".jpeg"):
            Image_Encoded_Prefix = "data:image/jpeg;base64,"
        # ..........................................
        if (Image_Extension_Auto == ".png"):
            Image_Encoded_Prefix = "data:image/png;base64,"
        # ..........................................
        if (Image_Extension_Auto == ".webp"):
            Image_Encoded_Prefix = "data:image/webp;base64,"
        # ..........................................
        return "%s%s" % (Image_Encoded_Prefix, Image_Encoded)

    def Round_1_Chat(self, Message:str) -> str:

        # Requests JSON Data Example:
        # - {"model": "gpt-4", "messages": [{"role": "user", "content": "Please introduce yourself!"}]}

        Headers:dict  = {'Authorization': f'Bearer {self.Pub_Key}', 'Content-Type': 'application/json'}
        Messages:list = [{"role": "user", "content": Message}]
        Data:dict     = {"model": self.Pub_Model, "messages": Messages}
        Response      = requests.post(url = self.Pub_URL, headers = Headers, json = Data)
        Response_JSON = Response.json()
        # ..........................................
        if (Response_JSON.get("choices", []) == []):
            # OpenAI Style 响应出错示例 (20250505):
            # - {'error': {'message': 'invalid param model:gpt-4x (sid: cha000b9019@dx196bacca051b8f2532)',
            # -            'type': 'invalid_request_error',
            # -            'param': None,
            # -            'code': '10005'}}
            Response_Text:str = Response_JSON.get("error", {}).get("message", '')
            print(f"[DEBUG] PY3_Requests2_POST_OpenAI_20250510.Round_1_Chat: {Response_Text}")
            return Response_Text
        # ..........................................
        if (Response_JSON.get("choices", []) != []):
            Response_Text:str = Response_JSON.get("choices", [])[0].get("message", {}).get("content", '')
            return Response_Text

    def Round_1_Chat_With_Image_Base64(self, Message:str, Image_Base64:str) -> str:

        # Requests JSON Data Example:
        # - {"model": "gpt-4", "messages": [{"role": "user", "content": "Please introduce yourself!"}]}

        Headers:dict         = {'Authorization': f'Bearer {self.Pub_Key}', 'Content-Type': 'application/json'}
        Message_Content:list = [{"type": "text", "text": Message}, {"type": "image_url", "image_url": {"url": Image_Base64}}]
        Messages:list        = [{"role": "user", "content": Message_Content}]
        Data:dict            = {"model": self.Pub_Model, "messages": Messages}
        Response             = requests.post(url = self.Pub_URL, headers = Headers, json = Data)
        Response_JSON        = Response.json()
        # ..........................................
        if (Response_JSON.get("choices", []) == []):
            Response_Text:str = Response_JSON.get("error", {}).get("message", '')
            print(f"[DEBUG] PY3_Requests2_POST_OpenAI_20250510.Round_1_Chat_With_Image_Base64: {Response_Text}")
            return Response_Text
        # ..........................................
        if (Response_JSON.get("choices", []) != []):
            Response_Text:str = Response_JSON.get("choices", [])[0].get("message", {}).get("content", '')
            return Response_Text

    def Round_1_Chat_With_Image_File(self, Message:str, Image_Path:str, Image_Extension:str = "auto") -> str:

        Image_Base64:str = self.Image_File_Encode_to_Base64(Image_Path = Image_Path, Image_Extension = Image_Extension)
        # ..........................................
        Response_Text:str = self.Round_1_Chat_With_Image_Base64(Message = Message, Image_Base64 = Image_Base64)
        # ..........................................
        return Response_Text

# EOF Signed by GF.
