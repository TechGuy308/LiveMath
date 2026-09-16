from src.logic import MathTutorEngine
import gradio as gr
import os

canvas_height = 900
canvas_width = 900
css = """
body {
    background: #f5f7fb;
}

#title {
    text-align: center;
    font-size: 32px;
    font-weight: 700;
}

#workspace {
    max-width: 900px;
    margin: 0 auto;
}

#ai_output {
    min-height: 180px;
    max-height: 420px;
    overflow-y: auto;
    padding: 14px 16px;
    background: #000000;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.05),
                0 1px 3px rgba(15, 23, 42, 0.08);
    color: #1e293b;
    line-height: 1.6;
}

#ai_output::before {
    content: "AI output";
    display: block;
    margin-bottom: 8px;
    color: #64748b;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

#ai_output > :first-child {
    margin-top: 0;
}

#ai_output > :last-child {
    margin-bottom: 0;
}
"""

def message_button_function(message, brain):
    if message is not None:
        return brain.ask(message)

def vision_button_function(image, brain):
    if image is not None:
        return brain.vision(image)

def load_text(saved_state):
    return saved_state

def get_opening_question(problem, brain):
    if not problem or not problem.strip():
        question = "Please enter a math question first."
    else:
        question = str(brain.get_opening_question(problem.strip()))
        
    return question 

with gr.Blocks() as demo:
    brain_state = gr.State()
    opening_question_state = gr.State("")
    with gr.Tabs() as tabs:
        with gr.Tab("Start", id=0):
            with gr.Column(elem_id="workspace"):
                gr.Markdown("# Live Math", elem_id="title")
                gr.Markdown("Start with the problem you are working on.")
                problem_input = gr.Textbox(
                    label="Math question",
                    placeholder="Type a math problem...",
                    lines=5,
                )
                start_button = gr.Button("Start solving", variant="primary")
                
                
        with gr.Tab("Work It Out", id=1):
            gr.Markdown("# Work it out")
            opening_question_display = gr.Markdown()

            with gr.Row():
                canvas = gr.ImageEditor(
                    elem_id="my-clean-canvas",
                    canvas_size=(canvas_height, canvas_width),
                    height=500,
                    width=1000,
                    type="numpy",
                    sources=(),
                    brush=gr.Brush(colors=["#000000"]),
                    label="Your work",
                    scale=3,
                )
                    
                with gr.Column(scale=1):
                    opening_question_display
                    ai_output = gr.Markdown(value="Chats will show up here", elem_id="ai_output")
                    message_input = gr.Textbox(
                                label="User Input",
                                placeholder="Ask any quesitons you may have...",
                                lines=3,
                            )
                    message_button = gr.Button("Send", variant="primary")
                    message_button.click(
                        fn=message_button_function,
                        inputs=[message_input, brain_state],
                        outputs=ai_output
                    )

            check_button = gr.Button("Check my work", variant="primary", scale=3)
            check_button.click(
                fn=vision_button_function,
                inputs=[canvas, brain_state],
                outputs=ai_output,
            )
    start_event = start_button.click(
        fn=get_opening_question,
        inputs=[problem_input, brain_state],
        outputs=ai_output
        ).then(fn=lambda: gr.Tabs(selected=1),outputs=tabs)

    demo.load(fn=MathTutorEngine, outputs=brain_state)
    

#demo.launch(css=css)


    
if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.environ.get("PORT", 7860)),css=css
    )
