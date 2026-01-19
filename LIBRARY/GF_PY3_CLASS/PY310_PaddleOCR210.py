# GF_PY3_CLASS/PY310_PaddleOCR210.py
# Create by GF 2025-09-19 16:53

import fitz  # PyMuPDF 1.25.5
import numpy
# ..................................................
from paddleocr import PaddleOCR  # PaddleOCR 2.10.0, PaddlePaddle 3.0.0, Torch 2.6.0, TorchVision 0.21.0

# ##################################################

class Python_3_PaddleOCR_2_10(object):

    def File_to_Text(self, File_Path:str, DPI:int = 300) -> str:

        Result_Text:str = str('')
        # ..........................................
        if (".pdf" in File_Path.lower()): Result_Text = self.PDF_to_Text(PDF_Path = File_Path, DPI = DPI)
        if (".png" in File_Path.lower()): Result_Text = self.PNG_to_Text(PNG_Path = File_Path, DPI = DPI)
        if (".jpg" in File_Path.lower()): Result_Text = self.JPG_to_Text(JPG_Path = File_Path, DPI = DPI)
        # ..........................................
        return Result_Text

    def PNG_to_Text(self, PNG_Path:str, DPI:int = 300) -> str:

        PNG_Text:str = str('')
        # ..........................................
        # 初始化 OCR 引擎
        OCR = PaddleOCR(show_log = False, use_angle_cls = True, lang = 'ch', use_gpu = False)
        # ..........................................
        # PaddleOCR 识别
        # - 参数 cls = True 表示使用方向分类
        OCR_Result:list = OCR.ocr(PNG_Path, cls = True)
        # ..........................................
        # OCR_Result 内容示例 (以识别火车票为例):
        # >>> print(OCR_Result)
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
        # ..........................................
        # 提取文本并拼接
        if (OCR_Result and OCR_Result[0]):
            Text_for_Recognized_List:list = []
            # ......................................
            i:int = 0
            while (i < len(OCR_Result[0])):
                Text_for_Recognized:str = OCR_Result[0][i][1][0]
                Text_for_Recognized_List.append(Text_for_Recognized)
                i = i + 1
            # ......................................
            PNG_Text = str('\n').join(Text_for_Recognized_List)
        # ..........................................
        return PNG_Text

    def JPG_to_Text(self, JPG_Path:str, DPI:int = 300) -> str:

        JPG_Text:str = self.PNG_to_Text(PNG_Path = JPG_Path, DPI = DPI)
        # ..........................................
        return JPG_Text

    def PDF_to_Text(self, PDF_Path:str, DPI:int = 300) -> str:

        PDF_Text:str = str('')

        # 初始化 OCR 引擎
        ocr = PaddleOCR(show_log = False, use_angle_cls = True, lang = 'ch', use_gpu = False)

        # 打开 PDF 文件
        PDF_File = fitz.open(PDF_Path)

        for page_num in range(len(PDF_File)):

            # 获取页面并渲染为图像
            page = PDF_File.load_page(page_num)
            mat  = fitz.Matrix(DPI / 72, DPI / 72)
            pix  = page.get_pixmap(matrix = mat)

            # 将图像转换为 NumPy 数组
            img_np = numpy.frombuffer(pix.samples, dtype = numpy.uint8).reshape(pix.h, pix.w, pix.n)

            # PaddleOCR 识别
            OCR_Result = ocr.ocr(img_np, cls = True)

            # 提取文本并拼接
            if (OCR_Result and OCR_Result[0]):
                Page_Text = str('\n').join( [Line_Text[1][0] for Line_Text in OCR_Result[0]] )
                PDF_Text = PDF_Text + f"Page Number {page_num}:\n{Page_Text}\n\n"

        PDF_File.close()

        return PDF_Text

# Signed by
