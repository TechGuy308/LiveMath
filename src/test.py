from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="phi3")
template= """
Answer the question below

Here is the chat history: {context}
Question:{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt|model


def chat_history():
    context = ""
    print("Hello")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"context":"","question":input("enter prompt:")})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAi: {result}"

