from sympy import sympify, simplify, solve, symbols

from langchain_ollama import OllamaLLM

from langchain_core.prompts import PromptTemplate


from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class MathTutorEngine():
    # Logic Engine for APP

    def __init__(self, model ="phi3:mini"):
        self.llm = OllamaLLM(model=model)
        self.memory = ChatMessageHistory()
        self.convo_hist = ""

    def get_opening_question(self, problem):
        
        prompt = f"""Problem: {problem}

    Ask one guiding question to help a student solve this.
    Remember this is Stage 1, so it should be a very simple, short question.
    Make it ask them to identify/extract/recognize something fundamental.
    Examples: "What are the known values?", "What are we solving for?"

    Question:"""
        return self.llm.invoke(prompt)
    
    def validate_answer(self, problem, question, user_answer):
        """Check if answer is correct"""
        prompt = f"""Problem: {problem}
        Question asked: {question}
        Student answer: {user_answer}

        Is this answer correct for answering the question?
        Respond ONLY with: CORRECT / INCOMPLETE / WRONG"""
        
        result = self.llm.invoke(prompt)
        return "CORRECT" in result
    
    #Get Next Question If USer was Correct
    def get_next_question(self, problem):
        """Generate next question based on conversation history"""

        
        for msg in self.memory.messages:
            role = "Student" if isinstance(msg, HumanMessage) else "Tutor"
            self.convo_hist += f"{role}: {msg.content}\n"
        prompt = f"""Problem: {problem}

        Conversation history so far:
        {self.convo_hist}

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
    
    def reset(self):
        """Clear conversation for new problem"""
        self.memory.clear()