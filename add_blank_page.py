import os

from PIL import Image, ImageDraw


class BlankPage:
    def __init__(self, width, height, page_color, blank_page_directory, blank_page_name, blank_page_extension):
        self.height = height
        self.width = width
        self.page_color = page_color
        self.blank_page_directory = blank_page_directory
        self.blank_page_name = blank_page_name
        self.blank_page_extension = blank_page_extension

    def add_page(self):
        # size of image
        canvas = (self.width, self.height)

        # init canvas
        im = Image.new('RGB', canvas, self.page_color)

        # save image
        if f"{self.blank_page_name}.{self.blank_page_extension}" not in os.listdir(
                self.blank_page_directory):
            im.save(f"{self.blank_page_directory}\\{self.blank_page_name}.{self.blank_page_extension}")
        else:
            im.save(f"{self.blank_page_directory}\\{self.blank_page_name} - Copy.{self.blank_page_extension}")
