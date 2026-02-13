"""Gradio UI skeleton for local operator experience."""

import gradio as gr


class TutorUI:
    """Thin UI layer that delegates answering to FastAPI backend."""

    def __init__(self, api_base_url: str) -> None:
        self.api_base_url = api_base_url

    def ask(self, question: str, mode: str, top_k: int):
        """Call backend /query endpoint and return answer + source payload."""
        raise NotImplementedError

    def build(self) -> gr.Blocks:
        """Build a local Gradio app with retrieval mode and top-k controls."""
        with gr.Blocks() as app:
            gr.Markdown("# Dataiku Tutor Assistant")
            query_input = gr.Textbox(label="Ask a Dataiku question", lines=3)
            mode = gr.Radio(choices=["semantic", "keyword", "hybrid"], value="hybrid", label="Retrieval mode")
            top_k = gr.Slider(minimum=1, maximum=15, value=5, step=1, label="Top-k chunks")
            submit = gr.Button("Ask")

            output = gr.Markdown(label="Step-by-step answer")
            sources = gr.JSON(label="Documentation sources")

            submit.click(fn=self.ask, inputs=[query_input, mode, top_k], outputs=[output, sources])

        return app
