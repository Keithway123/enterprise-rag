from pymilvus import MilvusClient,DataType

from app.parsers.pdf_parser import parse_pdf
from app.chunking import chunk_text
from app.embedding import get_embedding

COLLECTION_NAME ="enterprise_docs"
print("ingest_document - 开始执行")

def ingest_document(file_path:str , parse_mode:str , chunk_size:int = 500 , overlap:int =50):
    print("ingest_document 函数已经被调用，参数是:", file_path, parse_mode)

    client = MilvusClient(uri="http://localhost:19530")

    if not client.has_collection(COLLECTION_NAME):
        schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
 
        index_params = client.prepare_index_params()
        index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")
 
        client.create_collection(
            collection_name=COLLECTION_NAME,
            schema=schema,
            index_params=index_params,
        )

    parsed = parse_pdf(file_path,mode=parse_mode)

    data_to_insert=[]

    for item in parsed["content"]:
        page_number = item["page"]
        item_type = item["type"]

        if item_type == "text":
            chunks = chunk_text(item["text"],chunk_size=chunk_size,overlap=overlap)
            for chunk in chunks:
                vector = get_embedding(chunk)
                data_to_insert.append({
                    "vector":vector,
                    "text":chunk,
                    "source":file_path,
                    "page":page_number,
                    "mode":parse_mode,
                })
        elif item_type =="table":
            table_text = "\n".join([" ".join(row) for row in item["data"]])
            #table_text = chunk_table(table_text,rows_per_chunk=10)
            vector = get_embedding(table_text)
            data_to_insert.append({
                "vector":vector,
                "text":table_text,
                "source":file_path,
                "page":page_number,
                "mode":parse_mode,
            })

    if data_to_insert:
        result = client.insert(collection_name=COLLECTION_NAME,data=data_to_insert)
        print(f"写入完成，共{result['insert_count']}条数据")
    else:
        print("没有内容可以写入")

if __name__ == "__main__":
    ingest_document("data/raw/test_table.pdf",parse_mode="table",chunk_size=100,overlap=20)