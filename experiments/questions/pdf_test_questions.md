# PDF Test Questions

## data/raw/test_table.pdf

| id  | question                             | expected_evidence            | expected_source         | notes              |
| --- | ------------------------------------ | ---------------------------- | ----------------------- | ------------------ |
| Q1  | 张三在哪个部门？                     | 张三 技术部                  | data/raw/test_table.pdf | 测表格行召回       |
| Q2  | 李四的入职日期是什么？               | 李四 2023-03-20              | data/raw/test_table.pdf | 测同一行列绑定     |
| Q3  | 这份文档的数据是否代表真实人员信息？ | 测试用途，不代表真实人员信息 | data/raw/test_table.pdf | 测表格后说明文字   |
| Q4  | 王五的直属主管是谁？                 | 找不到答案依据               | data/raw/test_table.pdf | 测无依据时是否拒答 |
