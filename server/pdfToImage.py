from pdf2image import convert_from_path


def pdfToImage(input):
    images = convert_from_path(input)

    for i in range(len(images)):
        images[i].save("page" + str(i) + ".jpg", "JPEG")
