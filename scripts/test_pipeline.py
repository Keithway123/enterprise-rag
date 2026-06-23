"""
测试脚本：验证"解析 → 分块 → 向量化"这条链路能不能完整跑通。

这是一次性的验证脚本，放在 scripts/ 里——
正式的建库逻辑会在 app/core/ingest.py 里，这次只是先验证三个模块能不能正确接力。
"""

from app.parsers.pdf_parser import parse_pdf
from app.chunking import chunk_text
from app.embedding import get_embedding

# 第一步：解析（复用 Week 2 的测试文档）
parsed = parse_pdf("data/raw/test.pdf", mode="text")
print(f"解析完成，共 {len(parsed['content'])} 页")

# 第二步：分块
# 思考：parsed['content'] 是"列表套字典"结构（每个字典有 page 和 text）。
# chunk_text 这个函数，接收的参数是一个字符串（text: str），
# 不是一个"列表套字典"。这里需要先把每一页的 text 拿出来，
# 才能交给 chunk_text 处理。

all_chunks = []
for page_record in parsed["content"]:
    page_text = page_record["text"]
    chunks = chunk_text(page_text, chunk_size=100, overlap=20)
    all_chunks.extend(chunks)

print(f"分块完成，共 {len(all_chunks)} 块")
for i, chunk in enumerate(all_chunks, start=1):
    print(f"  块 {i}: {chunk[:30]}...")  # 只打印前 30 个字，避免输出太长

# 第三步：向量化（只对第一块做一次实际调用，验证链路通不通，不用每块都调，省 API 调用）
print()
print("对第一块做向量化测试...")
vector = get_embedding(all_chunks[0])
print(f"生成的向量维度: {len(vector)}")
print(f"向量前 5 个数字: {vector[:5]}")
