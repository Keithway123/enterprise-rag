"""
通用文档导入脚本。

职责边界：
- PDF: 需要 --mode text/table/ocr
- Word: 默认解析 text + table；如果传了 --mode，只提示并忽略
"""

import argparse
from pathlib import Path

from app.core.ingest import ingest_document


def main():
    parser = argparse.ArgumentParser(description="Import PDF/Word document into Milvus")
    parser.add_argument("file_path", help="Document path, for example: data/raw/test_table.pdf")
    parser.add_argument(
        "--mode",
        choices=["text", "table", "ocr"],
        default=None,
        help="PDF parse mode. Word documents ignore this option.",
    )
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=50)
    parser.add_argument("--rows-per-chunk", type=int, default=50)

    args = parser.parse_args()
    suffix = Path(args.file_path).suffix.lower()

    if suffix == ".pdf" and args.mode is None:
        raise ValueError("PDF 必须指定 --mode: text/table/ocr")

    parse_mode = args.mode

    if suffix == ".docx" and args.mode is not None:
        print("Warning: Word 文档会默认解析 text + table，已忽略 --mode 参数")
        parse_mode = None

    print("Import config:")
    print(f"- file_path: {args.file_path}")
    print(f"- suffix: {suffix}")
    print(f"- mode: {parse_mode}")
    print(f"- chunk_size: {args.chunk_size}")
    print(f"- overlap: {args.overlap}")
    print(f"- rows_per_chunk: {args.rows_per_chunk}")

    ingest_document(
        file_path=args.file_path,
        parse_mode=parse_mode,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        rows_per_chunk=args.rows_per_chunk,
    )


if __name__ == "__main__":
    main()
