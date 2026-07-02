# Multi-format Retrieval Eval

## Config

- time: 2026-07-02T15:58:44
- query: 张三在哪个部门？
- top_k: 5
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 2

## PDF

### Reset

```text
Dropped collection: enterprise_docs
Recreated collection: enterprise_docs
```

### Import

```text
Import config:
- file_path: data/raw/test_table.pdf
- suffix: .pdf
- mode: table
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 2
写入完成，共 3 条记录
```

### Retrieval

```text
=== 用户问题 ===
张三在哪个部门？

=== Top-k 召回调试信息 ===
1. score=0.7560, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
2. score=0.5442, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
3. score=0.3998, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之

=== 最终 Prompt ===
回答规则：
1. 只能根据下面的材料内容回答，不要使用材料外的知识补充细节。
2. 如果材料内容没有答案依据，请如实回答：找不到答案依据。
3. 如果能回答，请尽量带上来源文件和页码。

材料内容：
（来自 data/raw/test_table.pdf 第1页，表格）：
|姓名|部门|入职日期|
|---|---|---|
|张三|技术部|2023-01-15|
|李四|市场部|2023-03-20|
|王五|财务部|2022-11-08|
（来自 data/raw/test_table.pdf 第1页，文本）：
公司部门人员名单测试文档
这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信
息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table'
模式下,表格之外的普通文字是否也能被正确提取出来。
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门。

用户问题：张三在哪个部门？
```

## Word

### Reset

```text
Dropped collection: enterprise_docs
Recreated collection: enterprise_docs
```

### Import

```text
Import config:
- file_path: data/raw/test_word.docx
- suffix: .docx
- mode: None
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== 用户问题 ===
张三在哪个部门？

=== Top-k 召回调试信息 ===
1. score=0.7560, source=data/raw/test_word.docx, page=None, mode=word, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
2. score=0.5452, source=data/raw/test_word.docx, page=None, mode=word
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
3. score=0.5442, source=data/raw/test_word.docx, page=None, mode=word, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
4. score=0.5013, source=data/raw/test_word.docx, page=None, mode=word
   preview=如需更新人员变动，请联系人事部门。
5. score=0.4816, source=data/raw/test_word.docx, page=None, mode=word
   preview=公司部门人员名单测试 Word 文档

=== 最终 Prompt ===
回答规则：
1. 只能根据下面的材料内容回答，不要使用材料外的知识补充细节。
2. 如果材料内容没有答案依据，请如实回答：找不到答案依据。
3. 如果能回答，请尽量带上来源文件和页码。

材料内容：
（来自 data/raw/test_word.docx，表格）：
|姓名|部门|入职日期|
|---|---|---|
|张三|技术部|2023-01-15|
|李四|市场部|2023-03-20|
|王五|财务部|2022-11-08|
（来自 data/raw/test_word.docx，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
（来自 data/raw/test_word.docx，文本）：
如需更新人员变动，请联系人事部门。
（来自 data/raw/test_word.docx，文本）：
公司部门人员名单测试 Word 文档

用户问题：张三在哪个部门？
```

## Web

### Reset

```text
Dropped collection: enterprise_docs
Recreated collection: enterprise_docs
```

### Import

```text
Import config:
- file_path: data/raw/test_web.html
- suffix: .html
- mode: None
- chunk_size: 500
- overlap: 50
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== 用户问题 ===
张三在哪个部门？

=== Top-k 召回调试信息 ===
1. score=0.7560, source=data/raw/test_web.html, page=None, mode=web, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
2. score=0.5452, source=data/raw/test_web.html, page=None, mode=web
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
3. score=0.5443, source=data/raw/test_web.html, page=None, mode=web, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
4. score=0.5014, source=data/raw/test_web.html, page=None, mode=web
   preview=如需更新人员变动，请联系人事部门。
5. score=0.4930, source=data/raw/test_web.html, page=None, mode=web
   preview=公司部门人员名单测试网页

=== 最终 Prompt ===
回答规则：
1. 只能根据下面的材料内容回答，不要使用材料外的知识补充细节。
2. 如果材料内容没有答案依据，请如实回答：找不到答案依据。
3. 如果能回答，请尽量带上来源文件和页码。

材料内容：
（来自 data/raw/test_web.html，表格）：
|姓名|部门|入职日期|
|---|---|---|
|张三|技术部|2023-01-15|
|李四|市场部|2023-03-20|
|王五|财务部|2022-11-08|
（来自 data/raw/test_web.html，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
（来自 data/raw/test_web.html，文本）：
如需更新人员变动，请联系人事部门。
（来自 data/raw/test_web.html，文本）：
公司部门人员名单测试网页

用户问题：张三在哪个部门？
```
