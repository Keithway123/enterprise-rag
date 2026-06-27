from app.core.milvus_client import connect_milvus,COLLECTION_NAME
from app.embedding import get_embedding
import json


def search_similar_chunks(query:str, top_k:int =5 )-> list[dict]:
    user_query_vetor = get_embedding(query)

    client = connect_milvus()
    
    search_result= client.search(
        collection_name=COLLECTION_NAME,
        data = [user_query_vetor],#只传入了一个向量
        output_fields=["text","source","page","mode","table_index","table_chunk_index","table_data_json"],
        limit= top_k,#top_k=3 召回三条相似度最高的record
        )
    
    flat_results = [] 
    for result in search_result[0]:
        result = {**result,**result["entity"]}
        result.pop("entity")
        flat_results.append(result)
    return flat_results

def organize_by_mode(raw_result:list[dict])-> tuple[list[dict],list[dict]]:
    text_result=[]
    table_result=[]

    for data in raw_result:
        if data["table_data_json"] is None:#None 说明是text格式：
            text_result.append(data)
        else:
            table_result.append(data)
    
    return text_result,table_result

    
def reorder_table_chunks(table_results:list[dict])->list[dict]:
    #step1： 根据table_index
    groups = {}
    for record in table_results:
        idx = record["table_index"]
        if idx not in groups:
            groups[idx] = []
        groups[idx].append(record)
    
    #step2：在组内根据table_chunk_index排序
    final_result = []
    for idx, chunks in groups.items():
        sorted_group = sorted(chunks,key = lambda c:c["table_chunk_index"])
        final_result.extend(sorted_group)

    return final_result

def format_table_as_markdown(table_chunks:list[dict]) ->str:
    header = None
    all_rows = [] 
    
    for chunk in table_chunks:
        table_data = json.loads(chunk["table_data_json"])
        
        if chunk["table_chunk_index"] == 1:
            header = table_data[0]#['姓名', '部门', '入职日期'] list->三个元素
        all_rows.extend(table_data[1:])
    
    #表头
    header_line = "|" + "|".join(header) + "|"

    #分隔符行 separ
    separator_line = "|" + "|".join(["---"]*len(header)) + "|"

    row_lines = []
    for row in all_rows:
        row_line = "|" + "|".join(row) + "|"
        row_lines.append(row_line)

    markdown_table ="\n".join([header_line,separator_line] + row_lines)

    return markdown_table

if __name__ =="__main__":
    results = search_similar_chunks("张三在什么部门？",top_k=3)
    print(f"共召回{len(results)}条结果")#result[0] result[1] result[2]
    print("第一条结果的完整结构：")
    print(results[0])