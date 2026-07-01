# PDF RAG Eval - test_table - chunk500 topk5

## Config

- source: data/raw/test_table.pdf
- parse_mode: table
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 10
- top_k: 5

## Results

| id  | retrieval_hit | answer_correct | error_type | notes                                                                        |
| --- | ------------- | -------------- | ---------- | ---------------------------------------------------------------------------- |
| Q1  | yes           | yes            | none       | 召回了两条topk，在text下长度更长，召回的表格信息可能因为内容少所以没明显变化 |
| Q2  | yes           | yes            | none       | 同Q1一样的情况                                                               |
| Q3  | yes           | yes            | none       | 一样的情况                                                                   |
| Q4  | no            | yes            | none       | 有召回两条top_k score是0.5459 和0.4385，LLM返回答案符合预期                  |

## Observation

-
