from typing import Annotated
import uuid
from os import getenv

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI

load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_speech_file_path():
    return f"static/speech-{uuid.uuid4().hex}.mp3"


client = OpenAI(
    api_key=getenv("OPENAI_TOKEN"),
    organization=getenv("OPENAI_ORG_ID"),
    project=getenv("OPENAI_PROJECT_ID"),
)


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    context = {"request": request, "title": "Home"}
    response = templates.TemplateResponse("home.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)  # 3 days
    return response


@app.post("/generate")
async def generate(request: Request, text: Annotated[str, Form()]):
    session_key = request.cookies.get("session_key", uuid.uuid4().hex)
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )
    speech_file_path = get_speech_file_path()
    response.stream_to_file(speech_file_path)
    context = {"request": request, "audio_file_src": speech_file_path}
    response = templates.TemplateResponse("fragments/audio.html", context)
    response.set_cookie(key="session_key", value=session_key, expires=259200)  # 3 days
    return response
