import tempfile
import unittest
from pathlib import Path

from app.parsers.web_parser import parse_web


class WebParserTests(unittest.TestCase):
    def test_parse_web_extracts_text_and_table_without_noise_or_duplicates(self):
        html = """
        <html>
          <body>
            <nav>首页 关于我们</nav>
            <main>
              <h1>公司部门人员名单测试网页</h1>
              <p>这是一份测试用网页。</p>
              <table>
                <tr>
                  <th>姓名</th>
                  <th>部门</th>
                </tr>
                <tr>
                  <td><p>张三</p></td>
                  <td>技术部</td>
                </tr>
              </table>
              <p>补充说明：以上数据为测试用途。</p>
            </main>
            <footer>版权所有 2026</footer>
            <script>console.log("noise")</script>
          </body>
        </html>
        """

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "test.html"
            file_path.write_text(html, encoding="utf-8")

            result = parse_web(str(file_path))

        self.assertEqual(result["mode"], "web")

        text_items = [item["text"] for item in result["content"] if item["type"] == "text"]
        table_items = [item for item in result["content"] if item["type"] == "table"]

        self.assertIn("公司部门人员名单测试网页", text_items)
        self.assertIn("这是一份测试用网页。", text_items)
        self.assertIn("补充说明：以上数据为测试用途。", text_items)

        self.assertNotIn("首页 关于我们", text_items)
        self.assertNotIn("版权所有 2026", text_items)
        self.assertNotIn('console.log("noise")', text_items)

        self.assertEqual(len(table_items), 1)
        self.assertEqual(
            table_items[0]["data"],
            [["姓名", "部门"], ["张三", "技术部"]],
        )

        # Table cells are already parsed as structured data, so they should not
        # appear again as normal text.
        self.assertNotIn("张三", text_items)


if __name__ == "__main__":
    unittest.main()
