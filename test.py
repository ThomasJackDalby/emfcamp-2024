from escpos.printer import Serial

p = Serial("/dev/ttyUSB0", baudrate=19200)
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")
p.textln("TEST")