
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage


class MathTutorEngine():
    # Logic Engine for APP

    def __init__(self, model =("phi3:mini")):
        self.llm = OllamaLLM(model=model, temperature=0, num_predict=150)
        self.memory = ChatMessageHistory()
        self.convo_hist = ""

    #Get intial guidning question
    def get_opening_question(self, problem):
        
        prompt = f"""

    You are an expert physics tutor using the Socratic method.

        The student has just been given this problem:
        {problem}

        Your goal:
        Ask the BEST first question to help the student start thinking. (Remember the goal is to let the student figrure things out themselves)

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

        Do not congratulate the student. 
        Do not summarize the laws of physics. 
        Keep it under 25 words.
        
        Return ONLY: Question:"""
        return self.llm.invoke(prompt)
    
    #Checks if user's answer was correct
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
    
    #Get Next guiding question If USer was Correct
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

    #Checks if the problem is complete
    def check_problem_complete(self, problem):
        """Check if problem is fully solved"""
        prompt = f"""Problem: {problem}

        Conversation history:
        {self.convo_hist}

        Based on this conversation, has the student completely solved the problem?
        Respond ONLY with: YES / NO"""
        
        result = self.llm.invoke(prompt)
        return "YES" in result
    
    #Saves chat history
    def save_exchange(self, question, answer):
        """Save Q&A to conversation history"""
        self.memory.add_ai_message(question)
        self.memory.add_user_message(answer)
        for msg in self.memory.messages:
            role = "Student" if isinstance(msg, HumanMessage) else "Tutor"
            
        self.convo_hist += f"{role}: {msg.content}\n"
        file_path = 'my_new_file.txt'
        with open(file_path, "r+") as file:
            file.truncate(0)
        with open(file_path, 'a', encoding='utf-8') as file:
                file.write(str(self.convo_hist))
                print(f"File '{file_path}' created and written successfully.")
        
       
    def reset(self):
        """Clear conversation for new problem"""
        self.memory.clear()

    def Ai_Draw(self,canvas_height=600,canvas_width=1200):
        prompt = f"""
                    The student drew an image or equation at these coordinates:
                    Your job is the return the coordinates of their mistake so that it can be highlighted.

                    Return this JSON:
                    {{
                        "highlight_coords": [400, 300] 
                    }}"""
        
        result = self.llm.invoke(prompt)
        square = {
            "type": "rect",
            "left": 900,
            "top": 780,
            "width": 100,
            "height": 100,
            "fill": "rgba(255, 0, 0, 0.01)",
            "stroke": "red",
            "strokeWidth": 0
        }
        return square
    