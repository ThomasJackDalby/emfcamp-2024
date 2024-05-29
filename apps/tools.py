


def scan_barcode():
    print("Awaiting barcode scan:")
    barcode = input("$ ")
    if barcode is None:
        return None