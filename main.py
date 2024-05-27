from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/api")
def get_root():
    return {"Hello": "World"}

app.mount("/", StaticFiles(directory="static"), name="static")