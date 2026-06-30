# Experiments

这个目录用来记录 RAG 学习过程里的“可复现实验”。每次实验都尽量保留四件事：

- 输入：文档、问题、候选 chunk 或表格。
- 参数：chunk size、overlap、top-k、解析模式、Embedding 模型。
- 输出：召回内容、相似度、Prompt、最终答案。
- 观察：原来以为是什么，实测发现什么，下一次怎么调。

建议命名方式：

```text
YYYY-MM-DD_topic.md
```

例如：

```text
2026-06-29_chunk-size-topk.md
```

## 实验记录模板

```markdown
# 实验标题

## 问题

这次想验证什么？

## 输入

- 文档：
- 用户问题：
- 对照材料：

## 参数

- parse_mode:
- chunk_size:
- overlap:
- top_k:
- embedding_model:

## 结果

| 参数组合 | 命中情况 | 干扰内容 | 观察 |
| --- | --- | --- | --- |
|  |  |  |  |

## 结论

我原来以为：

实测发现：

所以下一次我会：
```
