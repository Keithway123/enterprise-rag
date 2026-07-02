# PDF RAG Eval - test_table - chunk100 topk5

## Config

- source: data/raw/test_table.pdf
- parse_mode: table
- chunk_size: 100
- overlap: 20
- rows_per_chunk: 10
- top_k: 5

## Results

| id  | retrieval_hit | answer_correct | error_type | notes |
| --- | ------------- | -------------- | ---------- | ----- |
| Q1  | yes           | yes            | none       |       |
| Q2  | yes           | yes            | none       |       |
| Q3  | yes           | yes            | none       |       |
| Q4  | no            | yes            | none       |       |

## Observation

-
