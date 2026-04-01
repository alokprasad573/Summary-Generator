from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from transformers import T5Tokenizer, T5ForConditionalGeneration
from pydantic import BaseModel
import torch
import re
import pandas as pd


app = FastAPI(
    title="Summary Generator",
    description="Generate summaries for text",
    version="1.0.0",
)

# Load Model
model = T5ForConditionalGeneration.from_pretrained("./models/t5-summary-model")
tokenizer = T5Tokenizer.from_pretrained("./models/t5-summary-tokenizer")

# device
if torch.backends.mps.is_available():
    device = torch.device("mps")
elif torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

model.to(device)

# templating
templates = Jinja2Templates(directory=".")


# Input Schema for dialogue
class DialougeInput(BaseModel):
    dialogue: str


# Clean DataFunction
def clean_data(text):
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    text = str(text)
    text = re.sub(r"\r\n", " ", text)  # Replace newlines with space
    text = re.sub(r"\s+", " ", text)  # Remove extra whitespace
    text = re.sub(r"<.*?>", " ", text)  # Remove HTML tags
    return text.strip().lower()


def summarize_dialogue(dialogue: str) -> str:
    dialogue = clean_data(dialogue)
    # tokenize
    inputs = tokenizer(
        dialogue,
        max_length=512,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    ).to(device)

    # generate the summary
    model.to(device)
    targets = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],
        max_length=150,
        num_beams=4,
        early_stopping=True,
    )

    # tokens ids convert to summary => decoding
    summary = tokenizer.decode(
        targets[0], skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return summary


# root api
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/summarize")
async def summarize(dialogue_input: DialougeInput):
    summary = summarize_dialogue(dialogue_input.dialogue)
    return {"summary": summary}
