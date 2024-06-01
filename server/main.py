import configparser
import logging
from escpos.printer import Serial
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
logging.basicConfig(level=logging.DEBUG, filename="logs/fastapi.log")

logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = 'config.ini'
COMMAND_TEXT = "text"
COMMAND_CUT = "cut"
COMMAND_FEED = "feed"
COMMAND_BARCODE = "barcode"

# load config
config = configparser.ConfigParser()
config["printer"] = {}
config["dev"] = {}
config.read(CONFIG_FILE_NAME)
PRINTER_SERIAL_ADDRESS = config["printer"]["serial_address"]
PRINTER_BAUDRATE = config["printer"]["baudrate"]
PRINTER_MODE = config["printer"]["mode"]

class FakePrinter:
    def textln(self, text):
        pass
    def feed(self, amount):
        pass
    def cut(self):
        pass

# initialise printer
if PRINTER_MODE == "serial": p = Serial(PRINTER_SERIAL_ADDRESS, baudrate=PRINTER_BAUDRATE)
else: p = FakePrinter()

class Style(BaseModel):
    double_height: bool | None = False
    double_width: bool | None = False
    bold: bool | None = False
    align: str | None = "left"
    underline: bool | None = False

class Command(BaseModel):
    type: str | None = None
    content: str | None = None
    style: int | None = None

class PrintJob(BaseModel):
    styles: list[Style] | None = None
    commands: list[Command] | None = None

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
    logger.info("Got request!")
    last_was_cut = False
    try:
        style_index = 0
        for command in job.commands:
            if command.type == COMMAND_TEXT: 
                if command.style != style_index:
                    style_index = command.style
                    style = command.styles[style_index]
                    p.set(
                        align=style.align,
                        double_height=style.double_height,
                        double_width=style.double_width,
                        bold=style.bold,
                        underline=style.underline)
                p.textln(command.content)
            elif command.type == COMMAND_FEED: 
                p.feed(5)
            elif command.type == COMMAND_CUT:
                p.cut()
            elif command.type == COMMAND_BARCODE:
                p.barcode(command.content, "UPC-A")
        last_was_cut = command.type == COMMAND_CUT
            
    except Exception as e:
        print("Uh oh, had an error")
        print(e.message)
        p.cut()
        p.textln("!! ERROR !!")
    finally:
        if not last_was_cut:
            p.cut()

app.mount("/", StaticFiles(directory="static", html=True), name="static")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

logger.info("Initialised the API!")