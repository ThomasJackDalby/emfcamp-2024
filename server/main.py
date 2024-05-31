import configparser
import logging
from escpos.printer import Serial
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

CONFIG_FILE_NAME = 'config.ini'

COMMAND_TEXT = "text"
COMMAND_CUT = "cut"
COMMAND_FEED = "feed"

# load config
config = configparser.ConfigParser()
config["printer"] = {}
config["dev"] = {}
config.read(CONFIG_FILE_NAME)
PRINTER_SERIAL_ADDRESS = config["printer"]["serial_address"]
PRINTER_BAUDRATE = config["printer"]["baudrate"]
OFFLINE = config["dev"]["offline"]

class FakePrinter:
    def textln(self, text):
        pass
    def feed(self, amount):
        pass
    def cut(self):
        pass

# initialise printer
if not OFFLINE:
    p = Serial(PRINTER_SERIAL_ADDRESS, baudrate=PRINTER_BAUDRATE)
else:
    p = FakePrinter()

class Style(BaseModel):
    pass

class Command(BaseModel):
    type: str | None = None
    content: str | None = None
    style: int | None = None

class PrintJob(BaseModel):
    commands: list[Command | Style] | None = None # not sure a union between two classes is allowed

def print_error_message(e: Exception):
    p.textln("------------")
    p.textln("!! ERROR !!")
    p.textln(e.message)
    p.textln("------------")

# define api
app = FastAPI()

@app.get("/api")
def get_root():
    return {"Hello": "World"}

@app.post("/api/print")
def post_job(job: PrintJob):
    current_style = None

    try:
        for command in job.commands:
            if command.type == COMMAND_TEXT: p.textln(command.content)
            elif command.type == COMMAND_FEED: p.feed(5)
            elif command.type == COMMAND_CUT: p.cut()
    except Exception as e:
        p.cut()
        p.textln("!! ERROR !!")
        # print out an error message?
        pass
    finally:
        # always cut to ensure the next job doesn't fail
        p.cut()

app.mount("/", StaticFiles(directory="static"), name="static")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)