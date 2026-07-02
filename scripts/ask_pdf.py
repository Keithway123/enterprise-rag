"""
Deprecated: use scripts.ask_rag instead.

保留这个入口是为了兼容早期命令：
    uv run python -m scripts.ask_pdf "问题"
"""

from scripts.ask_rag import main

if __name__ == "__main__":
    main()
