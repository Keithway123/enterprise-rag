from app.core.milvus_client import connect_milvus,COLLECTION_NAME
from app.embedding import get_embedding


def search_similar_chunks(query:str, top_k:int =5 )-> list[dict]:
    user_query_vetor = get_embedding(query)

    client = connect_milvus()
    
    search_result= client.search(
        collection_name=COLLECTION_NAME,
        data = [user_query_vetor],#只传入了一个向量
        output_fields=["text","source","page","mode","table_index","table_chunk_index","table_data_json"],
        limit= top_k,
        )
    
    flat_results = [] 
    for result in search_result[0]:
        result = {**result,**result["entity"]}
        result.pop("entity")
        flat_results.append(result)
    return flat_results

if __name__ =="__main__":
    results = search_similar_chunks("张三在什么部门？",top_k=3)
    print(f"共召回{len(results)}条结果")#result[0] result[1] result[2]
    print("第一条结果的完整结构：")
    print(results[0])