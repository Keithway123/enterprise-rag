"""
word_parser.py - Word 解析模块

目标：
- 按原文顺序解析段落和表格
- 输出结构对齐 pdf_parser.py
- 表格转换成二维数组，复用 chunk_table
"""

import logging

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph


def parse_word(file_path: str) -> dict:
    """
    解析 Word 文档，按原文顺序输出 text/table。
    """
    document = Document(file_path)
    content = []
    table_index = 0

    for child in document.element.body:
        if child.tag.endswith("}p"):
            paragraph = Paragraph(child, document)
            text = paragraph.text.strip()
            if not text:
                continue

            content.append({
                "page": None,
                "type": "text",
                "text": text,
            })

        elif child.tag.endswith("}tbl"):
            table_index += 1
            table = Table(child, document)
            table_data = _extract_table_data(table)

            content.append({
                "page": None,
                "type": "table",
                "table_index": table_index,
                "data": table_data,
            })

    if not content:
        logging.warning(f"{file_path} 用 word 模式提取后内容为空，请检查文档内容")

    return {
        "mode": "word",
        "content": content,
        "source": file_path,
    }


def _extract_table_data(table: Table) -> list[list[str]]:
    """
    把 Word 表格转换成二维数组，复用现有 chunk_table。
    """
    rows = []

    for row in table.rows:
        row_data = []

        for cell in row.cells:
            row_data.append(cell.text.strip())

        rows.append(row_data)

    return rows


if __name__ == "__main__":
    result = parse_word("data/raw/test_word.docx")
    print(result)