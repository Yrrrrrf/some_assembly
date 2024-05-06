# standard imports
from dataclasses import dataclass
from typing import Callable

# third-party imports
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
# import cv2 as cv

# local imports
# from logic.intel_sc import *  # for intelligent scissors algorithm implementation
from config.globals import Assets


@dataclass
class Visualizer(QLabel):
    '''
    A QLabel-derived class that acts as a visualizer for displaying the contents of a file.
    It includes a QTextEdit within which the file's contents are displayed.
    '''

    def __init__(self, workspace: QWidget, width: int = 512, height: int = 512):
        super().__init__(workspace)

        self.setProperty('class', 'visualizer')
        self.setCursor(QCursor(Qt.CursorShape.CrossCursor))

        self.setFixedSize(width, height)
        # self.setMargin(margin)  # Not uses because the QMargins can't be manipulated (paint on them)

        self.init_ui()


    def init_ui(self):
        ''' Initializes the user interface components inside the visualizer. '''
        self.text_edit: QTextEdit = QTextEdit(self)
        self.text_edit.setFont(QFont('Cascadia Code', 20))
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        self.setLayout(layout)

        set_content(self.text_edit, 'The pinchis...')

    
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 
            "Open File", 
            Assets.ASM_DOCS.value,
            # "Assembly files (*.ens);;All files (*)"
            "Assembly files (*.asm);;All files (*)"
        )

        match file_path:
            case '':
                print('\033[31mError: No file selected!\x1B[37m')
                QMessageBox.critical(self, 'Error', 'Please select a file.')
            case _: set_content(read_file(file_path))

def set_content(text_edit: QTextEdit, text: str):
    text_edit.setPlainText(text)

def read_file(file_path: str) -> str:
    file: QFile = QFile(file_path)
    if not file.open(QIODevice.OpenModeFlag.ReadOnly):
        print(f"Failed to open the file: {file.errorString()}")
        return None
    text_stream: QTextStream = QTextStream(file)
    content: str = text_stream.readAll()
    file.close()
    return content
