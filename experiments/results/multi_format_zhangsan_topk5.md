# 三格式检索对比实验：张三在哪个部门？

## 实验配置

- 问题：张三在哪个部门？
- top_k：5
- chunk_size：500
- overlap：50
- rows_per_chunk：2
- 测试文件：
    - `data/raw/test_table.pdf`
    - `data/raw/test_word.docx`
    - `data/raw/test_web.html`

## 实验结果

| 格式 | 入库记录数 | top1 是否命中答案 | top1 score | top1 内容              |
| ---- | ---------: | ----------------- | ---------: | ---------------------- |
| PDF  |          3 | 是                |     0.7560 | 张三 技术部 2023-01-15 |
| Word |          7 | 是                |     0.7561 | 张三 技术部 2023-01-15 |
| Web  |          7 | 是                |     0.7560 | 张三 技术部 2023-01-15 |

## 观察

- PDF / Word / Web 三种格式都能稳定召回正确表格 chunk。
- 三种格式最终都进入统一结构：`text` / `table_data_json` / `metadata`。
- PDF 记录数更少，是因为当前测试 PDF 的表格外文本被合并成一个 text record；Word/Web 按结构节点拆成多条 text record。
- Word/Web 没有页码，prompt 已避免出现 `第None页`，但来源显示格式后续仍可统一优化。

## 结论

parser 层已经把不同文档格式的差异屏蔽掉，后续 `chunk -> embedding -> Milvus -> retrieve -> prompt` 链路可以复用同一套处理逻辑。表格按行切块并补表头的策略，在三种格式下都能稳定支持问题召回。
