from PIL import Image, ImageFont, ImageDraw
from math import sqrt

class ImageWriter:
    def __init__(self, template, output_dir):
        try:
            self._img = Image.open(template)
            self._output_dir = output_dir
            x, y = self._img.size
            self._font = ImageFont.truetype("fonts/Roboto-Regular.ttf", int(sqrt(x*2)))
        except OSError as ex:
            print("Error opening the file!")
            print(ex)
        

    def write(self, filename, data, fill_color=(255, 255, 255)):
        filename = self._output_dir + str(filename) + ".jpg"
        self._img.save(filename)
        with Image.open(filename) as img_instance:
            drawer = ImageDraw.Draw(img_instance)
            for text, dimension in data.items():
                drawer.text(dimension, text, 
                            fill=fill_color, 
                            font=self._font)
            img_instance.save(filename)