# GF_PY3_CLASS/Python3_Requests2/PY3_Requests2_POST_OpenWebUI069_LLM_OCR.py
# Create by GF 2025-09-19 16:53

# Requirement: LLM (Multimodal)

import base64
# ..................................................
import fitz  # PyMuPDF 1.26.7
# ..................................................
import PY3_Requests2_POST_OpenWebUI069

# ##################################################

class PY3_Requests2_POST_OpenWebUI069_LLM_OCR(object):

    def __init__(self):

        self.Pub_Host:str = "127.0.0.1"
        self.Pub_Port:str = "3000"
        # ..........................................
        self.Pub_Model:str = "granite3.1-dense:8b"
        self.Pub_Token:str = ''

    def File_to_Text(self, File_Path:str, DPI:int = 150) -> str:

        Result_Text:str = str('')
        # ..........................................
        if (".pdf" in File_Path.lower()): Result_Text = self.PDF_to_Text(PDF_Path = File_Path, DPI = DPI)
        if (".png" in File_Path.lower()): Result_Text = self.PNG_to_Text(PNG_Path = File_Path)
        if (".jpg" in File_Path.lower()): Result_Text = self.JPG_to_Text(JPG_Path = File_Path)
        # ..........................................
        return Result_Text

    def PNG_to_Text(self, PNG_Path:str) -> str:

        PNG_Text:str = str('')
        # ..........................................
        POST_OpenWebUI069 = PY3_Requests2_POST_OpenWebUI069.PY3_Requests2_POST_OpenWebUI069()
        POST_OpenWebUI069.Pub_Host = self.Pub_Host
        POST_OpenWebUI069.Pub_Port = self.Pub_Port
        # ..........................................
        PNG_Text = POST_OpenWebUI069.Round_1_Chat_With_Image_File(
            Token                     = self.Pub_Token,
            Model                     = self.Pub_Model,
            Message                   = "Please extract the content from the image.",
            Image_File_Path           = PNG_Path,
            Specified_Image_Extension = ".png"
        )
        # ..........................................
        return PNG_Text

    def JPG_to_Text(self, JPG_Path:str) -> str:

        JPG_Text:str = str('')
        # ..........................................
        POST_OpenWebUI069 = PY3_Requests2_POST_OpenWebUI069.PY3_Requests2_POST_OpenWebUI069()
        POST_OpenWebUI069.Pub_Host = self.Pub_Host
        POST_OpenWebUI069.Pub_Port = self.Pub_Port
        # ..........................................
        JPG_Text = POST_OpenWebUI069.Round_1_Chat_With_Image_File(
            Token                     = self.Pub_Token,
            Model                     = self.Pub_Model,
            Message                   = "Please extract the content from the image.",
            Image_File_Path           = JPG_Path,
            Specified_Image_Extension = ".jpg"
        )
        # ..........................................
        return JPG_Text

    def PDF_to_Text(self, PDF_Path:str, DPI:int = 150, Max_Read_Page_Num:int = 0) -> str:

        # 图片太大, 可能会导致 Token 数量超过模型限制,
        # 例如 Open WebUI 0.6.9 返回的异常信息:
        #     {"detail": "400: The decoder prompt (length 8598) is longer than the maximum model length of 8192.
        #                Make sure that `max_model_len` is no smaller than the number of text tokens plus multimodal tokens.
        #                For image inputs,
        #                the number of image tokens depends on the number of images,
        #                and possibly their aspect ratios as well."}
        # 降低 DPI 可以降低图片分辨率, 以降低图片大小。
        # 通常高质量图片 DPI 为 300dpi。
        # 改用 JPEG 格式压缩图像也能显著降低图像大小 (比 PNG 更小)。

        PDF_Full_Text:str = str('')
        # ..........................................
        PDF_File = fitz.open(PDF_Path)  # 打开 PDF 文件
        # ..........................................
        POST_OpenWebUI069 = PY3_Requests2_POST_OpenWebUI069.PY3_Requests2_POST_OpenWebUI069()
        POST_OpenWebUI069.Pub_Host = self.Pub_Host
        POST_OpenWebUI069.Pub_Port = self.Pub_Port
        # ..........................................
        for Page_Num in range(len(PDF_File)):
            # 获取 PDF 页面
            PDF_Page        = PDF_File.load_page(Page_Num)
            Matrix_Object   = fitz.Matrix(DPI / 72, DPI / 72)
            Pixmap_Object   = PDF_Page.get_pixmap(matrix = Matrix_Object)
            # ......................................
            # 从 Pixmap 对象转换为 Base64 编码的图像 (支持 "png", "jpeg", "pnm", "ppm", "pgm", "pbm")
            Img_Bytes:bytes = Pixmap_Object.tobytes("png")
        #   Img_Bytes:bytes = Pixmap_Object.tobytes("jpeg", quality = 80)  # 中等质量
            Org_Base64:str  = base64.b64encode(Img_Bytes).decode("utf-8")
            Img_Base64      = "data:image/png;base64,%s" % Org_Base64
            # ......................................
            PDF_Page_Text:str = POST_OpenWebUI069.Round_1_Chat_With_Image_Base64(
                Token        = self.Pub_Token,
                Model        = self.Pub_Model,
                Message      = "Please extract the content from the image.",
                Image_Base64 = Img_Base64
            )
            # ......................................
            PDF_Full_Text    = "%sPage Number: %d\n%s\n\n" % (PDF_Full_Text, Page_Num, PDF_Page_Text)
            # ......................................
            if (Max_Read_Page_Num != 0 and Max_Read_Page_Num == Page_Num):
                break
        # ..........................................
        PDF_File.close()  # 关闭 PDF 文件
        # ..........................................
        return PDF_Full_Text

# EOF Signed by GF.
