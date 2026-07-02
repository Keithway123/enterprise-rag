import json
import os
import unittest

from app.chunking import chunk_table, chunk_text

os.environ.setdefault("DASHSCOPE_API_KEY", "test-key-for-import-only")

from app.core.retrieve import (  # noqa: E402
    build_prompt,
    format_retrieval_trace,
    format_table_as_markdown,
    organize_by_mode,
)


class ChunkTextTests(unittest.TestCase):
    def test_chunk_text_uses_overlap(self):
        text = "0123456789" * 3

        chunks = chunk_text(text, chunk_size=10, overlap=3)

        self.assertEqual(chunks[0], "0123456789")
        self.assertEqual(chunks[1], "7890123456")
        self.assertEqual(chunks[0][-3:], chunks[1][:3])

    def test_chunk_text_short_text_returns_one_chunk(self):
        chunks = chunk_text("短文本", chunk_size=10, overlap=2)

        self.assertEqual(chunks, ["短文本"])

    def test_chunk_text_rejects_overlap_that_cannot_move_forward(self):
        with self.assertRaises(ValueError):
            chunk_text("abcdef", chunk_size=5, overlap=5)


class ChunkTableTests(unittest.TestCase):
    def test_chunk_table_adds_header_to_later_chunks(self):
        table = [
            ["name", "department"],
            ["zhangsan", "tech"],
            ["lisi", "marketing"],
            ["wangwu", "finance"],
        ]

        chunks = chunk_table(table, rows_per_chunk=2)

        self.assertEqual(chunks[0], [["name", "department"], ["zhangsan", "tech"], ["lisi", "marketing"]])
        self.assertEqual(chunks[1], [["name", "department"], ["wangwu", "finance"]])

    def test_chunk_table_does_not_create_header_only_chunk(self):
        table = [
            ["name", "department"],
            ["zhangsan", "tech"],
            ["lisi", "marketing"],
        ]

        chunks = chunk_table(table, rows_per_chunk=1)

        self.assertEqual(chunks[0], [["name", "department"], ["zhangsan", "tech"]])
        self.assertEqual(chunks[1], [["name", "department"], ["lisi", "marketing"]])

    def test_chunk_table_empty_table_returns_empty_list(self):
        self.assertEqual(chunk_table([], rows_per_chunk=3), [])

    def test_chunk_table_rejects_zero_rows_per_chunk(self):
        with self.assertRaises(ValueError):
            chunk_table([["姓名", "部门"]], rows_per_chunk=0)


class MarkdownTableTests(unittest.TestCase):
    def test_format_table_as_markdown_keeps_columns_and_rows(self):
        chunks = [
            {
                "table_data_json": json.dumps(
                    [["姓名", "部门"], ["张三", "研发部"]],
                    ensure_ascii=False,
                )
            },
            {
                "table_data_json": json.dumps(
                    [["姓名", "部门"], ["李四", "市场部"]],
                    ensure_ascii=False,
                )
            },
        ]

        markdown = format_table_as_markdown(chunks)

        self.assertEqual(
            markdown,
            "|姓名|部门|\n|---|---|\n|张三|研发部|\n|李四|市场部|",
        )


class PromptAndTraceTests(unittest.TestCase):
    def test_organize_by_mode_treats_missing_table_json_as_text(self):
        raw_results = [
            {"text": "普通文本", "source": "a.pdf", "page": 1},
            {
                "text": "姓名 部门\n张三 研发部",
                "table_data_json": json.dumps([["姓名", "部门"], ["张三", "研发部"]]),
            },
        ]

        text_results, table_results = organize_by_mode(raw_results)

        self.assertEqual(len(text_results), 1)
        self.assertEqual(text_results[0]["text"], "普通文本")
        self.assertEqual(len(table_results), 1)

    def test_build_prompt_tells_llm_to_admit_missing_evidence(self):
        text_results = [
            {
                "source": "data/raw/policy.pdf",
                "page": 2,
                "text": "年假需提前3个工作日申请。",
            }
        ]

        prompt = build_prompt(text_results, table_results=[], query="年假提前几天申请？")

        self.assertIn("只能根据下面的材料内容回答", prompt)
        self.assertIn("找不到答案依据", prompt)
        self.assertIn("年假需提前3个工作日申请。", prompt)
        self.assertIn("用户问题：年假提前几天申请？", prompt)

    def test_format_retrieval_trace_shows_rank_score_source_and_preview(self):
        raw_results = [
            {
                "distance": 0.87654,
                "source": "data/raw/table.pdf",
                "page": 1,
                "mode": "table",
                "table_index": 2,
                "table_chunk_index": 1,
                "text": "姓名 部门\n张三 研发部",
            }
        ]

        trace = format_retrieval_trace(raw_results)

        self.assertIn("1. score=0.8765", trace)
        self.assertIn("source=data/raw/table.pdf", trace)
        self.assertIn("page=1", trace)
        self.assertIn("table=2, table_chunk=1", trace)
        self.assertIn("preview=姓名 部门 张三 研发部", trace)


if __name__ == "__main__":
    unittest.main()
