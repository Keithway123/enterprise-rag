"""
ingest.py — 建库模块
 
负责把一份文档，完整地变成 Milvus 里的多条记录：
解析 -> 分块 -> 向量化 -> 写入
 
设计决策（来自我们的讨论）：
- 每条记录除了 vector 和 text，还要带 source（来源文件）、page（页码）、
  mode（这一块是 text/table/ocr 哪种方式解析出来的）、file_hash（文件内容的哈希值）——
  mode 字段是为了以后能追溯"这条信息可信度怎么样"，
  尤其 OCR 来源的内容，曾经亲眼验证过"扫描"被识别成"扫挡"这种隐蔽错误，
  标注来源能让使用者多一份警觉
- file_hash 用来防止同一份文档被重复插入：对文件的实际二进制内容算哈希，
  不是对文件路径算——因为路径不变但内容变了的情况，必须被当成"新版本"重新插入
- 这个文件只负责"写入"，不负责"检索"，连接逻辑统一放在 milvus_client.py，
  避免 ingest.py 和 retrieve.py 各自重复写一遍"怎么连接 Milvus"
"""
 
import hashlib
 
from app.parsers.pdf_parser import parse_pdf
from app.chunking import chunk_text, chunk_table
from app.embedding import get_embedding
from app.core.milvus_client import connect_milvus, COLLECTION_NAME
 
 
def get_file_hash(file_path: str) -> str:
    """对文件的实际二进制内容计算哈希值，用来判断"这份文档是否已经插入过"。"""
    with open(file_path, "rb") as f:
        content = f.read()
    return hashlib.sha256(content).hexdigest()
 
 
def is_already_ingested(client, file_hash: str) -> bool:
    """检查 Milvus 里是否已经存在带着同样 file_hash 的记录。"""
    results = client.query(
        collection_name=COLLECTION_NAME,
        filter=f'file_hash == "{file_hash}"',
        output_fields=["id"],
        limit=1,
    )
    return len(results) > 0
 
 
def ingest_document(
    file_path: str,
    parse_mode: str,
    chunk_size: int = 500,
    overlap: int = 50,
    rows_per_chunk: int = 50,
):
    """
    把一份文档，完整地处理并写入 Milvus。
 
    Args:
        file_path: 文档路径
        parse_mode: 解析模式，"text" / "table" / "ocr"
        chunk_size: 普通文字的分块大小（按字数）
        overlap: 普通文字分块的重叠大小
        rows_per_chunk: 表格的分块大小（按行数）
    """
    client = connect_milvus()
 
    # 防重复检查：同一份文档（按内容哈希判断,不是按路径）已经插入过,就跳过
    file_hash = get_file_hash(file_path)
    if is_already_ingested(client, file_hash):
        print(f"{file_path} 这份文档（当前版本）已经插入过，跳过本次写入")
        return
 
    # 第一步：解析
    parsed = parse_pdf(file_path, mode=parse_mode)
 
    # 第二步 + 第三步：分块、向量化，组装成最终要写入的数据
    data_to_insert = []
 
    for item in parsed["content"]:
        page_number = item["page"]
        item_type = item["type"]
 
        if item_type == "text":
            chunks = chunk_text(item["text"], chunk_size=chunk_size, overlap=overlap)
            for chunk in chunks:
                vector = get_embedding(chunk)
                data_to_insert.append({
                    "vector": vector,
                    "text": chunk,
                    "source": file_path,
                    "page": page_number,
                    "mode": parse_mode,
                    "file_hash": file_hash,
                })
 
        elif item_type == "table":
            table_index = item["table_index"]
            table_chunks = chunk_table(item["data"], rows_per_chunk=rows_per_chunk)
            for table_chunk_index,table_chunk in enumerate(table_chunks,start=1):
                table_text = "\n".join([" ".join(row) for row in table_chunk])
                vector = get_embedding(table_text)
                data_to_insert.append({
                    "vector": vector,
                    "text": table_text,
                    "source": file_path,
                    "page": page_number,
                    "table_index":table_index,
                    "table_chunk_index":table_chunk_index,
                    "mode": parse_mode,
                    "file_hash": file_hash,
                })
 
    # 第四步：写入 Milvus
    if data_to_insert:
        result = client.insert(collection_name=COLLECTION_NAME, data=data_to_insert)
        print(f"写入完成，共 {result['insert_count']} 条记录")
    else:
        print("没有内容可写入（解析结果为空）")

if __name__ == "__main__":
    ingest_document("data/raw/test_table.pdf",parse_mode="table",chunk_size=100,overlap=20,rows_per_chunk=10)