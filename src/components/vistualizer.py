# standard imports
from dataclasses import dataclass
from typing import Callable

# third-party imports
from PyQt6.QtWidgets import QLabel, QWidget, QGridLayout
from PyQt6.QtGui import QCursor, QPixmap, QPainter, QColor, QPen
from PyQt6.QtCore import Qt
# import cv2 as cv

# local imports
# from logic.intel_sc import *  # for intelligent scissors algorithm implementation
from config.globals import Assets


@dataclass
class Visualizer(QLabel):
    '''
    This class contains one or more image buffer's, which are the images that are displayed in the workspace.
    The visualizer is the container of the image buffer's.
    '''
    bg_pixmap: QPixmap  # the main pixmap of the visualizer (This will be the image that will be saved)


    def __init__(self, workspace: QWidget, width: int = 512, height: int = 512, border: int = 0):
        super().__init__(workspace)

        self.setProperty('class', 'visualizer')
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))
        # width = 500
        # height = 300
        
        self.setFixedSize(width, height)
        # self.setMargin(margin)  # Not uses because the QMargins can't be manipulated (paint on them)

        self.images = []  # * list of image buffer's
        border = 16  # * Border of the visualizer

        # * Color the background
        self.bg_pixmap = QPixmap(self.width() + border * 2, self.height() + border * 2)
        self.bg_pixmap.fill(Qt.GlobalColor.transparent)
        # self.bg_pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.bg_pixmap)
