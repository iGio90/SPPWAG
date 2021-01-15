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
import base64
import binascii

from PyQt5.QtWidgets import QVBoxLayout, QComboBox, QHBoxLayout, QPlainTextEdit, QWidget
from hexdump import hexdump

FORMATS = [
    'string',
    'base64',
    'hex',
    'hexdump'
]


class QConversionsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.picker_from = QComboBox()
        self.picker_from.addItems(FORMATS[:-1])
        self.picker_from.currentIndexChanged.connect(self.data_changed)

        self.picker_to = QComboBox()
        self.picker_to.addItems(FORMATS)
        self.picker_to.currentIndexChanged.connect(self.data_changed)

        formats_container = QHBoxLayout()
        formats_container.addWidget(self.picker_from)
        formats_container.addWidget(self.picker_to)
        layout.addLayout(formats_container)

        self.data_from = QPlainTextEdit()
        self.data_from.textChanged.connect(self.data_changed)

        self.data_to = QPlainTextEdit()
        self.data_to.setReadOnly(True)

        data_container = QHBoxLayout()
        data_container.addWidget(self.data_from)
        data_container.addWidget(self.data_to)
        layout.addLayout(data_container)

        self.setLayout(layout)

    def data_changed(self):
        self.data_to.clear()

        from_type = self.picker_from.currentIndex()
        to_type = self.picker_to.currentIndex()
        if from_type != to_type:
            data = self.data_from.toPlainText()
            # always convert to raw bytes
            if from_type == 0:
                data = data.encode('utf8')
            elif from_type == 1:
                try:
                    data = base64.b64decode(data.encode('utf8'))
                except:
                    data = b''
            elif from_type == 2:
                data = bytes.fromhex(data)

            result = ''
            if to_type == 0:
                try:
                    result = data.decode('utf8')
                except:
                    result = "".join(map(chr, data))
            elif to_type == 1:
                result = binascii.b2a_base64(data)
            elif to_type == 2:
                result = binascii.hexlify(data)
            elif to_type == 3:
                result = hexdump(data, result='return').replace(' ', '&nbsp;&nbsp;')

            if type(result) == bytes:
                result = result.decode('utf8')

            self.data_to.appendHtml(result)
