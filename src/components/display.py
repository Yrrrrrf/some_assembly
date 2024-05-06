# standard imports
from dataclasses import dataclass

# third-party imports
from PyQt6.QtWidgets import QGridLayout, QFrame, QTabWidget, QPushButton, QWidget
from PyQt6.QtCore import Qt

# local imports
from components.workspace import Workspace
from components.side_panel import SidePanel
from config.globals import Assets


@dataclass
class Display(QFrame):
    '''
    Display class referece to the window that contains all the widgets.
    Also manage the position of the widgets and the size of the window.
    This class must the the main class of the application.
    '''
    side_panel: SidePanel  # * Maybe the Display can have more than one side panel along the window
    # workspace_tabs: QTabWidget  # * Handles 1 or many workspaces
    workspace: Workspace  # * Handles 1 or many workspaces


    def __init__(self):
        super().__init__()
        self.setProperty('class', 'display')

        self.side_panel = SidePanel()
        self.workspace = Workspace()
        
        layout = QGridLayout()  # ? Set the layout distribution
        # layout.addWidget(self.side_panel, 0, 0)  # * Expand and fill the space
        layout.addWidget(self.workspace, 0, 1)

        self.setLayout(layout)

        # Get the current selected tab
        # print(self.workspace.currentIndex())

        # get the visualizer of the current tab
        # print(self.workspace.v_list[self.workspace.currentIndex()])

        # Access to the workspace & save the image
        # self.workspace.v_list[0].save_image()
        # self.workspace.v_list[0].save_image('siuuuuuuuuuuu.png')


    # * MANAGE ALL SHORTCUTS OF THE APPLICATION
    def keyPressEvent(self, event):
        event_mod = event.modifiers()  # *  is a var because it is used multiple times
        match event_mod:
            case Qt.KeyboardModifier.ControlModifier:
                # print('Ctrl')
                # print(event.key())
                number = event.key() - 88 if event.key() == 94 else event.key() - 48
                match number:
                    case 30:  # N  # * Create a new tab & go to it
                        self.workspace._new_tab()
                        self.workspace.setCurrentIndex(self.workspace.count() - 1)
                    case 39:  # W  # * Close the current tab
                        self.workspace._close_tab(self.workspace.currentIndex())
                    case _:  # * Go to the tab of the number
                        if number <= self.workspace.count():  # If the number is less than the number of tabs
                            self.workspace.setCurrentIndex(number - 1)  # Go to the tab of the number

            # case Qt.KeyboardModifier.ShiftModifier:
            #     print('Shift')

            # case Qt.KeyboardModifier.AltModifier:
            #     print('Alt')

            # case Qt.KeyboardModifier.MetaModifier:
            #     print('Meta')

            # case Qt.KeyboardModifier.NoModifier:
            #     print('No modifier')

            # case _:
            #     print(f'Other modifier {event.key()}')

