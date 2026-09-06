#Manage conversation history

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage

class Conversation():
    def __init__(self):
        self.memory = []

    def add_tutor(self, ai_message):
        self.memory.append({"role": "TUTOR MODEL", "content": ai_message})
    def add_vision(self, img_message):
        self.memory.append({"role": "VISION MODEL", "content": img_message})

    def add_user(self, user_message):
        self.memory.append({"role": "User", "content": user_message})

    def add_tool(self, tool):
        self.memory.append({
            "role": "tool_caller",
            "tool": tool
        })
    def add_system(self, message):
        self.memory.append({
            "role": "System",
            "message": str(message)
        })

    def get_messages(self):
        return self.memory
        