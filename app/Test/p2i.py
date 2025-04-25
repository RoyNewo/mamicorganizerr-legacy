from pdf2image import convert_from_path

# from pdf2image.exceptions import (
#  PDFInfoNotInstalledError,
#  PDFPageCountError,
#  PDFSyntaxError
# )

images = convert_from_path(
    "/home/data/Downloads/dr who/doctorwho_thetenthdoctorarchives_vol3.pdf"
)

for i, image in enumerate(images):
    fname = (
        "/home/data/Comics/Descargas/temporal/"
        + "{:0>3}".format(i)
        + ".png"
    )
    image.save(fname, "PNG")
