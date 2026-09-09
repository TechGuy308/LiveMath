#Manage conversation history

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

class Conversation():
    def __init__(self, trigger_function):
        self.memory = []
        self.trigger_function = trigger_function

    def trigger(self):
        return self.trigger_function(self.memory)

    def add_tutor(self, message):
        self.memory.append(AIMessage(content=message))

    def add_vision(self, message):
        self.memory.append(
        HumanMessage(content=f"[VISION OBSERVATION]\n{message}"))
        return self.trigger()

    def add_user(self, message):
        self.memory.append(HumanMessage(content=message))
        return self.trigger()

    
        