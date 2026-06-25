import os
import gradio as gr
from llama_index.readers.file import PDFReader
from llama_index.core import VectorStoreIndex

# Set OpenAI API key directly inside the program
os.environ["OPENAI_API_KEY"] = "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"

# Custom premium CSS for styling
custom_css = """
body {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 2rem !important;
}
.header {
    text-align: center;
    margin-bottom: 2rem;
}
.header h1 {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, #58a6ff 0%, #bc8cff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.header p {
    font-size: 1.1rem;
    color: #8b949e;
}
.card {
    background: rgba(22, 27, 34, 0.7);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 12px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    margin-bottom: 1rem;
}
.status-msg {
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 500;
    margin-top: 1rem;
}
.status-waiting {
    background-color: rgba(240, 135, 0, 0.1);
    border: 1px solid rgba(240, 135, 0, 0.3);
    color: #f08700;
}
.status-success {
    background-color: rgba(46, 160, 67, 0.15);
    border: 1px solid rgba(46, 160, 67, 0.3);
    color: #3fb950;
}
.status-error {
    background-color: rgba(248, 81, 73, 0.15);
    border: 1px solid rgba(248, 81, 73, 0.3);
    color: #f85149;
}
.quick-btn {
    background-color: #21262d !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
    border-radius: 6px !important;
}
.quick-btn:hover {
    background-color: #30363d !important;
    border-color: #8b949e !important;
    transform: translateY(-1px);
}
"""

def initialize_index(pdf_file):
    """
    Load the uploaded PDF and build the LlamaIndex VectorStoreIndex.
    """
    if pdf_file is None:
        return (
            None, 
            gr.update(visible=True, value="<div class='status-msg status-waiting'>⚠️ Please upload a PDF resume file.</div>"),
            gr.update(interactive=False)
        )
    
    try:
        # Load PDF document using LlamaIndex PDFReader
        reader = PDFReader()
        documents = reader.load_data(file=pdf_file.name)
        
        # Build VectorStoreIndex
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        
        status_html = (
            f"<div class='status-msg status-success'>"
            f"✅ <b>Successfully processed:</b> {os.path.basename(pdf_file.name)}<br>"
            f"Index built with {len(documents)} pages. The chatbot is ready to answer questions!"
            f"</div>"
        )
        return (
            query_engine, 
            gr.update(visible=True, value=status_html),
            gr.update(interactive=True)
        )
    except Exception as e:
        status_html = f"<div class='status-msg status-error'>❌ <b>Error:</b> {str(e)}</div>"
        return (
            None, 
            gr.update(visible=True, value=status_html),
            gr.update(interactive=False)
        )

def chat_response(message, history, query_engine):
    """
    Query the vector store index using the query engine and append to the chat history.
    """
    if history is None:
        history = []
        
    if query_engine is None:
        # User somehow sent a message without an active index
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "⚠️ No resume loaded. Please upload a PDF resume first."})
        return "", history
    
    try:
        # Query the document
        response = query_engine.query(message)
        response_str = str(response)
        
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response_str})
        return "", history
    except Exception as e:
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"❌ Error querying index: {str(e)}\n\nMake sure your OpenAI API Key is valid and has sufficient credits."})
        return "", history

def handle_quick_prompt(prompt_text, history, query_engine):
    """
    Triggers a chat response immediately when a quick suggestion is clicked.
    """
    return chat_response(prompt_text, history, query_engine)

def reset_chat():
    """
    Reset chatbot history, state, and file inputs.
    """
    return (
        None,                             # query_engine state
        None,                             # file input
        gr.update(value=[]),              # chatbot component
        gr.update(value=""),              # message input
        gr.update(visible=True, value="<div class='status-msg status-waiting'>💡 Upload a PDF resume to get started.</div>"),
        gr.update(interactive=False)       # disable text box input
    )

# Build the Gradio App interface
with gr.Blocks() as demo:
    # State management
    query_engine_state = gr.State(None)
    
    # Header Section
    with gr.Row(elem_classes="header"):
        with gr.Column():
            gr.HTML("<h1>📄 AI Resume Q&A Chatbot</h1>")
            gr.HTML("<p>Interact directly with any PDF resume. Get instant summaries, experience timelines, and skill breakdowns.</p>")
        
    with gr.Row():
        # Left Panel (Settings and Upload)
        with gr.Column(scale=1, elem_classes="card"):
            gr.Markdown("### ⚙️ Configuration & Upload")
            
            # PDF Upload field
            pdf_input = gr.File(
                label="Upload Resume (PDF)",
                file_types=[".pdf"],
                interactive=True
            )
            
            # Index status indicator
            status_output = gr.HTML(
                value="<div class='status-msg status-waiting'>💡 Upload a PDF resume to get started.</div>"
            )
            
            # Reset Button
            reset_btn = gr.Button("🔄 Reset Chatbot", variant="secondary")

        # Right Panel (Chatbot Interface)
        with gr.Column(scale=2, elem_classes="card"):
            gr.Markdown("### 💬 Chat Interface")
            
            chatbot = gr.Chatbot(
                label="Resume Assistant",
                height=450
            )
            
            with gr.Row():
                msg_input = gr.Textbox(
                    placeholder="Ask a question about the candidate's resume (e.g. 'What is their experience with Python?')...",
                    container=False,
                    scale=7,
                    interactive=False  # Disabled until resume is uploaded and indexed
                )
                submit_btn = gr.Button("Send", variant="primary", scale=1)
                
            # Quick suggestion buttons
            gr.Markdown("**💡 Try asking:**")
            with gr.Row():
                btn_skills = gr.Button("Summarize key skills", elem_classes="quick-btn")
                btn_exp = gr.Button("Outline work experience", elem_classes="quick-btn")
                btn_education = gr.Button("Detail education history", elem_classes="quick-btn")

    # Wire up Events
    
    # Index build triggers on PDF change
    inputs = [pdf_input]
    outputs = [query_engine_state, status_output, msg_input]
    
    pdf_input.change(fn=initialize_index, inputs=inputs, outputs=outputs)
    
    # Message Submit triggers
    msg_input.submit(
        fn=chat_response, 
        inputs=[msg_input, chatbot, query_engine_state], 
        outputs=[msg_input, chatbot]
    )
    submit_btn.click(
        fn=chat_response, 
        inputs=[msg_input, chatbot, query_engine_state], 
        outputs=[msg_input, chatbot]
    )
    
    # Suggestion button clicks
    btn_skills.click(
        fn=handle_quick_prompt,
        inputs=[gr.State("Summarize my key skills and experience."), chatbot, query_engine_state],
        outputs=[msg_input, chatbot]
    )
    btn_exp.click(
        fn=handle_quick_prompt,
        inputs=[gr.State("Outline my professional work experience details and timeline."), chatbot, query_engine_state],
        outputs=[msg_input, chatbot]
    )
    btn_education.click(
        fn=handle_quick_prompt,
        inputs=[gr.State("Detail my education, certifications, and academic background."), chatbot, query_engine_state],
        outputs=[msg_input, chatbot]
    )
    
    # Reset button trigger
    reset_btn.click(
        fn=reset_chat,
        outputs=[query_engine_state, pdf_input, chatbot, msg_input, status_output, msg_input]
    )

if __name__ == "__main__":
    demo.launch(
        share=False,
        theme=gr.themes.Default(primary_hue="blue", secondary_hue="indigo"),
        css=custom_css
    )
