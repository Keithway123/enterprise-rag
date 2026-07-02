# Multi-format Chunk-size Compare: 这个文档是用来测试什么功能的？

## Experiment Config

- query: 这个文档是用来测试什么功能的？
- formats: PDF / Word / Web
- top_k: 5
- chunk_size: 100 / 300 / 500
- rows_per_chunk: 2
- purpose: compare how text chunk size changes retrieved chunks and final prompt

## Chunk size = 100

# Multi-format Retrieval Eval

## Config

- time: 2026-07-02T16:54:42
- query: 这个文档是用来测试什么功能的？
- top_k: 5
- chunk_size: 100
- overlap: 20
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
- chunk_size: 100
- overlap: 20
- rows_per_chunk: 2
写入完成，共 5 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.6759, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 
2. score=0.5822, source=data/raw/test_table.pdf, page=1, mode=table
   preview=表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之外的普通文字是否也能被正确提取出来。 补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门
3. score=0.4460, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20
4. score=0.4392, source=data/raw/test_table.pdf, page=1, mode=table
   preview=员信息。如需更新人员变动,请联系人事部门。
5. score=0.4081, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 王五 财务部 2022-11-08

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
息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 
（来自 data/raw/test_table.pdf 第1页，文本）：
表格之后还有一段补充说明文字,用来测试 mode='table'
模式下,表格之外的普通文字是否也能被正确提取出来。
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门
（来自 data/raw/test_table.pdf 第1页，文本）：
员信息。如需更新人员变动,请联系人事部门。

用户问题：这个文档是用来测试什么功能的？
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
- chunk_size: 100
- overlap: 20
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.7520, source=data/raw/test_word.docx, page=None, mode=word
   preview=这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
2. score=0.6255, source=data/raw/test_word.docx, page=None, mode=word
   preview=公司部门人员名单测试 Word 文档
3. score=0.6161, source=data/raw/test_word.docx, page=None, mode=word
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4800, source=data/raw/test_word.docx, page=None, mode=word
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4460, source=data/raw/test_word.docx, page=None, mode=word, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_word.docx，文本）：
这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
（来自 data/raw/test_word.docx，文本）：
公司部门人员名单测试 Word 文档
（来自 data/raw/test_word.docx，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_word.docx，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
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
- chunk_size: 100
- overlap: 20
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.7330, source=data/raw/test_web.html, page=None, mode=web
   preview=这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
2. score=0.6402, source=data/raw/test_web.html, page=None, mode=web
   preview=公司部门人员名单测试网页
3. score=0.6161, source=data/raw/test_web.html, page=None, mode=web
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4799, source=data/raw/test_web.html, page=None, mode=web
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4459, source=data/raw/test_web.html, page=None, mode=web, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_web.html，文本）：
这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
（来自 data/raw/test_web.html，文本）：
公司部门人员名单测试网页
（来自 data/raw/test_web.html，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_web.html，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
```


## Chunk size = 300

# Multi-format Retrieval Eval

## Config

- time: 2026-07-02T16:55:25
- query: 这个文档是用来测试什么功能的？
- top_k: 5
- chunk_size: 300
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
- chunk_size: 300
- overlap: 50
- rows_per_chunk: 2
写入完成，共 3 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.6659, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
2. score=0.4459, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20
3. score=0.4081, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 王五 财务部 2022-11-08

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

用户问题：这个文档是用来测试什么功能的？
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
- chunk_size: 300
- overlap: 50
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.7520, source=data/raw/test_word.docx, page=None, mode=word
   preview=这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
2. score=0.6255, source=data/raw/test_word.docx, page=None, mode=word
   preview=公司部门人员名单测试 Word 文档
3. score=0.6162, source=data/raw/test_word.docx, page=None, mode=word
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4799, source=data/raw/test_word.docx, page=None, mode=word
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4460, source=data/raw/test_word.docx, page=None, mode=word, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_word.docx，文本）：
这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
（来自 data/raw/test_word.docx，文本）：
公司部门人员名单测试 Word 文档
（来自 data/raw/test_word.docx，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_word.docx，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
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
- chunk_size: 300
- overlap: 50
- rows_per_chunk: 2
写入完成，共 7 条记录
```

### Retrieval

```text
=== Top-k 召回调试信息 ===
1. score=0.7329, source=data/raw/test_web.html, page=None, mode=web
   preview=这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
2. score=0.6403, source=data/raw/test_web.html, page=None, mode=web
   preview=公司部门人员名单测试网页
3. score=0.6161, source=data/raw/test_web.html, page=None, mode=web
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4799, source=data/raw/test_web.html, page=None, mode=web
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4460, source=data/raw/test_web.html, page=None, mode=web, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_web.html，文本）：
这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
（来自 data/raw/test_web.html，文本）：
公司部门人员名单测试网页
（来自 data/raw/test_web.html，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_web.html，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
```


## Chunk size = 500

# Multi-format Retrieval Eval

## Config

- time: 2026-07-02T16:56:11
- query: 这个文档是用来测试什么功能的？
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
=== Top-k 召回调试信息 ===
1. score=0.6659, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
2. score=0.4460, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20
3. score=0.4081, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 王五 财务部 2022-11-08

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

用户问题：这个文档是用来测试什么功能的？
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
=== Top-k 召回调试信息 ===
1. score=0.7520, source=data/raw/test_word.docx, page=None, mode=word
   preview=这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
2. score=0.6255, source=data/raw/test_word.docx, page=None, mode=word
   preview=公司部门人员名单测试 Word 文档
3. score=0.6161, source=data/raw/test_word.docx, page=None, mode=word
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4800, source=data/raw/test_word.docx, page=None, mode=word
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4460, source=data/raw/test_word.docx, page=None, mode=word, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_word.docx，文本）：
这是一份测试用 Word 文档，用来验证 Word 解析模块的正文和表格提取功能。
（来自 data/raw/test_word.docx，文本）：
公司部门人员名单测试 Word 文档
（来自 data/raw/test_word.docx，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_word.docx，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
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
=== Top-k 召回调试信息 ===
1. score=0.7331, source=data/raw/test_web.html, page=None, mode=web
   preview=这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
2. score=0.6403, source=data/raw/test_web.html, page=None, mode=web
   preview=公司部门人员名单测试网页
3. score=0.6161, source=data/raw/test_web.html, page=None, mode=web
   preview=补充说明：以上数据为测试用途，不代表真实人员信息。
4. score=0.4799, source=data/raw/test_web.html, page=None, mode=web
   preview=下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。
5. score=0.4459, source=data/raw/test_web.html, page=None, mode=web, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15 李四 市场部 2023-03-20

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
（来自 data/raw/test_web.html，文本）：
这是一份测试用网页，用来验证 Web 解析模块的正文和表格提取功能。
（来自 data/raw/test_web.html，文本）：
公司部门人员名单测试网页
（来自 data/raw/test_web.html，文本）：
补充说明：以上数据为测试用途，不代表真实人员信息。
（来自 data/raw/test_web.html，文本）：
下面这张表格列出了各部门的人员信息，包括姓名、部门和入职日期三个字段。

用户问题：这个文档是用来测试什么功能的？
```


## Manual Observation

- chunk_size=100:
- chunk_size=300:
- chunk_size=500:
- conclusion:
