from app.llm import generate_answer

answer = generate_answer("请只回答两个字：你好")

print(answer)

if __name__ == "__main__":
    main()