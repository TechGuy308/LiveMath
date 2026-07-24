
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
import src.prompts as prompts
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import json

#Store JSON data
class Validate_Class(BaseModel):
    is_correct: bool
    feedback: str | None = None  
    x_coord: int | None = None  
    y_coord: int | None = None  

class MathTutorEngine():
    # Logic Engine for APP

    def __init__(self, model =("phi3:mini")):
        self.llm = OllamaLLM(model=model, temperature=0, num_predict=150)
        self.memory = ChatMessageHistory()
        

    #Get intial guiding question
    def get_opening_question(self, problem):
        return self.llm.invoke(prompts.OPENING_QUESTION_PROMPT.format(problem=problem))
    
    #Checks if user's answer was correct
    def validate_answer_with_feedback(self, init_problem, ai_gen_question, reasoning, vision_feedback):
        #Validate and provide visual feedback on mistakes
        result = self.llm.invoke(prompts.VALIDATE_USER_REPONSE.format(problem=init_problem, question=ai_gen_question, vision_feedback=vision_feedback, reasoning=reasoning))
        try:
            validation_data = Validate_Class.model_validate_json(result)
            
            return validation_data

        except Exception as e:
            #For if LLM returns invalid JSON
            print(e)
            
            validation_data = Validate_Class(is_correct=False, feedback="Error Invalid Json", x_coord=0, y_coord=0)
            return validation_data

        
        
        
    #Get Next guiding question If USer was Correct
    def _format_history(self):
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a Socratic tutor for: {problem}"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{user_input}")])

    def get_next_question(self, problem):
        """Generate next question based on conversation history"""
        history = self._format_history()  # Fresh format each time
        
        prompt = f"""Problem: {problem}

    Conversation history so far:
    {history}

    Based on what the student has answered so far, generate the NEXT guiding question.
    Make it build on what they've established.
    Keep it under 25 words.

    Question:"""
        
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
        
        # Optional: log to file for debugging
        with open('conversation_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"Tutor: {question}\n")
            f.write(f"Student: {answer}\n\n")
        
       
    def reset(self):
        """Clear conversation for new problem"""
        self.memory.clear()

    def Ai_Interactions(self,json_data):
        # Handles How the AI interacts with the user. ie. reponses, hints, highight mistakes.
        if json_data.is_correct:
            return "CORRECT", None, None
        elif json_data.feedback == "Error Invalid Json":
            return None,"INVALID JSON. PLEASE SUBMIT AGAIN", None
        else:
            wrong = json_data.is_correct
            hint = json_data.feedback

            square = {
                "type": "rect",
                "left": json_data.x_coord,
                "top": json_data.y_coord,
                "width": 100,
                "height": 100,
                "fill": "rgba(255, 0, 0, 0.01)",
                "stroke": "red",
                "strokeWidth": 0
            }
        return wrong, hint, square
    