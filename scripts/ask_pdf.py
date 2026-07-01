import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.retrieve import build_explainable_prompt
from app.llm import generate_answer

def main():
    parser = argparse.ArgumentParser(description="Ask a question against the PDF RAG knowledge base")
    parser.add_argument("query", help="用户问题")
    parser.add_argument("--top-k", type=int, default=5, help="Milvus 召回数量")
    parser.add_argument("--show-prompt", action="store_true", help="是否打印完整prompt")
    args = parser.parse_args()

    debug_info = build_explainable_prompt(args.query,top_k=args.top_k)
    answer = generate_answer(debug_info["prompt"])

    print("=== 用户问题 ===")
    print(debug_info["query"])
    print()

    print("=== Top-k 召回调试信息 ===")
    print(debug_info["retrieval_trace"] or "没有召回结果")
    print()

    if args.show_prompt:
        print("=== 最终 Prompt ===")
        print(debug_info["prompt"])
        print()

    print("=== LLM答案 ====")
    print(answer)

if __name__ == "__main__":
    main()