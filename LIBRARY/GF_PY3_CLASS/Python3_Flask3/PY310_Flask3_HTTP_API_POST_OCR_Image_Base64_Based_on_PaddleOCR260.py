# PY310_Flask3_HTTP_API_POST_OCR_Image_Base64_Based_on_PaddleOCR260.py
# Memo: Python 3 Flask 3 HTTP API POST OCR Image Base64 Based on PaddleOCR 2.6.0
# Create by GF 2025-12-22 15:13

import base64
import io
import pathlib
# ..................................................
import flask  # Flask 3.1.2
import numpy  # NumPy 1.26.4
# ..................................................
from paddleocr import PaddleOCR  # PaddleOCR >= 2.6.0, PaddlePaddle >= 2.2.0
from PIL       import Image      # Pillow 11.1.0

# ##################################################

app = flask.Flask(__name__)
app.json.ensure_ascii = False  # JSON 输出配置: 保留原始字符, 而不是转义成 \uXXXX 形式的 ASCII 字符。
app.json.mimetype = "application/json; charset=utf-8"

# ##################################################
# 工具函数

def Image_File_Encode_to_Base64(Image_Path:str, Image_Extension:str = "auto") -> str:

    # Requirements:
    # - base64 (Python 3.10.6 Included)
    # - pathlib (Python 3.10.6 Included)

    Image_Extension_Auto:str = pathlib.Path(Image_Path).suffix
    Image_File               = open(Image_Path, "rb")
    Image_Encoded:str        = base64.b64encode(Image_File.read()).decode("utf-8")
    Image_Encoded_Prefix:str = ''
    Image_File.close()
    # ..............................................
    if (Image_Extension != "auto"):
        Image_Extension_Auto = Image_Extension
    # ..............................................
    if (Image_Extension_Auto == ".bmp"):
        Image_Encoded_Prefix = "data:image/bmp;base64,"
    # ..............................................
    if (Image_Extension_Auto == ".gif"):
        Image_Encoded_Prefix = "data:image/gif;base64,"
    # ..............................................
    if (Image_Extension_Auto == ".jpg"):
        Image_Encoded_Prefix = "data:image/jpeg;base64,"
    # ..............................................
    if (Image_Extension_Auto == ".jpeg"):
        Image_Encoded_Prefix = "data:image/jpeg;base64,"
    # ..............................................
    if (Image_Extension_Auto == ".png"):
        Image_Encoded_Prefix = "data:image/png;base64,"
    # ..............................................
    if (Image_Extension_Auto == ".webp"):
        Image_Encoded_Prefix = "data:image/webp;base64,"
    # ..............................................
    return "%s%s" % (Image_Encoded_Prefix, Image_Encoded)

def Image_Base64_to_NDArray(Image_Base64:str):

    # NumPy ndarray Explain: ndarray 这个名字是 "n-dimensional array" (N 维数组) 的缩写。
    # Requirements:
    # - base64 (Python 3.10.6 Included)
    # - io (Python 3.10.6 Included)
    # - NumPy 1.26.4
    # - Pillow 11.1.0
    # Example:
    # >>> Image_Base64 = "/9j/4AAQSkZJRgABAQ...(图片的 Base64 编码字符串)...ACAkCMK//Z"
    # >>> Image_NDArray = Image_Base64_to_NDArray(Image_Base64)
    # >>> print(Image_NDArray)
    # array([[[ 67, 146, 213],
    #         [ 67, 146, 213],
    #         [ 67, 146, 213],
    #         ...,
    #         [ 67, 150, 216],
    #         [ 67, 150, 216],
    #         [ 67, 150, 216]],
    # 
    #        ...,
    # 
    #        [[ 40, 108, 179],
    #         [ 40, 108, 179],
    #         [ 40, 108, 179],
    #         ...,
    #         [ 65, 152, 221],
    #         [ 65, 152, 221],
    #         [ 64, 151, 220]]], dtype=uint8)

    if (',' in Image_Base64):  # 移除 "data:image/png;base64," 前缀
        Image_Base64_Splited:list = Image_Base64.split(',')
        Image_Base64              = Image_Base64_Splited[1]
    # ..............................................
    Image_Bytes:bytes = base64.b64decode(Image_Base64) # Base64 解码。
    # ..............................................
    PIL_Image_Object = Image.open(io.BytesIO(Image_Bytes))  # 转换为 PIL Image 对象。
    # ..............................................
    Image_NDArray = numpy.array(PIL_Image_Object)  # 转换为 NumPy ndarray 数组。
    # ..............................................
    return Image_NDArray

