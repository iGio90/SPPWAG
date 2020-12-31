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

import binascii
import traceback

from PyByteBuffer import ByteBuffer
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPlainTextEdit, QWidget
from hexdump import hexdump

from lib.data_type import DataType


class QResultWidget(QWidget):
    def __init__(self, sppwag):
        super().__init__()

        self.sppwag = sppwag

        layout = QVBoxLayout()

        title = QLabel("Result")
        title.setStyleSheet("font: 12pt;")
        layout.addWidget(title)

        self.result_box = QPlainTextEdit()
        self.result_box.setReadOnly(True)

        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def process(self):
        pos = self.result_box.verticalScrollBar().value()
        self.result_box.clear()

        struct: list[DataType] = self.sppwag.struct_layout.get_struct()

        if len(struct) < 1:
            return

        indent = '&nbsp;' * 4
        row_n = 0

        for row in self.sppwag.data_layout.get_data():
            try:
                buf = ByteBuffer.from_hex(row)
            except:
                row_n += 1
                continue

            self.result_box.appendHtml('%d: %s<br><br>{' % (row_n, binascii.hexlify(buf.array()).decode('utf8')))
            buf.rewind()

            data_struct_rows = []
            data_field = 0

            for data_type in struct:
                length_data_type = data_type.length_type
                if length_data_type is not None:
                    try:
                        length = buf.get(length_data_type.get_length(), length_data_type.get_endianness_value())
                    except:
                        continue
                else:
                    length = data_type.get_length()

                date_buf = buf.array(length)

                try:
                    if data_type.data_type == 5:
                        item_parsed = date_buf.decode('utf8')
                    else:
                        data = ByteBuffer.wrap(date_buf)
                        item_parsed = str(data.get(length, data_type.get_endianness_value()))

                    item_bytes = binascii.hexlify(date_buf).decode('utf8')

                    data_struct_rows.append(
                        '%s%d: {<br>%s%s%s: %s<br>%s%s%s: %s<br>%s}' % (
                            indent, data_field, indent, indent, 'data', item_bytes,
                            indent, indent, 'value', item_parsed, indent
                        )
                    )
                    data_field += 1
                except AssertionError:
                    # not enough bytes to read
                    continue
                except:
                    traceback.print_exc()

            self.result_box.appendHtml('<br>'.join(data_struct_rows))
            self.result_box.appendHtml('}<br><br>')
            self.result_box.appendHtml(hexdump(buf.array(), result='return').replace(' ', '&nbsp;&nbsp;'))
            self.result_box.appendHtml('<br><br><br>')
            row_n += 1
        self.result_box.verticalScrollBar().setValue(pos)
