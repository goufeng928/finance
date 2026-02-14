# PY310_Flask3_HTTP_API_POST_Simulate_PPOCRv5_Based_on_PaddleOCR260.py
# Memo: Python 3 Flask 3 HTTP API POST Simulate PP-OCRv5 2.6.0 Based on PaddleOCR 2.6.0
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

@app.route("/pp/ocr/v5", methods = ['POST'])
def PY310_Flask3_HTTP_API_POST_Simulate_PPOCRv5_Based_on_PaddleOCR260():

    # 输入示例:
    # {
    #     "file": "/9j/4AAQSkZJRgABAQ......ACAkCMK//Z",
    #     "fileType": 1,
    #     "useDocOrientationClassify": false,
    #     "useDocUnwarping": false,
    #     "useTextlineOrientation": false
    # }
    # 字段说明:
    # - 字段 "images"   (array  类型): 文件的 Base64 编码字符串, 注意: 文件的 Base64 编码字符串不包含 "data:image/png;base64," 前缀。
    # - 字段 "fileType" (number 类型): 0: PDF | 1: 图片。
    # ..............................................
    # 输出示例:
    # {
    #     "result": {
    #         "ocrResults": [
    #             {
    #                 "prunedResult": "D056746......退票改签时须交回车站",
    #                 "confidence": 0.99,
    #                 "box": [[137.0, 136.0], [364.0, 126.0], [366.0, 173.0], [140.0, 184.0]],
    #                 "ocrImage": ''
    #             }
    #         ]
    #     }
    # }
    # 字段说明:
    # - 字段 "result" -> "ocrResults" -> 0 -> "prunedResult" (string 类型): OCR 识别出的文字内容。
    # - 字段 "result" -> "ocrResults" -> 0 -> "confidence"   (number 类型): 置信度。
    # - 字段 "result" -> "ocrResults" -> 0 -> "box"          (array  类型): 文字区域 box 的 4 个顶点坐标。
    # - 字段 "result" -> "ocrResults" -> 0 -> "ocrImage"     (string 类型): 返回带标注的图片 (可选)。

    VALID_KEYS:list = ["0123abcdefghijklmnopqrstuvwxyz0123456789"] 

    Request_Key:str = flask.request.headers.get("Authorization", "")  # 从请求头 "Authorization" 字段获取 API Key
    Request_Key = Request_Key.replace("token ", '')  # 移除 "token " 前缀 (官方示例为 "token 99efa......7cb47")
    Request_Key = Request_Key.replace("Bearer ", '')

    if (Request_Key not in VALID_KEYS):
        return flask.jsonify({"error":   "Invalid credentials for TextRecognitionTool",
                              "message": "Invalid token"}), 401

    # ----------------------------------------------

    # 验证请求类型 (支持 JSON 数据)
    if (flask.request.is_json != True):
        return flask.jsonify({"error": "Content-Type must be application/json"}), 400

    # ----------------------------------------------

    fileBase64:str = flask.request.json.get("file", '')
    fileType:int = flask.request.json.get("fileType", (-1))  # {0: "PDF", 1: "图片"}

    # 验证请求字段
    if (fileBase64 == ''):
        return flask.jsonify({"error": "Missing required field: file"}), 400
    if (fileType == ''):
        return flask.jsonify({"error": "Missing required field: fileType"}), 400

    # ----------------------------------------------

    # 验证文件类型
    if (fileType != 0 and fileType != 1):
        return flask.jsonify({"error": "For PDF documents, set \"fileType\" to 0; for images, set \"fileType\" to 1",
                              "result": {"ocrResults": []}}), 200

    # ----------------------------------------------

    ocrResults:list = []

    Image_NDArray = Image_Base64_to_NDArray(fileBase64)
    PaddleOCR260Results:list = PaddleOCR260.ocr(Image_NDArray, cls = True)
    # ..........................................
    i:int = 0
    while (i < len(PaddleOCR260Results[0])):
        ocrResults.append({"prunedResult": PaddleOCR260Results[0][i][1][0],
                           "confidence":   float(PaddleOCR260Results[0][i][1][1]),
                           "box":          PaddleOCR260Results[0][i][0]})
        # ......................................
        i = i + 1

    # ----------------------------------------------

    return flask.jsonify({"result": {"ocrResults": ocrResults}}), 200

# ##################################################

if __name__ == "__main__":

    app.run(debug = True, port = 5000)

# EOF Signed by GF.
