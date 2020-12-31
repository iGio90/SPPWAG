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

from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPlainTextEdit


class QDataLayout(QVBoxLayout):
    def __init__(self, sppwag):
        super().__init__()

        self.sppwag = sppwag

        title = QLabel("Buffers")
        title.setStyleSheet("font: 12pt;")
        self.addWidget(title)

        self.data_box = QPlainTextEdit()
        self.data_box.textChanged.connect(self.on_change)

        self.addWidget(self.data_box)

    def get_data(self):
        valid_data = []
        for row in self.data_box.toPlainText().split('\n'):
            if len(row) > 0:
                try:
                    bytes.fromhex(row)
                    valid_data.append(row)
                except:
                    pass
        return valid_data

    def on_change(self):
        self.sppwag.process()
