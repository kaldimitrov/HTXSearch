from PIL import Image

def crop(input, left, top, right, bottom):
    img = Image.open(input)
    img2 = img.crop((left, top, right, bottom))
    img2.save("img2.jpg")