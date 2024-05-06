# standard imports
from dataclasses import dataclass

# third-party imports
from PyQt6.QtWidgets import QScrollArea, QTabWidget, QPushButton, QWidget
from PyQt6.QtGui import QIcon, QPainter, QColor, QPen
from PyQt6.QtCore import QSize, Qt
from numpy import add

# local imports
from config.globals import Assets
from components.vistualizer import Visualizer


@dataclass
class Workspace(QTabWidget):
    '''
    The workspace is the container of the visualizer.

    It handles the mouse events and the buttons of the visualizer.

    Also it handles the buttons of the image buffer's. (RUD operations)
    '''
    v_list: list[Visualizer]  # * list of visualizers (One for each tab)


    def __init__(self):
        super().__init__()
        self.setProperty('class', 'workspace')
        self.setMovable(True)
        # self.setMouseTracking(True)
        # * New Tab button
        # add_button = QPushButton(QIcon(Assets.ICONS.value+'sum.png'), '')
        add_button = QPushButton()
        add_button.clicked.connect(self._new_tab)
        add_button.setProperty('class', 'add_button')
        self.setCornerWidget(add_button, Qt.Corner.TopRightCorner)

        # * Close Tab button
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self._close_tab)

        # * Set initial tabs
        self.v_list = []  # * list of visualizers (One for each tab)
        [self._new_tab() for _ in range(1)]  # Create n tabs (n: int)

        # print(self.v_list)

        # V is a Visualizer
        # -> parent: QWidget: scroll_zone
        # -> parent: QScrollArea: scroll_area
        # -> parent: QStackedWidget
        # -> parent: Workspace (self)
        # for v in self.v_list:
            # print(type(v))


    def _new_tab(self):
        '''
        Create a new tab with a visualizer.
        Also set the buttons of the image buffer's inside the visualizer.
        '''
        # * Instantiate the visualizer, the scroll zone & the scroll area
        scroll_area = QScrollArea()
        scroll_area.setProperty('class', 'scroll_area')

        scroll_zone = QWidget()
        scroll_zone.setProperty('class', 'scroll_zone')

        visualizer = Visualizer(scroll_zone)

        # * Set the visualizer to the center of the scroll zone
        scroll_zone_margin: int = 480  # * Margin of the scroll zone (out border of the visualizer)
        scroll_zone.setFixedSize(visualizer.width() + 2 * scroll_zone_margin, visualizer.height() + 2 * scroll_zone_margin)
        visualizer.move(scroll_zone.width() // 2 - visualizer.width() // 2, scroll_zone.height() // 2 - visualizer.height() // 2)

        # # * Add the visualizer to the scroll area
        scroll_area.setWidget(scroll_zone)   # Set the scroll zone as the widget of the scroll area
        scroll_area.setWidgetResizable(True)  # Make the scroll area resizable
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # * Set the scroll area to the center of the tab
        # initial_pos_margin: int = 32  # Visualizer initialized on (32, 32)
        initial_pos_margin: int = 48  # Visualizer initialized on (48, 48)
        scroll_area.verticalScrollBar().setValue(scroll_zone.height() // 2 - visualizer.height() // 2 - initial_pos_margin)  # type: ignore
        scroll_area.horizontalScrollBar().setValue(scroll_zone.width() // 2 - visualizer.width() // 2 - initial_pos_margin)  # type: ignore

        # * Add the scroll area to the tab widget
        self.addTab(scroll_area, f'New_{self.count()+1}')
        # * Add the visualizer to the list of visualizers
        self.v_list.append(visualizer)


    def _close_tab(self, index: int):
        """
        Close the tab at the given index.

        If the last tab is closed, create a new one. This is to avoid having no tabs.

        ## Arguments:
            - index (int): the index of the tab to close
        """
        # TODO: Add a confirmation dialog (are you sure you want to close this tab?)
        self.removeTab(index)   # Remove the tab from the tab widget
        self.v_list.pop(index)  # * Remove the visualizer from the list of visualizers
        if self.count() == 0: self._new_tab()  # If there are no tabs, create a new one
