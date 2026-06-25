"""
milvus_client.py — Milvus 连接管理模块

设计决策（来自我们的讨论）：
- 这个文件只负责"怎么连接 Milvus、怎么建 collection"，
  不负责具体的业务逻辑（写入是 ingest.py 的事，检索是 retrieve.py 的事）
- ingest.py 和 retrieve.py 都会调用这里的 connect_milvus()，
  避免两边各自重复写一遍"怎么连接"
"""

from pymilvus import MilvusClient, DataType, MilvusException

COLLECTION_NAME = "enterprise_docs"


def connect_milvus():
    """
    连接 Milvus，如果 collection 不存在就创建它。

    Returns:
        MilvusClient 实例——调用者（ingest.py / retrieve.py）需要拿这个对象
        去调用 .insert()、.search()、.has_collection() 等方法

    Raises:
        MilvusException: 连接失败时，打印一句友好提示后，
        依然把异常往外抛——不悄悄返回 None，避免调用者在不知情的情况下继续往下跑
    """
    try:
        client = MilvusClient(uri="http://localhost:19530")
    except MilvusException as e:
        print("无法连接到 Milvus，请确认容器是否已启动（docker-compose up -d）")
        raise e

    if not client.has_collection(COLLECTION_NAME):
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
        schema.add_field(field_name="file_hash", datatype=DataType.VARCHAR, max_length=64)

        index_params = client.prepare_index_params()
        index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")

        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params,
        )

    return client