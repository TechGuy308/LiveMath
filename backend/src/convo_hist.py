#Manage conversation history

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

class Conversation():
    def __init__(self, trigger_function):
        self.memory = []
        self.trigger_function = trigger_function
        
    
    def trim_memory(self):
        memory_snapshot = self.memory + []
        if len(memory_snapshot) > 10:
            # Keep the original question alongside the ten most recent messages.
            recent_messages = memory_snapshot[-(len(memory_snapshot)-(len(memory_snapshot)-10)):]
            recent_messages.insert(0, memory_snapshot[0])
            return recent_messages
        else:
            return memory_snapshot
    #Trigger the function to generate a response from the tutor agent based on the conversation history
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
            

    
        