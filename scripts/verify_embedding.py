"""
实验脚本：验证"分块切割点是否完整"对检索相似度的实际影响。

设计思路：
- 用户问题、完整句子、被切断的残句，三段文字分别生成向量
- 计算"问题 vs 完整句子"和"问题 vs 残句"的余弦相似度
- 对比两个数字，把"切断会让效果变差"这个直觉变成实测数据

环境要求：.env 文件里要有 DASHSCOPE_API_KEY
"""

import os
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


def get_embedding(text: str) -> list[float]:
    """
    调用阿里百炼 Embedding API，把一段文字转换成向量。

    提示：client.embeddings.create(...) 这个方法需要传入
    model（用 "text-embedding-v3"）、input（要转换的文字）、
    dimensions（向量维度，跟 CLAUDE.md 里定的保持一致，1024）

    返回值结构：response.data[0].embedding 这个路径下，
    存放着真正的向量（一个数字列表）
    """
    response =client.embeddings.create(
        model="text-embedding-v3",
        input=text,
        dimensions=1024
    )

    result = response.data[0].embedding

    return result

def cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    计算两个向量的余弦相似度。

    公式：cos(θ) = (A·B) / (|A| × |B|)
    用 numpy 实现：
    - A·B（点积）：np.dot(vec_a, vec_b)
    - |A|（向量的长度/模）：np.linalg.norm(vec_a)
    """
    
    result = np.dot(vec_a,vec_b) /(np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return result

if __name__ == "__main__":
    question = "年假需要提前几天申请？"
    complete_sentence = "年假需提前3个工作日向直属主管申请，经批准后方可休假。"
    broken_sentence = "年假需提前3个工作"

    question_vec = get_embedding(question)
    complete_vec = get_embedding(complete_sentence)
    broken_vec = get_embedding(broken_sentence)

    sim_complete = cosine_similarity(question_vec, complete_vec)
    sim_broken = cosine_similarity(question_vec, broken_vec)

    print(f"问题: {question}")
    print(f"完整句子: {complete_sentence}")
    print(f"残句: {broken_sentence}")
    print()
    print(f"问题 vs 完整句子 的相似度: {sim_complete:.4f}")
    print(f"问题 vs 残句     的相似度: {sim_broken:.4f}")
    print(f"差距: {sim_complete - sim_broken:.4f}")