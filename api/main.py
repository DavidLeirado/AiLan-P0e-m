import torch
from fastapi import FastAPI

model = torch.load("./model/spanish_poems_model.pt").to("cpu")

app = FastAPI()


@app.post("/")
async def poem_maker():
    return {"message": "Hello World"}
