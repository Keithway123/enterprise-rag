"""
查询脚本：验证刚写入 Milvus 的数据，长什么样。

用 query()（按条件筛选）而不是 search()（按向量相似度检索）——
这次只是想看"数据库里现在有什么"，不是做相似度搜索。
"""

from pymilvus import MilvusClient
import json

client = MilvusClient(uri="http://localhost:19530")

results = client.query(
    collection_name="enterprise_docs",
    filter="",  # 一个永远成立的条件，相当于"把所有记录都查出来",>=0会限制字段为int，""就不限制字段
    output_fields=["id", "text", "source", "page","table_index","table_chunk_index","mode","table_data_json"], 
    # 不要 output_fields=["*"]
    limit=1000,
    # 向量本身有 1024 个数字，打印出来会刷屏，这次不需要看它
)

print(f"共查到 {len(results)} 条记录\n")

for i, record in enumerate(results, start=1):
    print(f"--- 第 {i} 条 ---")
    print(f"id: {record['id']}")
    print(f"source: {record['source']}")
    print(f"page: {record['page']}")
    print(f"table_index: {record.get('table_index')}")
    print(f"table_chunk_index: {record.get('table_chunk_index')}")
    print(f"mode: {record['mode']}")
    print(f"text: {record['text']}")
    print(f"table_data_json: {record.get('table_data_json')}")

    """
    验证合法的 JSON 字符串
    raw_json = record.get('table_data_json')
    if raw_json is not None:
        restored = json.loads(raw_json)
        print(f"还原后的类型: {type(restored)}")
        print(f"还原后的内容: {restored}")
    """
    print()
