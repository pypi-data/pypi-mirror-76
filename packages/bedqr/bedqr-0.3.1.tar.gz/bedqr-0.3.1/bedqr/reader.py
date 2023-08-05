# -*- python -*-
#
# Copyright 2018, 2019, 2020 Liang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
'''
bedqr.reader

file I/O wrapper
'''

from bedqr.format import BED, bedDetail


class Reader(object):
    '''
    base-class of file reader
    '''

    def load_file_with_parser(self, parser_cls):
        file_content = self._fp.read()
        lines = file_content.splitlines()
        flags = map(parser_cls.detect_line_type, lines)
        line_count = len(lines)
        parts = {
            'header': [ lines[i] for i in range(line_count) if flags[i]==parser_cls.ROW_TYPE['HEADER'] ],
            'body'  : [ lines[i] for i in range(line_count) if flags[i]==parser_cls.ROW_TYPE['BODY'] ],
        }
        return parser_cls(parts)


class QuickReader(Reader):
    '''
    class should be used by general users
    '''

    def __init__(self, fp, parser=bedDetail):
        self._fp = fp
        self.data = self.load_file_with_parser(parser)


