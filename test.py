from escpos.printer import Serial

p = Serial("/dev/ttyUSB01", baudrate=19200)
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")