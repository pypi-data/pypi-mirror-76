try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import os

def detect(filename):
    if (os.path.isfile(filename)):
        detected_text = pytesseract.image_to_string(Image.open(filename)).lower()

        result = detected_text.find('binod')
        if (result):
            print('Binod found in image file : ', filename)
        else:
            print('Binod not found in image file : ', filename)
    else:
        print(filename, ' path does not exist')



