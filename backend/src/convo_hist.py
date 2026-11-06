#Manage conversation history

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class Conversation():
    def __init__(self, trigger_function):
        self.memory = []
        self.trigger_function = trigger_function
        
    #Trigger the function to generate a response from the tutor agent based on the conversation history
    def trim_memory(self):
        value = self.memory + []
        if len(value) > 10:
            value2 = value[-(len(value)-(len(value)-10)):]
            value2.insert(0, value[0])
            return value2
        else:
            return value
        
    async def trigger(self):
        return await self.trigger_function(self.trim_memory())

    def add_tutor(self, message):
        self.memory.append(AIMessage(content=message))

    async def add_vision(self, message):
        self.memory.append(
        HumanMessage(content=f"[VISION OBSERVATION]\n{message}"))
        return await self.trigger()

    async def add_user(self, message):
        self.memory.append(HumanMessage(content=message))
        return await self.trigger()
    
    def add_system(self, message):
        self.memory.append(SystemMessage(content=message))
            

    
        