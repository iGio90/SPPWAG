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

BIG_ENDIAN = 'big endian'
LITTLE_ENDIAN = 'little endian'

DATA_TYPES = [
    ('byte', 1),
    ('short', 2),
    ('int', 4),
    ('long', 8),
    ('varInt', 0),
    ('string', 0),
    ('array', 0)
]


class DataType:
    def __init__(self, data_type, endianness, length_type=None):
        self.data_type = data_type
        self.endianness = endianness
        self.length_type: DataType = length_type

    def get_length(self):
        return DATA_TYPES[self.data_type][1]

    def get_endianness_value(self):
        return 'big' if self.endianness == 0 else 'little'
