from app.core.milvus_client import connect_milvus,COLLECTION_NAME
from app.embedding import get_embedding
import json


ANSWER_RULES = """回答规则：
1. 只能根据下面的材料内容回答，不要使用材料外的知识补充细节。
2. 如果材料内容没有答案依据，请如实回答：找不到答案依据。
3. 如果能回答，请尽量带上来源文件和页码。"""


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
        if data.get("table_data_json") is None:#None 或字段不存在，都说明不是表格格式
            text_result.append(data)
        else:
            table_result.append(data)
    
    return text_result,table_result

    
def reorder_table_chunks(table_results:list[dict])->list[dict]:
    #step1： 根据table_index
    groups = group_by_table_index(table_results)

    #step2：在组内根据table_chunk_index排序
    final_result = []
    for idx, chunks in groups.items():
        sorted_group = sorted(chunks,key = lambda c:c.get("table_chunk_index", 0))
        final_result.extend(sorted_group)

    return final_result

def format_table_as_markdown(table_chunks:list[dict]) ->str:
    header = json.loads(table_chunks[0]["table_data_json"])[0]
    all_rows = [] 
    
    #获取数据行
    for chunk in table_chunks:
        table_data = json.loads(chunk["table_data_json"])
        all_rows.extend(table_data[1:])

   
    #表头
    header_line = "|" + "|".join(header) + "|"

    #分隔符行 separator_line
    separator_line = "|" + "|".join(["---"]*len(header)) + "|"

    row_lines = []
    for row in all_rows:
        row_line = "|" + "|".join(row) + "|"
        row_lines.append(row_line)

    #list + list
    markdown_table ="\n".join([header_line,separator_line] + row_lines)

    return markdown_table

def group_by_table_index(table_results:list[dict]) -> dict[int, list[dict]]:
    groups = {}
    for record in table_results:
        idx = record.get("table_index", 0)
        if idx not in groups:
            groups[idx] = []
        groups[idx].append(record)

    return groups

def build_prompt(text_results:list[dict],table_results: list[dict],query:str)-> str:
    #table
    groups =group_by_table_index(table_results)

    table_markdown_list = [] 

    for idx,chunks in groups.items():
        sorted_chunks = sorted(chunks,key=lambda c:c.get("table_chunk_index", 0))
        markdown = format_table_as_markdown(sorted_chunks)
        source = sorted_chunks[0].get("source", "unknown")
        page = sorted_chunks[0].get("page", "unknown")
        labeled_markdown = f"{format_source_label(source,page,'表格')}\n{markdown}"
        table_markdown_list.append(labeled_markdown)
    #text
    text_with_source_list = []

    for record in text_results:
        source = record.get("source", "unknown")
        page = record.get("page", "unknown")
        labeled_text = f"{format_source_label(source, page, '文本')}\n{record.get('text', '')}"
        text_with_source_list.append(labeled_text)
    
    all_materials = []
    all_materials.extend(table_markdown_list)
    all_materials.extend(text_with_source_list)

    materials_text = "\n".join(all_materials)
    
    prompt = f"{ANSWER_RULES}\n\n材料内容：\n{materials_text}\n\n用户问题：{query}"

    return prompt


def format_retrieval_trace(raw_results: list[dict]) -> str:
    """
    把 Milvus 召回结果整理成适合人工排查的文本。

    这一步不是给 LLM 看的，而是给我们自己看的：答案错了时，先判断
    top-k 里有没有真正的答案依据，再去怀疑 prompt 或生成模型。
    """
    lines = []

    for rank, record in enumerate(raw_results, start=1):
        score = record.get("distance", record.get("score"))
        score_text = "N/A" if score is None else f"{score:.4f}"
        source = record.get("source", "unknown")
        page = record.get("page", "unknown")
        mode = record.get("mode", "unknown")
        table_index = record.get("table_index")
        table_chunk_index = record.get("table_chunk_index")
        preview = record.get("text", "").replace("\n", " ")[:120]

        table_label = ""
        if table_index is not None:
            table_label = f", table={table_index}, table_chunk={table_chunk_index}"

        lines.append(
            f"{rank}. score={score_text}, source={source}, page={page}, mode={mode}"
            f"{table_label}\n   preview={preview}"
        )

    return "\n".join(lines)


def build_explainable_prompt(query: str, top_k: int = 5) -> dict:
    """
    完成一次可解释检索：问题 -> top-k -> 分类 -> prompt -> trace。

    返回 dict 而不是只返回 prompt，是为了保留排查线索：
    - raw_results: Milvus 原始召回结果
    - retrieval_trace: 人能快速看的召回摘要
    - prompt: 最终交给 LLM 的材料
    """
    raw_results = search_similar_chunks(query, top_k=top_k)
    text_results, table_results = organize_by_mode(raw_results)
    prompt = build_prompt(text_results, table_results, query)

    return {
        "query": query,
        "top_k": top_k,
        "raw_results": raw_results,
        "retrieval_trace": format_retrieval_trace(raw_results),
        "prompt": prompt,
    }

def format_source_label(source:str, page, content_type:str) -> str:
    """
    有页码就显示页码，没页码不显示None页
    """
    if page is None:
        return f"（来自 {source}，{content_type}）："   
     
    return f"（来自 {source} 第{page}页，{content_type}）："

if __name__ =="__main__":
    results = search_similar_chunks("张三在什么部门？",top_k=3)
    print(f"共召回{len(results)}条结果")#result[0] result[1] result[2]
    print("第一条结果的完整结构：")
    print(results[0])
