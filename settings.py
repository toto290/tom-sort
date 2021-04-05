import os
from pathlib import Path
from debug_utilities_lib import *


class Settings:
    images = {'placeholder': 'default_placeholder',
              'welcome_screen': 'start_background'}
    valid_image_types = ['.jpg', '.JPG', '.png', '.PNG']

    # Paths
    root_path = os.path.dirname(__file__)
    media_path = Path.joinpath(Path(root_path), 'images')


class Styles:
    colors = {'background': '#121212',
              'widget_bg': '#1f2933',
              'font': '#ffffff',
              'widget_fg': '#323f4b',
              'logo_tom': '#17c745'}
    fontsizes = {'s': 8, 'm': 14, 'l': 20, 'logo': 180, 'slogan': 70}
    font = {'default': 'Candara',
            'tom': 'Candara',
            'slogan': 'Brush Script MT'}


if __name__ == '__main__':
    class Xy:
        def __init__(self):
            self.a = 1

    myXy = Xy()

    debug(type(myXy))
    debug(type(Xy()))
    debug(isinstance(myXy, Xy))
