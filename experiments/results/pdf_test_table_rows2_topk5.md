# PDF RAG Eval - test_table - chunk500 topk5 rows-per-chunk 2

## Config

- source: data/raw/test_table.pdf
- parse_mode: table
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 2
- top_k: 5

## Results

| id  | retrieval_hit | answer_correct | error_type | notes                                                                                                                      |
| --- | ------------- | -------------- | ---------- | -------------------------------------------------------------------------------------------------------------------------- |
| Q1  | yes           | yes            | none       | 之前LLM的答案是**技术部** 现在没有\*号了 top1的score=0.7561 比之前的scroe高了不少                                          |
| Q2  | yes           | yes            | none       | 这次召回的table_chunk有2，说明表格被切成了两块，而且从topk召回的信息显示：chunk1是2行，chunk2是3行，说明表头的添加是成功的 |
| Q3  | yes           | yes            | none       |                                                                                                                            |
| Q4  | no            | yes            | none       | LLM找不到答案依据                                                                                                          |

## Observation

-
