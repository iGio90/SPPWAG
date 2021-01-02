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
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QDialog, \
    QDialogButtonBox, QHeaderView, QComboBox, QFileDialog

from lib.data_type import DataType, DATA_TYPES, BIG_ENDIAN, LITTLE_ENDIAN


class QDataTypeDialog(QDialog):
    def __init__(self, is_length=False):
        super().__init__()

        if is_length:
            self.setWindowTitle("Select length data type")
        else:
            self.setWindowTitle("Select data type")

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(buttons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        self.data_types_tree = QTreeView()
        self.data_types_tree.setHeaderHidden(True)
        self.data_types_model = QStandardItemModel(0, 1)
        self.data_types_model.setHeaderData(0, Qt.Horizontal, "type")
        self.data_types_tree.setModel(self.data_types_model)
        self.data_types_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)

        self.data_types_tree.selectionModel().selectionChanged.connect(self.selection_changed)
        self.data_types_tree.doubleClicked.connect(self.accept)

        for idx in range(len(DATA_TYPES)):
            _type, length = DATA_TYPES[idx]
            if is_length and self.data_types_model.rowCount() > 4:
                continue

            item = QStandardItem(_type)
            item.setData(idx, Qt.UserRole)
            item.setEditable(False)
            self.data_types_model.appendRow([item])

        self.endianness = QComboBox()
        self.endianness.setEnabled(False)
        self.endianness.addItems([BIG_ENDIAN, LITTLE_ENDIAN])

        self.layout.addWidget(self.data_types_tree)
        self.layout.addWidget(self.endianness)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def selection_changed(self, selected, unselected):
        row = selected.indexes()[0].row()
        self.endianness.setEnabled(row < 4)


class QStructLayout(QVBoxLayout):
    def __init__(self, sppwag):
        super().__init__()

        self.sppwag = sppwag

        title = QLabel("Structure")
        title.setStyleSheet("font: 12pt;")
        self.addWidget(title)

        self.data_tree = QTreeView()
        self.data_tree.setHeaderHidden(True)
        self.data_model = QStandardItemModel(0, 3)
        self.data_tree.setModel(self.data_model)
        self.data_tree.header().setSectionResizeMode(0, QHeaderView.Stretch)

        data_tree_buttons_container = QVBoxLayout()
        data_tree_add_remove_container = QHBoxLayout()
        data_tree_load_save_container = QHBoxLayout()

        data_tree_add = QPushButton("Add")
        data_tree_add.clicked.connect(self.add_data)
        data_tree_remove = QPushButton("Remove")
        data_tree_remove.clicked.connect(self.remove_data)
        data_tree_add_remove_container.addWidget(data_tree_add)
        data_tree_add_remove_container.addWidget(data_tree_remove)

        self.data_tree_save = QPushButton('Save')
        self.data_tree_save.clicked.connect(self.save_struct)
        self.data_tree_save.setEnabled(False)
        data_tree_load_save_container.addWidget(self.data_tree_save)
        data_tree_load = QPushButton('Load')
        data_tree_load.clicked.connect(self.load_struct)
        data_tree_load_save_container.addWidget(data_tree_load)

        data_tree_buttons_container.addLayout(data_tree_add_remove_container)
        data_tree_buttons_container.addLayout(data_tree_load_save_container)

        self.addWidget(self.data_tree)
        self.addLayout(data_tree_buttons_container)

    def add_data(self):
        dlg = QDataTypeDialog()
        if dlg.exec_():
            selections = dlg.data_types_tree.selectionModel().selectedIndexes()
            if len(selections) > 0:
                if dlg.endianness.isEnabled():
                    endianness = dlg.endianness.currentIndex()
                else:
                    endianness = 0

                type_item = dlg.data_types_model.item(selections[0].row(), 0)
                type_index = type_item.data(Qt.UserRole)

                length_type = None
                if type_index > 4:
                    # define length
                    dlg = QDataTypeDialog(True)
                    if not dlg.exec_():
                        return
                    selections = dlg.data_types_tree.selectionModel().selectedIndexes()
                    if len(selections) == 0:
                        return
                    length_endianness = dlg.endianness.currentIndex()
                    length_type = DataType(
                        dlg.data_types_model.item(selections[0].row(), 0).data(Qt.UserRole), length_endianness)

                self.create_data_struct(type_index, endianness, length_type)

                self.invalidate_ui()
                self.sppwag.process()

    def create_data_struct(self, type_index, endianness, length_type):
        data_type = DataType(type_index, endianness, length_type=length_type)
        data_type_const = DATA_TYPES[type_index]

        item_type = QStandardItem(data_type_const[0])
        item_type.setData(data_type, Qt.UserRole)
        item_type.setEditable(False)

        if length_type is None:
            item_length = QStandardItem(str(data_type.get_length()))
        else:
            item_length = QStandardItem(DATA_TYPES[length_type.data_type][0])
        item_length.setEditable(False)

        item_endianness = QStandardItem('big' if endianness == 0 else 'little')
        item_endianness.setEditable(False)
        self.data_model.appendRow([item_type, item_length, item_endianness])

    def remove_data(self):
        selections = self.data_tree.selectionModel().selectedIndexes()
        if len(selections) > 0:
            for x in selections:
                self.data_model.removeRow(x.row())

            self.invalidate_ui()
            self.sppwag.process()

    def save_struct(self):
        struct = []
        for x in self.get_struct():
            struct.append(x.serialize())
        
        file_name, _type = QFileDialog().getSaveFileName(filter="SPPWAG (*.sppwag)", initialFilter="SPPWAG (*.sppwag)")
        if file_name and len(file_name) > 0:
            with open(file_name, 'w') as fp:
                fp.write(json.dumps(struct, indent=2))

    def load_struct(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["SPPWAG (*.sppwag)"])
        dlg.selectNameFilter("SPPWAG (*.sppwag)")
        if dlg.exec_():
            f = dlg.selectedFiles()
            if len(f) > 0:
                f = f[0]
                try:
                    with open(f, 'r') as fp:
                        f = json.load(fp)
                except:
                    return

                self.data_model.setRowCount(0)
                for data in f:
                    length_type = data['length']
                    if length_type is not None:
                        length_type = DataType(length_type['data_type'], length_type['endianness'])
                    self.create_data_struct(data['data_type'], data['endianness'], length_type)
                self.invalidate_ui()
                self.sppwag.process()

    def invalidate_ui(self):
        self.data_tree_save.setEnabled(self.data_model.rowCount() > 0)

    def get_struct(self):
        struct = []
        for row in range(self.data_model.rowCount()):
            item_data_type = self.data_model.item(row, 0)
            struct.append(item_data_type.data(Qt.UserRole))
        return struct
