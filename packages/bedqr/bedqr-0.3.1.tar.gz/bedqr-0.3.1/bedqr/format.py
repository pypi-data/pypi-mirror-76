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
bedqr.format

file format specification: https://genome.ucsc.edu/FAQ/FAQformat.html
'''

from bedqr.base import FileWithHeaderAndContent


class RowBasedStore(object):
    ROW_TYPE = {
        'HEADER' :  0,
        'BODY'   :  1,
        'EMPTY'  : -1,
        'INVALID': -2,
    }

    def get_cells_from_row(self, row):
        #ret = list()
        ret = row.split(self.FIELD_SEP)
        return ret


class BED(FileWithHeaderAndContent, RowBasedStore):
    '''
    Browser Extensible Data (BED)
    '''

    REQUIRED_FIELDS = ('chrom', 'chromStart', 'chromEnd')
    OPTIONAL_FIELDS = ('name', 'score', 'strand', 'thickStart', 'thickEnd', 'itemRgb', 'blockCount', 'blockSizes', 'blockStarts')
    HEADER_PREFIX = ('browser', 'track')
    FIELD_EMPTY_VALUE = '.'
    FIELD_CHROM_REGEX = ('chr[0-9a-zA-Z_]+', 'scaffold[0-9]+')

    def get_column_names(self, data):
        '''
        :param data: (list of string/tuple)
        '''
        ret = self.REQUIRED_FIELDS + self.OPTIONAL_FIELDS
        detected_column_count = 0 #len(ret)
        if len(data):
            first_row = data[0]
            if isinstance(first_row, (list, tuple)):
                detected_column_count = len(first_row)
            elif isinstance(first_row, (basestring, unicode)):
                #detected_column_count = len(first_row.split(self.FIELD_SEP))
                detected_column_count = len(self.get_cells_from_row(first_row))
            else:
                # TODO: need to find a strategy to deal with unknown/foreign/unpredictable types/classes
                #raise ValueError('cannot parse data row')  # caller or somewhere else deal with this exception
                #detected_column_count = len(first_row)  # call dumb boilerplate instance method
                #detected_column_count = first_row.get_size()  # or the object's public interface
                pass
        return ret[:detected_column_count]

    @classmethod
    def detect_line_type(cls, line):
        CHOICE = cls.ROW_TYPE
        ret = CHOICE['INVALID']

        class FoundMatchSignal(Exception):
            def __init__(self, *args, **kwargs):
                self.found = kwargs.pop('found', None)
                super(FoundMatchSignal, self).__init__(*args, **kwargs)

        try:
            if len(line) == 0:
                raise FoundMatchSignal(found=CHOICE['EMPTY'])

            header_prefix = cls.HEADER_PREFIX
            for item in header_prefix:
                if line.startswith(item):
                    raise FoundMatchSignal(found=CHOICE['HEADER'])

            data_prefix = map(lambda x: x.split('[', 1)[0], cls.FIELD_CHROM_REGEX)
            for item in data_prefix:
                if line.startswith(item):
                    raise FoundMatchSignal(found=CHOICE['BODY'])
        except FoundMatchSignal as match:
            ret = match.found
        #except Exception as ex:
        #    raise
        return ret


class bedDetail(BED):
    '''
    BED detail
    '''
    FIELD_SEP = '\t'

    DETAIL_FIELDS = ('id', 'description')

    def __init__(self, data, **kwargs):
        super(bedDetail, self).__init__(**kwargs)
        if isinstance(data, dict):
            if data.has_key('header') and data.has_key('body'):
                self._parts = list()
                self._parts.append(data['header'])
                self._parts.append(data['body'])

    def get_column_names(self, data):
        columns_a = super(bedDetail, self).get_column_names(data)
        columns_b = ([ None for i in columns_a ] + list(self.DETAIL_FIELDS))[len(self.DETAIL_FIELDS):]
        return map(lambda x, y: y if y is not None else x, columns_a, columns_b)


