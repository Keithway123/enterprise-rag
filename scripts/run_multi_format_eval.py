import argparse
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS = [
    {
        "label": "PDF",
        "path": "data/raw/test_table.pdf",
        "mode": "table",
    },
    {
        "label": "Word",
        "path": "data/raw/test_word.docx",
        "mode": None,
    },
    {
        "label": "Web",
        "path": "data/raw/test_web.html",
        "mode": None,
    },
]


def run_command(args: list[str]) -> str:
    """
    Reuse existing CLI scripts so automated eval matches the manual path.
    """
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        env=_clean_proxy_env(),
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )

    output = result.stdout
    if result.stderr:
        output += "\n" + result.stderr

    if result.returncode != 0:
        raise RuntimeError(output)

    return output.strip()


def _clean_proxy_env() -> dict[str, str]:
    """
    Local Milvus uses localhost; proxy variables can break pymilvus connections.
    """
    env = dict(os.environ)
    for key in ["HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"]:
        env.pop(key, None)
    env["PYTHONIOENCODING"] = "utf-8"
    return env


def import_document_command(document: dict, args) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "scripts.import_document",
        document["path"],
        "--chunk-size",
        str(args.chunk_size),
        "--overlap",
        str(args.overlap),
        "--rows-per-chunk",
        str(args.rows_per_chunk),
    ]

    if document["mode"] is not None:
        command.extend(["--mode", document["mode"]])

    return command


def run_eval(args) -> str:
    sections = [
        "# Multi-format Retrieval Eval",
        "",
        "## Config",
        "",
        f"- time: {datetime.now().isoformat(timespec='seconds')}",
        f"- query: {args.query}",
        f"- top_k: {args.top_k}",
        f"- chunk_size: {args.chunk_size}",
        f"- overlap: {args.overlap}",
        f"- rows_per_chunk: {args.rows_per_chunk}",
        "",
    ]

    for document in DOCUMENTS:
        sections.extend([f"## {document['label']}", ""])

        reset_output = run_command([
            sys.executable,
            "-m",
            "scripts.reset_collection",
            "--yes",
        ])

        import_output = run_command(import_document_command(document, args))

        retrieval_output = run_command([
            sys.executable,
            "-m",
            "scripts.debug_retrieval",
            args.query,
            "--top-k",
            str(args.top_k),
        ])

        sections.extend([
            "### Reset",
            "",
            "```text",
            reset_output,
            "```",
            "",
            "### Import",
            "",
            "```text",
            import_output,
            "```",
            "",
            "### Retrieval",
            "",
            "```text",
            retrieval_output,
            "```",
            "",
        ])

    return "\n".join(sections)


def parse_args():
    parser = argparse.ArgumentParser(description="Run PDF/Word/Web retrieval eval and save Markdown output.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--chunk-size", type=int, default=500)
    parser.add_argument("--overlap", type=int, default=50)
    parser.add_argument("--rows-per-chunk", type=int, default=2)
    parser.add_argument(
        "--output",
        default="experiments/results/multi_format_eval_latest.md",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    markdown = run_eval(args)

    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Saved eval result to: {output_path}")


if __name__ == "__main__":
    main()
