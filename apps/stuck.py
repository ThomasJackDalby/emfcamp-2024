import printers
from rich import print, traceback
traceback.install()

PRINTER_TYPE = printers.REMOTE

with printers.get_printer(PRINTER_TYPE) as p:
    p.textln("HELP!! I'm stuck in a printer :(")
    for i in range(20):
        p.textln("Aaaaaaaaahhhhhhhh")
    p.cut()