# ##################################################

PaddleOCR260 = PaddleOCR(show_log = False, use_angle_cls = True, lang = "ch", use_gpu = False)  # 初始化 OCR 引擎。

# ##################################################

@app.route("/paddleocr/image/base64", methods = ['POST'])
def PY310_Flask3_HTTP_API_POST_OCR_Image_Base64_Based_on_PaddleOCR260():

    # 输入示例:
    # {
    #     "images": [
    #         "/9j/4AAQSkZJRgABAQ......ACAkCMK//Z",
    #         "/0A/ARCAaqBP8DSafd......KzRmJ8M//A",
    #         ......
    #     ]
    # }
    # 字段说明:
    # - 字段 "images" (array 类型): 包含图片的 Base64 编码字符串, 注意: 图片的 Base64 编码字符串不包含 "data:image/png;base64," 前缀。
    # ..............................................
    # 输出示例:
    # {
    #     "data": [
    #         {
    #             "imageIndex": 1,
    #             "text": "D056746......退票改签时须交回车站",
    #             "confidence": 0.99,
    #             "position": [[137.0, 136.0], [364.0, 126.0], [366.0, 173.0], [140.0, 184.0]]
    #         },
    #         ......
    #     ]
    # }
    # 字段说明:
    # - 字段 "data" -> 0 -> "text"       (string 类型): OCR 识别出的文字内容。
    # - 字段 "data" -> 0 -> "confidence" (number 类型): 置信度。
    # - 字段 "data" -> 0 -> "position"   (array  类型): 文字区域 box 的 4 个顶点坐标。

    VALID_KEYS:list = ["0123abcdefghijklmnopqrstuvwxyz0123456789"] 

    Request_Key:str = flask.request.headers.get("Authorization", "")  # 从请求头获取 API Key
    Request_Key     = Request_Key.replace("token ", '')
    Request_Key     = Request_Key.replace("Bearer ", '')

    if (Request_Key not in VALID_KEYS):
        return flask.jsonify({"error":   "Invalid credentials for PaddleOCR image recognition tool",
                              "message": "Invalid key"}), 401

    images:list = flask.request.json.get("images", [])

    output:list = []

    imageIndex:int = 0
    while (imageIndex < len(images)):
        Image_Base64  = images[imageIndex]
        Image_NDArray = Image_Base64_to_NDArray(Image_Base64)
        # PaddleOCR 识别
        # - 参数 cls = True 表示使用方向分类
        # ..........................................
        # PaddleOCR260Results 内容示例 (以识别火车票为例):
        # >>> print(PaddleOCR260Results)
        # [[[[[137.0, 136.0], [364.0, 126.0], [366.0, 173.0], [140.0, 184.0]],
        #    ('D056746', 0.9844202399253845)],
        #   [[[730.0, 149.0], [990.0, 149.0], [990.0, 211.0], [730.0, 211.0]],
        #    ('成都南站', 0.9963602423667908)],
        #   [[[168.0, 170.0], [430.0, 157.0], [433.0, 214.0], [171.0, 226.0]],
        #    ('眉山站', 0.9826920628547668)],
        # 
        # ...,
        # 
        #   [[[338.0, 1299.0], [657.0, 1292.0], [658.0, 1334.0], [339.0, 1342.0]],
        #    ('报销凭证 遗失不补', 0.9538708925247192)],
        #   [[[307.0, 1351.0], [688.0, 1343.0], [689.0, 1384.0], [308.0, 1392.0]],
        #    ('退票改签时须交回车站', 0.9913343191146851)],
        #   [[[134.0, 1422.0], [634.0, 1414.0], [634.0, 1455.0], [135.0, 1463.0]],
        #    ('32208320030505D056747JM', 0.9965883493423462)]]]
        PaddleOCR260Results:list = PaddleOCR260.ocr(Image_NDArray, cls = True)
        # ..........................................
        i:int = 0
        while (i < len(PaddleOCR260Results[0])):
            output.append({"imageIndex": imageIndex,
                           "text":       PaddleOCR260Results[0][i][1][0],
                           "confidence": float(PaddleOCR260Results[0][i][1][1]),
                           "position":   PaddleOCR260Results[0][i][0]})
            # ......................................
            i = i + 1
        # ..........................................
        imageIndex = imageIndex + 1

    return flask.jsonify({"data": output}), 200

# ##################################################

if __name__ == "__main__":

    app.run(debug = True, port = 5000)

# EOF Signed by GF.
