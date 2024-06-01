import sys
import printers
from rich import print, traceback
traceback.install()

PRINTER_TYPE = printers.REMOTE

message = sys.argv[1]

with printers.get_printer(PRINTER_TYPE) as p:
    p.set(double_height=True, double_width=True, bold=True, underline=True, align="centre")
    p.textln("Incoming MESSAGE!!!!")
    p.set()
    p.textln("--------------------")
    p.textln(message)
    p.textln("--------------------")
    p.cut()