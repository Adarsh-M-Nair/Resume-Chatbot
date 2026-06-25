# AI QnA Resume Chatbot 📄🤖

An interactive, AI-powered Resume Q&A Chatbot that allows you to upload any PDF resume and query it for skills, education, professional experience, and custom questions. Built with **Gradio** and **LlamaIndex**, powered by **OpenAI**.

---

## Features ✨

* **Upload PDF Resumes**: Easily drag-and-drop or browse your local files to upload any resume in PDF format.
* **Instant In-Memory Indexing**: Fast vector indexing of your PDF documents using LlamaIndex's `VectorStoreIndex`.
* **Secured LLM Setup**: The OpenAI API key is configured directly in the application's source code for convenience.
* **Gradio 6.0 Custom UI**: Sleek, modern dark-mode responsive styling with:
  - Dynamic status indicators.
  - Interactive chat panel.
  - Quick prompt suggestions ("Summarize key skills", "Outline work experience", "Detail education history") for immediate answers.
* **Reset Interface**: One-click reset to clean current index and clear chat history.

---

## Installation 📦

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Clone/Copy the Project
Navigate to your project directory:
```bash
cd "Resume Chatbot"
```

### 3. Install Dependencies
Install all the required Python packages:
```bash
pip install -r requirements.txt
```

The packages installed include:
* `llama-index`
* `llama-index-readers-file`
* `gradio`
* `openai`
* `pypdf`

---

## Configuration ⚙️

The application uses an OpenAI API Key to generate embeddings and retrieve answers.

The API key is securely hardcoded in the script. If you need to change the key in the future, open `app.py` and replace the key in the following line:

```python
# Set OpenAI API key directly inside the program
os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY_HERE"
```

---

## Running the App 🚀

Start the application by running:

```bash
python app.py
```

After launching, you will see output in the terminal indicating the local URL:
```text
Running on local URL:  http://127.0.0.1:7860
```

1. Open your web browser and go to [http://127.0.0.1:7860](http://127.0.0.1:7860).
2. Upload your PDF resume in the **Configuration & Upload** panel on the left.
3. Once the status indicator changes to **Successfully processed**, start typing questions in the chat interface!

---

## File Structure 📂

```text
Resume Chatbot/
├── app.py              # Main Gradio application & LlamaIndex logic
├── requirements.txt    # Project dependencies
└── README.md           # This project guide
```
