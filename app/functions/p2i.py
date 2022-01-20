from pdf2image import convert_from_path
import os


def splitpdf(archivo, rutaexport, foldername):

    if not os.path.exists(rutaexport):
        os.makedirs(rutaexport)

    convert_from_path(
        archivo,
        output_folder=rutaexport,
        fmt="png",
        output_file=foldername,
        paths_only=True,
    )
