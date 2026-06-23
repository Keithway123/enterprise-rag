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

import logging
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

# 告诉 pytesseract 这个"遥控器"，真正的"机器"装在哪
# Windows 上几乎总是需要这一行，因为 Tesseract 装完不会自动进系统 PATH
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
    """
    pages_content = []
    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            pages_text = page.extract_text()
            if pages_text is None:
                continue
            pages_content.append({"page": page_number, "type": "text", "text": pages_text})

    if not pages_content:
        # 不报错，不打断程序——但留一条记录，方便事后排查
        # "这份文档是不是其实该用 mode='ocr' 重新处理"
        logging.warning(f"{file_path} 用 text 模式提取后内容为空，可能是扫描件，建议改用 mode='ocr'")

    return {
        "mode": "text",
        "content": pages_content,
        "source": file_path,
    }


def _parse_table(file_path: str) -> dict:
    """
    用 pdfplumber 提取表格，同时提取表格之外的普通文字。

    返回结构跟 _parse_text / _parse_ocr 统一：都是 {"mode", "content", "source"}。
    content 列表里的每个元素，靠 "type" 字段区分是表格还是普通文字——
    这样调用者遍历 content 时，不需要在最外层判断 mode 是不是 "table"，
    只需要看每个元素自己的 "type"。

    已知 TODO（记录在 CLAUDE.md）：extract_tables() 和 extract_text()
    互不感知对方，一页里有表格时，普通文字部分会把表格内容也重复读一遍。
    """
    content = []

    with pdfplumber.open(file_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables()

            for table_index, table in enumerate(tables, start=1):
                content.append({
                    "page": page_number,
                    "type": "table",
                    "table_index": table_index,
                    "data": table,
                })

            page_text = page.extract_text()
            if page_text is not None:
                content.append({
                    "page": page_number,
                    "type": "text",
                    "text": page_text,
                })

    if not content:
        logging.warning(f"{file_path} 用 table 模式提取后内容为空，可能是扫描件，建议改用 mode='ocr'")

    return {
        "mode": "table",
        "content": content,
        "source": file_path,
    }


def _parse_ocr(file_path: str) -> dict:
    """
    用 OCR 识别扫描件。

    思路跟 _parse_text 结构一样：按页处理，每页存一条 {page, text} 记录。
    区别是这次"获取这一页的文字"要分两步：先转图片，再识别。
    """
    pages_content = []

    # 第一步：把整份 PDF 的每一页，都转换成一张图片
    # convert_from_path 返回的是"一个列表，列表里每个元素是一页对应的图片对象"
    # 思考：这个列表的顺序，是不是天然就对应"第几页"？
    # 如果是，你要怎么用 enumerate 拿到"页码 + 这一页的图片"？
    images = convert_from_path(file_path)

    for page_number, image in enumerate(images, start=1):
        # 第二步：把这一页的图片，喂给 OCR 引擎识别
        # lang="chi_sim" 指定用简体中文模型识别（默认是英文，识别中文会全错）
        page_text = pytesseract.image_to_string(image, lang="chi_sim")

        # 思考：OCR 识别一张完全空白的图片，会返回 None，
        # 还是会返回一个空字符串 ""？回想 _parse_text 里判断 None 的写法，
        # 这里的判断条件应该写成什么？
        if not page_text.strip():
            continue

        pages_content.append({"page": page_number, "type": "text","text": page_text})

    if not pages_content:
        logging.warning(f"{file_path} 用 ocr 模式识别后内容为空，请检查图片质量或语言包设置")

    return {
        "mode": "ocr",
        "content": pages_content,
        "source": file_path,
    }


if __name__ == "__main__":
    # 简单的手动测试入口，方便你单独跑这个文件验证
    # 把这里换成你自己的测试 PDF 路径
    result = parse_pdf("data/raw/test_table.pdf", mode="table")
    print(result)