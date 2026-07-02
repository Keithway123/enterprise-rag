# PDF RAG Eval Run

## Config

- questions_file: experiments\questions\pdf_test_questions.json
- dataset: data/raw/test_table.pdf
- top_k: 5

## Q1: 张三在哪个部门？

### Expected

- expected_evidence: 张三 技术部
- expected_source: data/raw/test_table.pdf
- notes: 测表格行召回

### Retrieval Trace

```text
1. score=0.7561, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
2. score=0.5478, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
3. score=0.5443, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
```

### Final Prompt

```text
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
姓名 部门 入职日期
张三 技术部 2023-01-15
李四 市场部 2023-03-20
王五 财务部 2022-11-08
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门。

用户问题：张三在哪个部门？
```

### Answer

```text
根据材料内容，张三在**技术部**。

（来源：data/raw/test_table.pdf 第1页）
```

## Q2: 李四的入职日期是什么？

### Expected

- expected_evidence: 李四 2023-03-20
- expected_source: data/raw/test_table.pdf
- notes: 测同一行列绑定

### Retrieval Trace

```text
1. score=0.6590, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
2. score=0.5313, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
3. score=0.5194, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
```

### Final Prompt

```text
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
姓名 部门 入职日期
张三 技术部 2023-01-15
李四 市场部 2023-03-20
王五 财务部 2022-11-08
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门。

用户问题：李四的入职日期是什么？
```

### Answer

```text
李四的入职日期是2023-03-20。

来源：data/raw/test_table.pdf 第1页。
```

## Q3: 这份文档的数据是否代表真实人员信息？

### Expected

- expected_evidence: 测试用途，不代表真实人员信息
- expected_source: data/raw/test_table.pdf
- notes: 测表格后说明文字

### Retrieval Trace

```text
1. score=0.6717, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
2. score=0.5492, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
3. score=0.5344, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
```

### Final Prompt

```text
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
姓名 部门 入职日期
张三 技术部 2023-01-15
李四 市场部 2023-03-20
王五 财务部 2022-11-08
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门。

用户问题：这份文档的数据是否代表真实人员信息？
```

### Answer

```text
根据材料内容，这份文档的数据**不代表**真实人员信息。

来源：data/raw/test_table.pdf 第1页，文本（补充说明：以上数据为测试用途,不代表真实人员信息。）
```

## Q4: 王五的直属主管是谁？

### Expected

- expected_evidence: 找不到答案依据
- expected_source: data/raw/test_table.pdf
- notes: 测无依据时是否拒答

### Retrieval Trace

```text
1. score=0.5866, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=2
   preview=姓名 部门 入职日期 李四 市场部 2023-03-20 王五 财务部 2022-11-08
2. score=0.4386, source=data/raw/test_table.pdf, page=1, mode=table
   preview=公司部门人员名单测试文档 这是一份测试用文档,用来验证 PDF 解析模块的表格提取功能。下面这张表格列出了各部门的人员信 息,包括姓名、部门和入职日期三个字段。表格之后还有一段补充说明文字,用来测试 mode='table' 模式下,表格之
3. score=0.4383, source=data/raw/test_table.pdf, page=1, mode=table, table=1, table_chunk=1
   preview=姓名 部门 入职日期 张三 技术部 2023-01-15
```

### Final Prompt

```text
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
姓名 部门 入职日期
张三 技术部 2023-01-15
李四 市场部 2023-03-20
王五 财务部 2022-11-08
补充说明：以上数据为测试用途,不代表真实人员信息。如需更新人员变动,请联系人事部门。

用户问题：王五的直属主管是谁？
```

### Answer

```text
找不到答案依据。
```
