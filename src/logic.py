from sympy import sympify, simplify, solve, symbols

from langchain_ollama import OllamaLLM

from langchain_core.prompts import PromptTemplate


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class MathTutorEngine():
    # Logic Engine for APP

    def __init__(self, model ="llama3.2:1b"):
        self.llm = OllamaLLM(model=model)
        self.memory = ChatMessageHistory()
        self.convo_hist = ""

    def get_opening_question(self, problem):
        
        prompt = f"""

    You are an expert physics tutor using the Socratic method.

        The student has just been given this problem:
        {problem}

        Your goal:
        Ask the BEST first question to help the student start thinking.

        Guidelines:
        - Ask only ONE question
        - Do NOT solve the problem
        - Do NOT list steps
        - Do NOT be generic unless appropriate
        - Focus on helping the student identify how to begin

        Good starting directions:
        - identifying known values
        - identifying what is being solved
        - identifying the type of problem (motion, forces, etc.)
        - identifying relevant relationships

        
        
        Return ONLY: Question:"""
        return self.llm.invoke(prompt)
    
    def validate_answer(self, problem, question, user_answer):
        """Check if answer is correct"""
        prompt = f"""Problem: {problem}
        Question asked: {question}
        Student answer: {user_answer}

        Is this answer correct for answering the question?
        Respond ONLY with: CORRECT  / WRONG"""
        
        result = self.llm.invoke(prompt)
        print(prompt)
        print(result)
        return "CORRECT" in result
    
    #Get Next Question If USer was Correct
    def get_next_question(self, problem):
        """Generate next question based on conversation history"""

        
        for msg in self.memory.messages:
            role = "Student" if isinstance(msg, HumanMessage) else "Tutor"
            self.convo_hist += f"{role}: {msg.content}\n"
        
    
        prompt = f"""Problem: {problem}

        Conversation history so far:
        {self.memory.messages}

        Based on what the student has answered so far, generate the NEXT guiding question.
        Make it build on what they've established.

        Next Question:"""
        
        return self.llm.invoke(prompt)
    
    def check_problem_complete(self, problem):
        """Check if problem is fully solved"""
        prompt = f"""Problem: {problem}

        Conversation history:
        {self.convo_hist}

        Based on this conversation, has the student completely solved the problem?
        Respond ONLY with: YES / NO"""
        
        result = self.llm.invoke(prompt)
        return "YES" in result
    
    def save_exchange(self, question, answer):
        """Save Q&A to conversation history"""
        self.memory.add_ai_message(question)
        self.memory.add_user_message(answer)
        for msg in self.memory.messages:
            role = "Student" if isinstance(msg, HumanMessage) else "Tutor"
            self.convo_hist += f"{role}: {msg.content}\n"
        file_path = 'my_new_file.txt'
        with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(self.convo_hist))
                print(f"File '{file_path}' created and written successfully.")
        
       
    def reset(self):
        """Clear conversation for new problem"""
        self.memory.clear()