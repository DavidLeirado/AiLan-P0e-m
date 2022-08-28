import os
import sys

from fastapi import FastAPI, Request
from pydantic import BaseModel

from model.poem_generator import PoemGenerator

sys.path.append(os.path.abspath("../"))

from utils.logger import Logger

Logger.info("Loading model . . .")
pgen = PoemGenerator("./model/spanish_poems_model.pt")

Logger.info("Initializing app . . .")
app = FastAPI()


class PoemRequest(BaseModel):
    name: str = ""
    text: str
    entry_count: int
    entry_length: int
    temperature: float
    top_p: float


class PoemResponse(BaseModel):
    original_text: str = "Something bad Happened"
    generated: list = []


@app.post("/")
async def poem_maker(request: Request, poem_params: PoemRequest) -> PoemResponse:
    Logger.info(f"IP: {request.client.host} - Name: {poem_params.name}")
    poem = pgen.generate(poem_params.text, entry_count=poem_params.entry_count, entry_length=poem_params.entry_length,
                         temperature=poem_params.temperature, top_p=poem_params.top_p)

    response = PoemResponse()
    response.original_text = poem_params.text
    response.generated = poem

    return response
