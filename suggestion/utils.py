import os
from PIL import Image
from pyzbar.pyzbar import decode


def get_barcode(img):
    bar = Image.open(img)
    code = decode(bar)
    if code:
        return code[0][0]
    return None


if __name__ == "__main__":
    img_file = "bar.jpeg"
    path = os.getcwd()
    img = os.path.join(path, img_file)
    barcode = get_barcode(img)
    print(os.curdir)
