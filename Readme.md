# Text Summarizer

A complete pipeline for training and deploying an advanced AI text summarization model using Hugging Face's `transformers` library and a `FastAPI` backend. This project focuses on summarizing conversational dialogues and features a sleek, modern web frontend.

## Project Structure

- **Backend & Serving**
  - `app.py`: The FastAPI server that loads the fine-tuned model and exposes a POST `/summarize` endpoint.
  - `index.html` & `script.js`: The frontend user interface built with TailwindCSS and connected client-side logic that seamlessly interacts with the REST API.
  
- **Model Training Data & Notebook**
  - `TextSummarizer.ipynb`: A Jupyter Notebook containing the full training pipeline to load the dataset, preprocess the text, and fine-tune a T5 sequence-to-sequence model.
  - `samsum-train.csv`, `samsum-validation.csv`, `samsum-test.csv`: The SAMSum dialogue summaries dataset utilized for training robust, chat-like text summarization.

## Getting Started

### 1. Requirements

Ensure you have Python installed. You can install all project dependencies using:
```bash
pip install -r requirements.txt
```

*(Note: Depending on your system hardware, you might need to install a specific `torch` build tailored to your GPU/Environment from [PyTorch's Official Site](https://pytorch.org/).)*

### 2. Preparing the Model

For the web application to function properly, your pre-trained or fine-tuned artifacts must exist in the `./models/` directory:
- `./models/t5-summary-model`
- `./models/t5-summary-tokenizer`

*You can generate these directories by running all cells in the `TextSummarizer.ipynb` notebook.*

### 3. Web Service

Start up the Uvicorn ASGI server and application:
```bash
uvicorn app:app --reload
```

Finally, open your preferred web browser and navigate directly to **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** to interact with the summarizer!
