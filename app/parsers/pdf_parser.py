"""
pdf_parser.py — PDF 解析模块

设计决策（来自我们之前的讨论，别忘了为什么这样设计）：
1. mode 由调用者手动指定，不做"自动判断该用哪种模式"——
   学习阶段要自己练判断力，不要让程序替你猜。
2. mode="table" 内部可以自动按页检测表格（pdfplumber 自带能力），
   这跟"自动判断扫描件"不是同一类风险——表格漏检的结果是"明显混乱"，容易发现。
3. mode="ocr" 的输出不能直接信任——OCR 错误是"看起来通顺但悄悄错"的那种危险错误，
   后面写分块/检索逻辑时要记得这一点。

依赖：
    uv add pdfplumber pytesseract pdf2image pillow
    （pytesseract 还需要系统装 tesseract-ocr 这个识别引擎本体，不只是 Python 包）
"""

import pdfplumber
import logging
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def parse_pdf(file_path: str, mode: str) -> dict:
    """
    解析一份 PDF，返回统一格式的结果。

    Args:
        file_path: PDF 文件路径
        mode: "text"（纯文字提取） / "table"（表格提取） / "ocr"（扫描件识别）

    Returns:
        一个字典，至少包含：
        {
            "mode": 用的是哪种模式,
            "content": 提取出来的内容（具体长什么样，下面每个模式分别决定）,
            "source": file_path,
        }
    """
    if mode == "text":
        return _parse_text(file_path)
    elif mode == "table":
        return _parse_table(file_path)
    elif mode == "ocr":
        return _parse_ocr(file_path)
    else:
        # 想一下：如果调用者传了一个 mode="excel" 这种压根不存在的值，
        # 程序应该悄悄返回空结果，还是应该直接报错、提前暴露问题？
        # 回想我们聊过的"明显出错 vs 悄悄出错"——哪种处理方式更安全？
        raise ValueError(f"不支持的 mode: {mode}")


def _parse_text(file_path: str) -> dict:
    """
    用 pdfplumber 提取纯文字。

    提示：pdfplumber.open(file_path) 之后，遍历 pdf.pages，
    每一页调用 page.extract_text()，记得处理"这一页提取结果是 None"的情况
    （有些页面可能没有文字，extract_text() 会返回 None，不是空字符串）。

    思考一下：多页文档，你打算把每页的文字直接拼成一个大字符串，
    还是保留"第几页"这个信息？回想 CLAUDE.md 第 3 节链路图里写的——
    "文本块列表（每块带 metadata：来源文件、页码/位置）"
    ——这里要不要为后面的"带页码"做准备？
    """
    pages_content = []
    with pdfplumber.open(file_path) as pdf:
        for page_number,page in enumerate(pdf.pages,start=1):
            pages_text = page.extract_text()
            if pages_text is None:
                continue
            pages_content.append({"page":page_number,"text":pages_text})

    if not pages_content:
        logging.warning(f"{file_path} 用text模式提取后为空,可能是扫描件,建议改用mode='ocr'")

    return {
        "mode":"text",
        "content":pages_content,
        "source":file_path,
    } 


def _parse_table(file_path: str) -> dict:
    """
    用 pdfplumber 提取表格。

    提示：每一页调用 page.extract_tables()，
    这个方法返回的是"一个列表，列表里每个元素是一张表格"，
    每张表格本身又是"一个二维列表"（行 x 列）。

    思考一下：如果一页里有表格，也有表格之外的普通文字
    （比如表格上方有一句说明），这部分文字要不要也提取出来？
    要不要在这个函数里，同时调用 extract_text() 把非表格的文字也捎带上？
    """
    tables_content = []
    other_text_content =[]

    with pdfplumber.open(file_path) as pdf:
        for page_number,page in enumerate(pdf.pages,start=1):
            tables = page.extract_tables()

            for table_index, table in enumerate(tables,start=1):
                tables_content.append({
                    "page":page_number,
                    "table_index":table_index,
                    "data":table,
                })

            page_text = page.extract_text()
            if page_text is not None:
                other_text_content.append({"page":page_number,"text":page_text})
    
    return{
        "mode":"table",
        "tables":tables_content,
        "other_text":other_text_content,
        "source":file_path,
    }


def _parse_ocr(file_path: str) -> dict:
    """
    用 OCR 识别扫描件。

    这个会比前两个复杂一点，因为 PDF 本身不是图片格式，
    需要先把 PDF 的每一页"渲染"成图片，再把图片喂给 OCR 引擎。

    大致流程（这次给你流程提示，因为涉及的库比较新）：
    1. 用 pdf2image 库的 convert_from_path(file_path)，
       把 PDF 转成一组图片对象（每页一张）
    2. 对每张图片，用 pytesseract.image_to_string(image, lang="chi_sim")
       做识别（lang 参数指定识别中文，默认是英文）
    3. 把每页识别出来的文字收集起来

    提醒：识别结果不要直接当成"绝对正确"，
    后面如果发现检索效果差，第一个该怀疑的环节就是这里。
    """
    pages_content=[] 

    images = convert_from_path(file_path, poppler_path=r"E:\AI Agent Job Road\poppler-26.02.0\Library\bin")
    for page_number,image in enumerate(images,start=1):
        page_text = pytesseract.image_to_string(image,lang="chi_sim")

        if not page_text.strip():
            continue

        pages_content.append({"page":page_number,"text":page_text})
        
    
    if not pages_content:
        logging.warning(f"{file_path} 用 ocr 模式识别后内容为空，请检查图片质量或语言包设置")

    return {
        "mode":"ocr",
        "content":pages_content,
        "source":file_path
    }


if __name__ == "__main__":
    # 简单的手动测试入口，方便你单独跑这个文件验证
    # 把这里换成你自己的测试 PDF 路径
    result = parse_pdf("data/raw/scanned_test.pdf", mode="ocr")
    print(result)