"""
Week 1 验证脚本：确认 Milvus 能正常连接、插入、检索。
这一步不接 Embedding API，用随机向量模拟，先把 Milvus 这一环单独验证通过。
"""

from pymilvus import MilvusClient

# 第一步：连接 Milvus
# uri 用 localhost，因为我们是从"大楼外面"（自己的电脑）去连容器映射出来的端口
client = MilvusClient(uri="http://localhost:19530")

# 第二步：定义一个 collection（相当于关系型数据库里的"表"）
# 这里先用一个测试用的名字，跟以后正式的 collection 区分开
collection_name = "test_collection"

# 如果这个 collection 之前已经存在（比如重复跑这个脚本），先删掉，避免冲突
if client.has_collection(collection_name):
    client.drop_collection(collection_name)

# 第三步：创建 collection
# dimension 这里先用一个小数字（比如 8），方便我们自己肉眼检查向量内容
# 实际项目里，这个数字必须跟你之后用的 Embedding 模型输出的维度一致（CLAUDE.md 里定的是 1024）
client.create_collection(
    collection_name=collection_name,
    dimension=8,
)

# 第四步：插入几条假数据
# 每条数据至少要有：id、向量（vector）、可以附带其他字段（这里加一个 text 字段模拟"原文"）
import random

data = [
    {"id": i, "vector": [random.random() for _ in range(8)], "text": f"这是第 {i} 条测试文本"}
    for i in range(5)
]

insert_result = client.insert(collection_name=collection_name, data=data)
print("插入结果：", insert_result)

# 第五步：检索——用其中一条数据的向量去查，预期它自己应该排第一（距离最近，因为是同一个向量）
query_vector = data[0]["vector"]

search_result = client.search(
    collection_name=collection_name,
    data=[query_vector],
    limit=5,
    output_fields=["text"],
)

print("检索结果：", search_result)