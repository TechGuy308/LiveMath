from src.logic import MathTutorEngine
import gradio as gr

canvas_height = 900
canvas_width = 900
Brain = MathTutorEngine()
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
"""

def message_button_function(message):
    if message is not None:
        return Brain.ask(message)

def vision_button_function(image):
    if image is not None:
        return Brain.vision(image)

def load_text(saved_state):
    return saved_state

def get_opening_question(problem):
    if not problem or not problem.strip():
        question = "Please enter a math question first."
    else:
        question = str(Brain.get_opening_question(problem.strip()))
        
    return question 

with gr.Blocks() as demo:
    question = ""
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
                start_event = start_button.click(
                        fn=get_opening_question,
                        inputs=problem_input,
                        outputs=opening_question_state
                    ).then(
                        fn=lambda: gr.Tabs(selected=1),
                        outputs=tabs,
                    )
                
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
                        inputs=message_input,
                        outputs=ai_output
                    )

            check_button = gr.Button("Check my work", variant="primary", scale=3)
            check_button.click(fn=vision_button_function, inputs=canvas, outputs=ai_output)
    start_event = start_button.click(
        fn=get_opening_question,
        inputs=problem_input,
        outputs=ai_output
        )
    

    

    

demo.launch(css=css)