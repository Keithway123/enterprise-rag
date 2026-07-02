"""
chunking.py — 分块模块

设计决策（来自我们的讨论，别忘了为什么这样设计）：
1. chunk_size 和 overlap 都作为参数传入，不写死在代码里——
   Week 5 要做"调参对比实验"，必须能灵活换数字测试。
2. 分块逻辑不关心文本来自什么格式（PDF/Word/网页）——
   这是我们在规划项目结构时就确认过的判断："分块只处理纯文本，跟来源格式无关"。
3. 优先尝试按句子/段落边界切，但如果一段太长、太混杂，允许在不完美的位置强制切——
   "块越大、越可能混杂多个主题，向量就越模糊"，这是分块要避免的核心风险。
4. overlap 的作用：防范切割点恰好落在关键信息正中间，导致两边都不完整。
"""


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    把一段长文本切成多个块。

    Args:
        text: 待分块的纯文本（已经是解析阶段处理完的纯文本，不关心它原本是 PDF/Word/网页）
        chunk_size: 每块的最大字数
        overlap: 相邻两块之间重叠的字数

    Returns:
        一个字符串列表，每个元素是一个文本块

    思考第一步：最简单的"按固定字数切"，思路是什么？
    假设 text 总共有 1000 个字，chunk_size=300，overlap=50——
    第一块该是 text 的第几个字到第几个字？第二块的起始位置，
    应该比第一块的起始位置往后移动多少？（提示：往后移动的距离，
    应该是 chunk_size，还是 chunk_size - overlap？想清楚这两者的区别，
    这是这个函数最核心的一步，决定了"重叠"到底有没有真正生效）

    思考第二步：循环什么时候停止？当"下一块的起始位置"已经
    超出了 text 的总长度时，应该怎么处理？
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size 必须大于 0")
    if overlap < 0:
        raise ValueError("overlap 不能是负数")
    if overlap >= chunk_size:
        raise ValueError("overlap 必须小于 chunk_size，否则下一块不会向前推进")

    chunks = []
    start = 0  # 当前块的起始位置，从 0 开始

    while start < len(text):
        end = start + chunk_size  # 当前块的结束位置
        chunk = text[start:end]   # 切片，取出这一块的内容（超出范围会自动截断，不会报错）
        chunks.append(chunk)

        # 下一块的起始位置 = 当前块结束位置 - 重叠字数
        # 这样保证相邻两块之间，恰好有 overlap 个字符是重复的
        start = end - overlap

    return chunks

def chunk_table(table_data:list[list], rows_per_chunk:int) -> list[list[list]]:
    if rows_per_chunk <= 0:
        raise ValueError("rows_per_chunk 必须大于 0")

    if not table_data:
        return []

    header = table_data[0]
    data_rows = table_data[1:]

    if not data_rows:
        return []

    chunks = []
    start_row = 0

    while start_row < len(data_rows):
        end_row = start_row + rows_per_chunk
        chunk_rows = data_rows[start_row:end_row]
        chunks.append([header] + chunk_rows)
        start_row = end_row

    return chunks


if __name__ == "__main__":
    # 用一段简单、可预测的文本测试，方便你肉眼数清楚每块的内容对不对
    test_text = "".join([str(i % 10) for i in range(100)])  # "0123456789012345..." 共 100 个字符
    print("原始文本长度:", len(test_text))
    print("原始文本:", test_text)
    print()

    chunks = chunk_text(test_text, chunk_size=30, overlap=5)
    for i, chunk in enumerate(chunks, start=1):
        print(f"块 {i} (长度 {len(chunk)}): {chunk}")
