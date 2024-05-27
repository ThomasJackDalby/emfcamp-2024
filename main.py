import configparser
import logging
from escpos.printer import Serial
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

CONFIG_FILE_NAME = 'config.ini'
OFFLINE = False

# load config
config = configparser.ConfigParser()
config.read(CONFIG_FILE_NAME)
PRINTER_SERIAL_ADDRESS = config["printer"]["serial_address"]
PRINTER_BAUDRATE = config["printer"]["baudrate"]

class FakePrinter:
    def textln(self, text):
        pass
    def cut(self):
        pass

# initialise printer
if not OFFLINE:
    p = Serial(PRINTER_SERIAL_ADDRESS, baudrate=PRINTER_BAUDRATE)
else:
    p = FakePrinter()

class Step(BaseModel):
    type: str | None = None
    content: str | None = None
    style: int | None = None

class Job(BaseModel):
    steps: list[Step] | None = None

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



@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)