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
from pydantic import BaseModel, Field, BeforeValidator, field_validator
from typing import Literal
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")
client = Groq(
    api_key=my_api_key
)





class Vision_Class(BaseModel):
    description: str = Field(description="A description of the handwritten image content.")
    latex: str = Field(description="The mathematical latex representation string.")
    type: Literal["equation", "geometry", "diagram"]

    # Pre-validate the field to coerce numbers into strings smoothly
    @field_validator("latex", mode="before")
    @classmethod
    def coerce_number_to_string(cls, value):
        if isinstance(value, (int, float)):
            return str(value)
        return value

#tools
@tool
def Ai_Draw(image_base64:str, x_min:int, y_min:int, x_max:int, y_max:int, feedback_text:str) ->str:
    """
    Draws a red highlight box and feedback text directly onto the student's image.
    Returns the newly annotated image as a base64 string.
    """
    return src.vision.draw_img(image_base64, x_min, y_min, x_max, y_max, feedback_text)
    
Avaiable_Tools = [Ai_Draw]

# Logic Engine for APP
class MathTutorEngine():

    def __init__(self, model =("qwen/qwen3.6-27b")):
        self.llm = ChatGroq(model=model, temperature=0, max_tokens=1000,api_key=my_api_key, reasoning_format="hidden")
        self.chat_history = src.convo_hist.Conversation(trigger_function=self.tutor)
        self.tutor_agent = create_agent(model=self.llm, tools=Avaiable_Tools, system_prompt=prompts.TUTOR_PROMPT)
        
    #Get intial guiding question
    def get_opening_question(self, problem):
        print(problem)
        response = self.llm.invoke(prompts.OPENING_QUESTION_PROMPT.format(problem=problem))
        print(response.content)
        self.chat_history.add_tutor(response.content)
        return response.content, response.content
    
    #Checks if user's answer was correct
    def vision(self, img_data):
        #Validate and provide visual feedback on mistakes
        structured_output = self.llm.with_structured_output(Vision_Class)
        
        message= HumanMessage(
        content=[
            {
                "type": "text",
                "text": "Analyze the student's handwritten mathematical work. Describe what is visible."

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
            result = structured_output.invoke([message])
            print(f"{result.description} {result.latex} {result.type}")
            vision_result = {
                "type": result.type,
                "latex": result.latex,
                "description": result.description
            }
            self.chat_history.add_vision(vision_result)
            

        except Exception as e:
            try:
                print("Error Occured+" + str(e))
                result = self.llm.invoke([message])
                response_text = getattr(result, "content", str(result))
                self.chat_history.add_vision(response_text)
                return response_text

            except Exception as e:
                print("Error Occured+" + str(e))
                return "Oops Something Went Wrong 😭"

    def ask(self, input):
        return self.chat_history.add_user(input)

    def tutor(self, history):
        response = self.tutor_agent.invoke({"messages": history})
        messages = response.get("messages", [])
        if not messages:
            return "I could not generate a response."

        last_message = messages[-1]
        response_text = getattr(last_message, "content", str(last_message))
        print(response_text)
        return response_text

        
        
        

        


   
    