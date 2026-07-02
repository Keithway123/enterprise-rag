import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.retrieve import build_explainable_prompt
from app.llm import generate_answer


def load_questions(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def format_case_result(case: dict, debug_info: dict, answer: str) -> str:
    return f"""## {case["id"]}: {case["question"]}

### Expected

- expected_evidence: {case["expected_evidence"]}
- expected_source: {case["expected_source"]}
- notes: {case["notes"]}

### Retrieval Trace

```text
{debug_info["retrieval_trace"]}
```

### Final Prompt

```text
{debug_info["prompt"]}
```

### Answer

```text
{answer}
```
"""


def main():
    parser = argparse.ArgumentParser(description="Run PDF RAG eval questions")
    parser.add_argument("questions_file", help="JSON questions file")
    parser.add_argument("--top-k", type=int, default=5, help="Milvus retrieval top_k")
    parser.add_argument(
        "--output",
        default=None,
        help="Output markdown file. If omitted, write to experiments/runs/ with timestamp.",
    )
    args = parser.parse_args()

    questions_path = Path(args.questions_file)
    data = load_questions(questions_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(args.output) if args.output else Path(
        f"experiments/runs/pdf_eval_{timestamp}.md"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 这里只收集原始证据，人工判断仍写到 results 文件
    sections = [
        "# PDF RAG Eval Run",
        "",
        "## Config",
        "",
        f"- questions_file: {questions_path}",
        f"- dataset: {data.get('dataset')}",
        f"- top_k: {args.top_k}",
        "",
    ]

    for case in data["questions"]:
        debug_info = build_explainable_prompt(case["question"], top_k=args.top_k)
        answer = generate_answer(debug_info["prompt"])
        sections.append(format_case_result(case, debug_info, answer))

    output_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"Saved eval run to: {output_path}")


if __name__ == "__main__":
    main()
