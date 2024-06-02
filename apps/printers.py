import requests
import json
from rich import print, traceback
traceback.install()

REMOTE = 0
CONSOLE = 1
RECEIPT = 2

class Printer:

    def __enter__(self):
        return self

    def __exit__(self,  exception_type, exception_value, exception_traceback):
        pass

    def textln(self, text: str=""):
        raise Exception("Not implemented")

    def feed(self, amount):
        raise Exception("Not implemented")
        
    def set(self, double_height=False, double_width=False, bold=False, align="left", underline=False):
        raise Exception("Not implemented")

    def barcode(self, barcode, type):
        raise Exception("Not implemented")

    def cut(self):
        raise Exception("Not implemented")
    
    def flush(self):
        pass

COMMAND_TEXT = "text"
COMMAND_CUT = "cut"
COMMAND_BARCODE = "barcode"
COMMAND_FEED = "feed"

ALIGN_LEFT = "left"
ALIGN_RIGHT = "right"
ALIGN_CENTER = "center"

class RemotePrinter(Printer):
    def __init__(self):
        self.url = "http://151.216.211.144:8000/api/print"
        #self.url = "http://localhost:8000/api/print"
        
        self.commands = []
        self.styles = []

    def __enter__(self):
        self.commands = []
        self.styles = []
        self.set() # set a default style
        return self
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.flush()

    def textln(self, text: str=""):
        self.commands.append({
            "type" : COMMAND_TEXT,
            "content" : str(text),
            "style": self.style_index
        })
    
    def _get_style_index(self, style):
        return None
        for i, existing_style in enumerate(self.styles):
            if style == existing_style:
                return i
        return None

    def set(self, double_height=False, double_width=False, bold=False, align=ALIGN_LEFT, underline=False):
        pass
        style = {
            "double_height": double_height,
            "double_width": double_width,
            "bold": bold,
            "align": align,
            "underline": underline
        }
        style_index = self._get_style_index(style)
        if style_index is None:
            self.styles.append(style)
            style_index = len(self.styles) - 1
        self.style_index = style_index
    
    def cut(self):
        self.commands.append({
            "type" : COMMAND_CUT
        })

    def barcode(self, barcode, type):
        self.commands.append({
            "type" : COMMAND_BARCODE,
            "content": str(barcode)
        })

    def flush(self):
        print("Send IT!")
        request = {
            "styles": self.styles,
            "commands": self.commands
        }
        with open("request.json", "w") as file:
            json.dump(request, file)
        requests.post(self.url, json=request)

class ReceiptPrinter(Printer):
    def __init__(self):
        from escpos.printer import Serial      
        self.p = Serial("COM6", baudrate=19200)

    def textln(self, text=""):
        self.p.textln(str(text))

    def set_title():
        set(double_height=True, double_width=True, bold=True, align="center")

    def set(self, double_height=False, double_width=False, bold=False, align="left", underline=False):
        self.p.set(double_height=double_height, double_width=double_width, bold=bold, align=align, underline=underline)

    def barcode(self, barcode, type):
        self.p.barcode(barcode, type)

    def cut(self):
        self.p.cut()

class ConsolePrinter(Printer):

    def __init__(self):
        self.width = 42
        self.margin = 2

        print()
        self._print_start()

    def textln(self, text):
        while len(text) > self.width:
            self._print(text[:self.width])
            text = text[self.width:]
        self._print(text)

    def set(self, double_height=False, double_width=False, bold=False, align="left", underline=False):
        pass

    def barcode(self, code, type):
        self._print_blank()
        if len(code) % 2 != 0:
            code += "0"
        margin = " "*(self.margin+(self.width - len(code))//2)
        print("|"+margin+"|"*(len(code))+margin+"|")
        print("|"+margin+code+margin+"|")
        self._print_blank()

    def cut(self):
        self._print_end()
        print()
        self._print_start()

    def _print_blank(self):
        print("|"+" "*(self.width+self.margin*2)+"|")

    def _print_edge(self):
        print("+"+"-"*(self.width+self.margin*2)+"+")

    def _print_start(self):
        self._print_edge()
        self._print_blank()

    def _print_end(self):
        self._print_edge()

    def _print(self, text):
        print("|"+" "*self.margin+str.ljust(text, self.width)+" "*self.margin+"|")

def get_printer(type):
    if type == CONSOLE: return ConsolePrinter()
    elif type == REMOTE: return RemotePrinter()
    elif type == RECEIPT: return ReceiptPrinter() 