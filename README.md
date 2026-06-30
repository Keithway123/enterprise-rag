# Enterprise-RAG

一个用来学习企业知识库 RAG 的手写项目。这个仓库的目标不是先套 LangChain 跑通 demo，而是把 RAG 的每一步拆开验证：文档解析、分块、Embedding、Milvus 写入、向量检索、Prompt 拼接和答案来源标注。

AGENTS.md 记录完整学习过程和踩坑复盘；这份 README 面向面试官或第一次打开项目的人，快速说明项目在做什么、做到哪一步、怎么验证。

## 项目目标

- 用一份 PDF、一份 Word、一个网页打通知识库问答链路。
- 亲手验证 chunk size、overlap、top-k、表格切块等参数如何影响检索效果。
- 保留实验记录和固定问题集，让每次调参都有可复查证据。
- 为第三阶段 LangGraph Agent 项目准备一个可靠的 RAG 底座。

## 技术选型

| 模块 | 选择 | 理由 |
| --- | --- | --- |
| API 框架 | FastAPI 预留 | 第一阶段已练过工程底座，这一阶段先聚焦 RAG 链路 |
| 向量数据库 | Milvus Community, Docker Compose | 提前熟悉 collection、schema、index 等企业场景常见概念 |
| Embedding | 阿里百炼 `text-embedding-v3`, 1024 维 | 成本和效果适合学习阶段反复实验 |
| 文档解析 | `pdfplumber`, `pytesseract`, `python-docx`, `BeautifulSoup` | 轻量、透明，便于理解每一步发生了什么 |
| RAG 框架 | 暂不使用 LangChain | 第一版手写核心链路，避免只会调框架不会解释原理 |

## RAG 链路

```text
PDF / Word / Web
  -> parse: text / table / OCR
  -> chunk: text chunks + table row chunks
  -> embed: same embedding model for documents and queries
  -> store: vector + raw text + metadata in Milvus
  -> retrieve: top-k similar chunks
  -> prompt: materials + source labels + user question
  -> answer: LLM response with citations
```

当前重点在第二阶段：RAG 完整链路。第三阶段会在这个底座上继续做 LangGraph Agent 编排。

## 当前进度

- Week 1: Milvus Docker Compose 启动、随机向量插入和自检索验证已完成。
- Week 2: PDF 解析已实现，包含 text/table/OCR 三种模式；Word 和网页解析文件已预留。
- Week 3: 文本分块、表格按行切块、Embedding 调用、Milvus 写入已打通。
- Week 4: 检索、表格 Markdown 还原、Prompt 拼接正在完善。
- Week 5: 将围绕 chunk size、overlap、top-k 和不同文档类型做对比实验。

## 运行方式

1. 启动 Milvus:

```powershell
docker-compose up -d
```

2. 配置环境变量:

在 `.env` 中放入模型 API key，例如：

```text
DASHSCOPE_API_KEY=your-key
```

3. 验证 Milvus:

```powershell
uv run python scripts/verify_milvus.py
```

4. 验证 Embedding:

```powershell
uv run python scripts/verify_embedding.py
```

5. 运行测试:

```powershell
uv run python -m unittest discover -s tests
```

6. 收尾关闭 Milvus:

```powershell
docker-compose down
```

## 已沉淀的关键实验

实验记录放在 `experiments/`：

- `embedding_similarity_sentence_boundary.md`: 完整句子 vs 被切断残句的相似度对比。
- `chunk_topk_eval_template.md`: chunk size、overlap、top-k 对比实验模板。
- `interview_question_bank.md`: 固定 5 个面试自查问题，用于反复验证检索效果。

## 已知 TODO

- 高优先级：解决 PDF 表格模式下 `extract_tables()` 和 `extract_text()` 内容重叠问题，避免同一份表格内容被重复入库。
- 中优先级：把文件二进制 hash 改为解析后内容 hash，避免文档重新保存但文本不变时重复入库。
- 中优先级：补齐 Word 和网页的端到端建库、检索和对比实验。
- 后续阶段：用 FastAPI 包装问答接口，并在第三阶段接入 LangGraph Agent。

## 学习验收标准

这个项目不只看“能不能跑”，还要能回答：

- 为什么某个 chunk 能被召回，另一个不能？
- top-k 增大后，答案为什么可能更差？
- 表格为什么不能按字数切？
- 向量库里除了向量，还必须存哪些 metadata？
- 当答案错了，问题出在解析、分块、检索、Prompt 还是生成？
