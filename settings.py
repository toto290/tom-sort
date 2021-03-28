import os
from pathlib import Path
from debug_utilities_lib import *


class Settings:
    default_image = None
    valid_image_types = ['.jpg', '.JPG', '.png', '.PNG']

    # Paths
    root_path = os.path.dirname(__file__)
    media_path = Path.joinpath(Path(root_path), 'images')


class Styles:
    colors = {'background': '#121212',
              'widget_bg': '#1f2933',
              'font': '#ffffff',
              'widget_fg': '#323f4b'}


if __name__ == '__main__':
    debug(Settings.default_placeholder_img_path)

    class Xy:
        def __init__(self):
            self.a = 1

    myXy = Xy()

    debug(type(myXy))
    debug(type(Xy()))
    debug(isinstance(myXy, Xy))
