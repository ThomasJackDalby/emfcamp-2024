import sys
import os
import math
from PIL import Image

# STRIP_WIDTH = 42

# image = Image.open("test.jpg")
# pixels = list(image.getdata())

# width, height = image.size    
# number_of_strips = math.ceil(width / STRIP_WIDTH)
# print(f"{number_of_strips=}")

# # import printers
# # p = printers.get_printer(printers.RECEIPT)

def resize():
    im = Image.open("test.jpg")
    im.thumbnail((128, 128))
    im.save("small.jpg", "JPEG")



#     size = 128, 128

#     for infile in sys.argv[1:]:
#         outfile = os.path.splitext(infile)[0] + ".thumbnail"
#         if infile != outfile:
#             try:
#                 im = Image.open(infile)
#                 im.thumbnail(size, Image.Resampling.LANCZOS)
#                 im.save(outfile, "JPEG")


