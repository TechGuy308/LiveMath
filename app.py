from src.logic import MathTutorEngine
import gradio as gr

canvas_height = 700
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

def load_text(saved_state):
    return saved_state


def get_opening_question(problem):
    if not problem or not problem.strip():
        question = "Please enter a math question first."
    else:
        question = str(Brain.get_opening_question(problem.strip()))

    return question


with gr.Blocks() as demo:
    opening_question_state = gr.State("")

    with gr.Column(elem_id="workspace"):
        gr.Markdown("# Live Math", elem_id="title")
        gr.Markdown("Start with the problem you are working on.")
        problem_input = gr.Textbox(
            label="Math question",
            placeholder="Type a math problem...",
            lines=5,
        )
        start_button = gr.Button("Start solving", variant="primary", link="/second")

    start_button.click(
        fn=get_opening_question,
        inputs=problem_input,
        outputs=opening_question_state,
    )

with demo.route("Second Page", "/second"):
    gr.Markdown("# Work it out")
    opening_question_display = gr.Markdown()

    with gr.Row():
        canvas = gr.ImageEditor(
            elem_id="my-clean-canvas",
            canvas_size=(canvas_width, canvas_height),
            height=500,
            width=1000,
            type="numpy",
            sources=(),
            brush=gr.Brush(colors=["#000000"]),
            label="Your work",
            scale=3,
        )
        with gr.Column(scale=1):
            gr.Markdown("### AI feedback")
            ai_output = gr.Textbox(
                label="",
                lines=8,
                interactive=False,
                placeholder="Loading..."
            )
            message_input = gr.Textbox(
                        label="User Input",
                        placeholder="Ask any quesitons you may have...",
                        lines=3,
                    )
            message_button = gr.Button("Send", variant="primary")
            message_button.click(
                fn=Brain.ask,
                inputs=message_input,
                outputs=ai_output
            )

    check_button = gr.Button("Check my work", variant="primary", scale=3)
    check_button.click(fn=Brain.vision, inputs=canvas, outputs=ai_output)

    demo.load(
        fn=load_text,
        inputs=opening_question_state,
        outputs=ai_output,
    )

demo.launch(css=css)