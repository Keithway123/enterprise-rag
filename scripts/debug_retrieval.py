"""
Week 4 调试脚本：可解释检索。

运行示例：
    uv run python scripts/debug_retrieval.py "张三在哪个部门？" --top-k 5

这个脚本暂时不调用 LLM，只做三件事：
1. 把用户问题转成向量并检索 Milvus。
2. 打印 top-k 召回内容、分数、来源和预览。
3. 打印最终会交给 LLM 的 prompt。

这样做是为了先判断“答案依据有没有被召回”，再进入生成答案。
"""

import argparse
import sys
from pathlib import Path

from pymilvus import MilvusException

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.retrieve import build_explainable_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="打印一次可解释 RAG 检索结果")
    parser.add_argument("query", help="用户问题")
    parser.add_argument("--top-k", type=int, default=5, help="Milvus 召回数量")
    args = parser.parse_args()

    try:
        debug_info = build_explainable_prompt(args.query, top_k=args.top_k)
    except MilvusException:
        print("无法连接到 Milvus。请先运行：docker-compose up -d")
        print("如果刚启动容器，请等几秒再重试这个脚本。")
        raise SystemExit(1)

    parser.add_argument("--show-query", action="store_true", help="是否单独打印用户问题")

    if args.show_query:
        print("=== 用户问题 ===")
        print(debug_info["query"])
        print()

    print("=== Top-k 召回调试信息 ===")
    print(debug_info["retrieval_trace"] or "没有召回结果")
    print()

    print("=== 最终 Prompt ===")
    print(debug_info["prompt"])


if __name__ == "__main__":
    main()
