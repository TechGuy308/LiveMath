from langchain.agents import create_agent
import src.prompts as prompts
from langchain_groq import ChatGroq
from langchain.tools import tool
from dotenv import load_dotenv
import os
import src.vision
import src.convo_hist
from langchain_core.messages import HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from pydantic import BaseModel
from typing import Literal
from groq import Groq





load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key=my_api_key
)
#tools
chat_history = src.convo_hist.Conversation()



@tool
def Ai_Draw(image_base64:str, x_min:int, y_min:int, x_max:int, y_max:int, feedback_text:str) ->str:
    """
    Draws a red highlight box and feedback text directly onto the student's image.
    Returns the newly annotated image as a base64 string.
    """
    return src.vision.draw_img(image_base64, x_min, y_min, x_max, y_max, feedback_text)
    
Avaiable_Tools = [Ai_Draw]

class MathTutorEngine():
    # Logic Engine for APP

    def __init__(self, model =("qwen/qwen3.6-27b")):
        self.llm = ChatGroq(model=model, temperature=0, max_tokens=1000,api_key=my_api_key, reasoning_format="hidden")
        
        self.tutor_agent = create_agent(model=self.llm, tools=Avaiable_Tools, system_prompt=prompts.TUTOR_PROMPT)
        
    #Get intial guiding question
    def get_opening_question(self, problem):
        response = self.llm.invoke(prompts.OPENING_QUESTION_PROMPT.format(problem=problem))
        return response
    
    #Checks if user's answer was correct
    def vision(self, img_data):
        #Validate and provide visual feedback on mistakes
        
        message= HumanMessage(
        content=[
            {
                "type": "text",
                "text": ""#prompts.VISION_PROMPT
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": src.vision.processImage(img_data.get("composite", None))
                }
            }
        ]
    )

        try:
            
            result = self.llm.invoke([message])
            print(result.content)
            return result

        except Exception as e:
            #For if LLM returns invalid JSON
            print(e)

            validation_data = "Hello Error Occured"
            return validation_data
    def tutor(self, prompt):
        pass

        
        
        

        


   
    