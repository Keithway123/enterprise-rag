"""
Deprecated: PDF-only import script.

保留原因：早期学习阶段使用过。
新入口：scripts.import_document，支持 PDF / Word / Web。
"""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# CLI 只做参数解析，核心入库逻辑留在 app.core.ingest
from app.core.ingest import ingest_document


def main():
    parser = argparse.ArgumentParser(description="Import a PDF into Milvus")
    parser.add_argument("file_path", help="PDF file path, for example: data/raw/test_table.pdf")
    parser.add_argument(
        "--mode",
        choices=["text", "table", "ocr"],
        default="text",
        help="PDF parse mode",
    )
    # chunk_size / overlap / rows_per_chunk 是后续实验对比的关键变量
    parser.add_argument("--chunk-size", type=int, default=500, help="Text chunk size")
    parser.add_argument("--overlap", type=int, default=50, help="Text chunk overlap")
    parser.add_argument("--rows-per-chunk", type=int, default=50, help="Table rows per chunk")

    args = parser.parse_args()

    print("=== Import PDF Parameters ===")
    print(f"file_path={args.file_path}")
    print(f"mode={args.mode}")
    print(f"chunk_size={args.chunk_size}")
    print(f"overlap={args.overlap}")
    print(f"rows_per_chunk={args.rows_per_chunk}")
    print()

    ingest_document(
        args.file_path,
        parse_mode=args.mode,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
        rows_per_chunk=args.rows_per_chunk,
    )


if __name__ == "__main__":
    main()
