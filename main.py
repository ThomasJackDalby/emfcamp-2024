from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from escpos.printer import Serial
import configparser

CONFIG_FILE_NAME = 'config.ini'

# load config
config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)
PRINTER_SERIAL_ADDRESS = config["printer"]["serial_address"]
PRINTER_BAUDRATE = config["printer"]["baud_rate"]

# initialise printer
p = Serial(PRINTER_SERIAL_ADDRESS, baudrate=PRINTER_BAUDRATE)

class Step(BaseModel):
    type: str
    content: str
    style: int

class Job(BaseModel):
    steps: List[Step]

# define api
app = FastAPI()

@app.get("/api")
def get_root():
    return {"Hello": "World"}

@app.post("/api/job")
def post_job(job: Job):
    for step in job.steps:
        p.textln(step.content)
    p.cut()

app.mount("/", StaticFiles(directory="static"), name="static")