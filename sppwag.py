"""
Copyright 2021 - Giovanni (iGio90) Rocca

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import qdarkgraystyle

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSplitter

from lib.widget_conversions import QConversionsWidget
from lib.layout_data import QDataLayout
from lib.widget_result import QResultWidget
from lib.layout_struct import QStructLayout


class SPPWAG(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        root = QSplitter()

        content_splitter = QSplitter()
        content_splitter.setOrientation(Qt.Vertical)

        main_container = QWidget()
        main_container.setLayout(QVBoxLayout())

        self.data_layout = QDataLayout(self)
        self.struct_layout = QStructLayout(self)
        self.q_result = QResultWidget(self)
        self.conversions_layout = QConversionsWidget()

        main_container.layout().addLayout(self.data_layout)
        main_container.layout().addLayout(self.struct_layout)

        content_splitter.addWidget(main_container)
        content_splitter.addWidget(self.conversions_layout)
        content_splitter.setStretchFactor(0, 3)
        content_splitter.setStretchFactor(1, 3)

        root.addWidget(content_splitter)
        root.addWidget(self.q_result)

        layout.addWidget(root)

        self.setLayout(layout)

    def process(self):
        self.q_result.process()


if __name__ == "__main__":
    QApplication.setDesktopSettingsAware(True)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setLayoutDirection(Qt.LeftToRight)

    QApplication.setOrganizationName("https://github.com/iGio90/SPPWAG")
    QApplication.setApplicationName("SPPWAG")
    QApplication.setApplicationDisplayName('SPPWAG')

    app = QApplication([])
    app.setStyleSheet(qdarkgraystyle.load_stylesheet())

    sppwag = SPPWAG()
    sppwag.showMaximized()
    app.exec_()

