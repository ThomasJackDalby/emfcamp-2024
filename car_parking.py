import printers

PRINTER_TYPE = printers.CONSOLE

def print_carpark_ticket():
    with printers.get_printer(PRINTER_TYPE) as p:
        p.textln("--------")
        p.set(double_width=True, double_height=True, bold=True, align="center")
        p.textln("EMF Parking Ticket")
        p.textln()
        p.textln()
        p.set(double_width=True, double_height=True, align="left")
        p.textln("This ticket entitles the bearer to ONE car being parked in le field next to EMF.")
        p.textln()
        p.textln("Contact:")
        p.textln()
        p.textln("Ben Oxley")
        p.textln()
        p.textln("Hab Ville Campsite F")
        p.textln() 
        p.textln("07967 750 851")
        p.textln()
        p.textln()
        p.image("barcode_ben.png")
        p.textln()
        p.textln()
        p.image("qrcode_ben.png")
        p.set(align="center")
        p.textln("--------")
        p.cut()

if __name__ == "__main__":
    print_carpark_ticket()