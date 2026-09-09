from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="phi3")
template= """
Answer the question below

Here is the chat history: {context}
Question:{question}

Answer:
"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt|model


def chat_history():
    context = ""
    print("Hello")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = chain.invoke({"context":"","question":input("enter prompt:")})
        print("Bot: ", result)
        context += f"\nUser: {user_input}\nAi: {result}"


Pizza= """
Analyze this image as a mathematical and scientific visual.
Extract and identify ALL mathematically relevant information that is visibly present, including:

- Mathematical equations and expressions
- Geometry: angles, lengths, shapes, points, lines, parallel/perpendicular relationships
- Graphs and charts: axes, labels, coordinates, functions, trends, data points
- Tables: headers, rows, columns, values, and relationships
- Diagrams: objects, arrows, vectors, forces, labels, and spatial relationships
- Handwritten calculations and the order in which they appear
- The student's work and any apparent intermediate steps

Transcribe mathematical expressions accurately using LaTeX.
Preserve spatial relationships and distinguish between the original problem and the student's work.

Do not solve the problem.
Do not correct the student's work.
Do not infer information that is not visibly present.

Return a clear, concise description of the mathematical content.
"""

Pizza2='''def handle_submission(image_dict):
    # 1. Process or save what the user drew
    user_drawing = image_dict["composite"]
    print("Saved user drawing data shape:", user_drawing.shape)
    
    # 2. Prepare the new canvas dictionary structure
    new_canvas_value = {
        "background": NEW_BACKGROUND_URL,
        "layers": [],  # Clear the canvas layers so they don't overlay on the new image
        "composite": None
    }
    
    # 3. Return gr.update() to change the value of the ImageEditor dynamically
    return gr.update(value=new_canvas_value)

with gr.Blocks() as demo:
    canvas = gr.ImageEditor(
        value=blank_canvas,
        sources=(), 
        brush=gr.Brush(colors=["#FF0000"]), # Red brush for visibility
        label="Drawing Canvas"
    )
    btn = gr.Button("Submit & Change Background")
    
    # Notice that the output target is the canvas component itself
    btn.click(fn=handle_submission, inputs=canvas, outputs=canvas)

if __name__ == "__main__":
    demo.launch()'''