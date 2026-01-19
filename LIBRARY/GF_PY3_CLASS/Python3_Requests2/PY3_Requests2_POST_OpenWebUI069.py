# GF_PY3_CLASS/Python3_Requests2/PY3_Requests2_POST_OpenWebUI069.py
# Create by GF 2025-12-26 14:13

import base64
import pathlib
# ..................................................
import requests

# ##################################################

class PY3_Requests2_POST_OpenWebUI069():

    def __init__(self):

        self.Pub_Host:str = "127.0.0.1"
        self.Pub_Port:str = "3000"

    def Read_Image_File_Encode_to_Base64(self, Image_File_Path:str, Specified_Image_Extension:str = '') -> str:

        Image_Extension:str      = pathlib.Path(Image_File_Path).suffix
        Image_File               = open(Image_File_Path, "rb")
        Image_Encoded:str        = base64.b64encode(Image_File.read()).decode("utf-8")
        Image_Encoded_Prefix:str = ''
        Image_File.close()
        # ..........................................
        if (Image_Extension == ".bmp"):
            Image_Encoded_Prefix = "data:image/bmp;base64,"
        # ..........................................
        if (Image_Extension == ".gif"):
            Image_Encoded_Prefix = "data:image/gif;base64,"
        # ..........................................
        if (Image_Extension == ".jpg"):
            Image_Encoded_Prefix = "data:image/jpeg;base64,"
        # ..........................................
        if (Image_Extension == ".jpeg"):
            Image_Encoded_Prefix = "data:image/jpeg;base64,"
        # ..........................................
        if (Image_Extension == ".png"):
            Image_Encoded_Prefix = "data:image/png;base64,"
        # ..........................................
        if (Image_Extension == ".webp"):
            Image_Encoded_Prefix = "data:image/webp;base64,"
        # ..........................................
        if (Specified_Image_Extension != ''):
            Image_Extension = Specified_Image_Extension
        # ..........................................
        return "%s%s" % (Image_Encoded_Prefix, Image_Encoded)

    def Round_1_Chat(self, Token:str, Model:str, Message:str) -> str:

        # Requests JSON Data Example:
        # - {"model": "granite3.1-dense:8b", "messages": [{"role": "user", "content": "Please introduce yourself!"}]}

        URL:str       = f"http://{self.Pub_Host}:{self.Pub_Port}/api/chat/completions"
        Headers:dict  = {'Authorization': f'Bearer {Token}', 'Content-Type': 'application/json'}
        Messages:list = [{"role": "user", "content": Message}]
        Data:dict     = {"model": Model, "messages": Messages}
        Response      = requests.post(URL, headers = Headers, json = Data)
        Response_JSON = Response.json()
        # ..........................................
        if (Response_JSON.get("choices", []) == []):
            # Open WebUI 0.6.9 响应出错示例:
            # - {"detail": "400: The decoder prompt (length 12201) is longer than the maximum model length of 819 ..."}
            Response_Text:str = Response_JSON.get("detail", '')
            print(f"[DEBUG] PY3_Requests2_POST_OpenWebUI069.Round_1_Chat: {Response_Text}")
            return Response_Text
        # ..........................................
        if (Response_JSON.get("choices", []) != []):
            Response_Text:str = Response_JSON.get("choices", [])[0].get("message", {}).get("content", '')
            return Response_Text

    def Round_1_Chat_With_Image_Base64(self, Token:str, Model:str, Message:str, Image_Base64:str) -> str:

        # Requests JSON Data Example:
        # - {"model": "granite3.1-dense:8b", "messages": [{"role": "user", "content": "Please introduce yourself!"}]}

        URL:str              = f"http://{self.Pub_Host}:{self.Pub_Port}/api/chat/completions"
        Headers:dict         = {'Authorization': f'Bearer {Token}', 'Content-Type': 'application/json'}
        Message_Content:list = [{"type": "text", "text": Message}, {"type": "image_url", "image_url": {"url": Image_Base64}}]
        Messages:list        = [{"role": "user", "content": Message_Content}]
        Data:dict            = {"model": Model, "messages": Messages}
        Response             = requests.post(URL, headers = Headers, json = Data)
        Response_JSON        = Response.json()
        # ..........................................
        if (Response_JSON.get("choices", []) == []):
            Response_Text:str = Response_JSON.get("detail", '')
            print(f"[DEBUG] PY3_Requests2_POST_OpenWebUI069.Round_1_Chat_With_Image_Base64: {Response_Text}")
            return Response_Text
        # ..........................................
        if (Response_JSON.get("choices", []) != []):
            Response_Text:str = Response_JSON.get("choices", [])[0].get("message", {}).get("content", '')
            return Response_Text

    def Round_1_Chat_With_Image_File(self, Token:str, Model:str, Message:str, Image_File_Path:str, Specified_Image_Extension:str = '') -> str:

        Image_Base64:str = self.Read_Image_File_Encode_to_Base64(Image_File_Path = Image_File_Path, Specified_Image_Extension = Specified_Image_Extension)
        # ..........................................
        Response_Text:str = self.Round_1_Chat_With_Image_Base64(Token = Token, Model = Model, Message = Message, Image_Base64 = Image_Base64)
        # ..........................................
        return Response_Text

# EOF Signed by GF.
