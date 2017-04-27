# coding=utf-8

# Adapted from https://github.com/jackmaney/csv-to-table
# This module infers a typed table from a csv.
#
#
# The MIT License (MIT)
#
# Copyright (c) 2014 Jack Maney
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

import unicodecsv as csv
import re
from collections import OrderedDict
from numbers import Real
import random
from warnings import warn
from dateutil import parser as dateParser

class TypedTable(object):
    """
    A table with column types inferred by their content:

    type ::=
            'text'
        |   'date'
        |   'timestamp'
        |   'numeric'
        |   'smallint'
        |   'bigint'
        |   'int'
        |   'boolean'
        |   'null'     -- if only null values are in a column


    """

    def __init__(self, fileName, header=True, sampleProbability=None,
                 delimiter=',', quotechar='"', tableName=None, columnNames=None,
                 lowercaseHeader=False):
        self.file = fileName
        self.hasHeader = header

        if sampleProbability is not None and not isinstance(sampleProbability, Real) and \
                (sampleProbability > 1 or sampleProbability < 0):
            raise ValueError(
                "The parameter sampleProbability must either be None or a number between 0 and 1")

        self.sampleProbability = sampleProbability
        self.delimiter = delimiter
        self.quoteChar = quotechar
        self.lowercaseHeader = lowercaseHeader
        self.fileSample = []

        self.types = []

        # The data types of the current row
        self._currentTypes = []

        # The data types of the previous row.
        # Once we get the types of the current row, we
        # compare to self.previousTypes and for each column,
        # we take the more general type.
        self._previousTypes = []

        if columnNames is None:
            self._columnNames = []
        else:
            self._columnNames = columnNames

        self.dispatch = {
            "boolean": self.isBool,
            "date": self.isDate,
            "timestamp": self.isTimestamp,
            "numeric": self.isNumeric,
            "int": self.isInteger
        }

        if tableName is None:
            self.tableName = os.path.basename(self.file).replace(".csv", "")
        else:
            self.tableName = tableName

        #: OrderedDict[string,{'indice':int,'type':str,'isNullable':bool}]
        #: orderect dictionnary indexed by the column names and giving
        #: the indice of the column, its type and a boolean indicating if
        #: the column is nullable.
        self.columnInfos = OrderedDict()

        # set self.columnInfos
        self._guessTypes()


    def _sampleFile(self):
        """
        Grabs a list of lists representing a sample of the file.
        The sample is either sampleSize rows or all of the file
        depending on whether or not sampleSize is None.
        While reading through the file, we also make sure that each
        row belongs to the same number of columns.
        """
        result = []
        colCount = None
        rowCounter = 0

        with open(self.file) as f:
            reader = csv.reader(f, delimiter=self.delimiter,
                                quotechar=self.quoteChar)
            for row in reader:
                rowCounter += 1

                if colCount is None:
                    colCount = len(row)
                else:
                    if colCount != len(row):
                        raise Exception(
                            "Column count mismatch at row %d: (%d vs %d)" %
                            (rowCounter, colCount, len(row)))

                if rowCounter == 1 and self.hasHeader:
                    self._columnNames = self._tidyColumns(row)
                    if self.lowercaseHeader:
                        self._columnNames = [x.lower() for x in self._columnNames]
                    continue

                if self.sampleProbability is None or random.random() <= self.sampleProbability:
                    result.append(row)

        self.fileSample = result
        self.types = [(None,False)] * colCount

        if not self.hasHeader and not self._columnNames:
            self._columnNames = ["col" + str(i) for i in list(range(colCount))]



    @staticmethod
    def isNull(string):
        return string.lower() == 'null'

    @staticmethod
    def isBool(string):
        return string.lower() in ["true", "false", "t", "f", "0", "1"]

    @staticmethod
    def isTimestamp(string):
        try:
            dateParser.parse(string)
            return True
        except:
            return False

    @staticmethod
    def isDate(string):
        try:
            dt = dateParser.parse(string)
            return (dt.hour, dt.minute, dt.second) == (0, 0, 0)
        except:
            return False

    @staticmethod
    def isNumeric(string):
        try:
            float(string)
            return True
        except:
            return False

    @staticmethod
    def isInteger(string):
        try:
            a = float(string)
            n = int(a)

            return a == n
        except:
            return False

    @staticmethod
    def _alterColumnName(name):
        return re.sub('[-\s]', '_', name)


    def _tidyColumns(self, columns):
        return map(self._alterColumnName, columns)


    def _guessType(self, s):
        """

        :param s:
        :return:
        """

        # If our field is null, then we have no guess, so return None
        if not s:
            return (None,False)

        if self.isNumeric(s):
            if float(s) == int(float(s)):
                if s == "0" or s == "1":
                    return ("boolean",False)

                if s[0] == "0":
                    return ("text",False)

                if -32768 <= int(float(s)) <= 32767:
                    return ("smallint",False)

                if -2147483648 <= int(float(s)) <= 2147483647:
                    return ("int",False)
                else:
                    return ("bigint",False)
            else:
                return ("numeric",False)
        else:
            if self.isBool(s):
                return ("boolean",False)

            if self.isTimestamp(s):
                if self.isDate(s):
                    return ("date",False)
                else:
                    return ("timestamp",False)

            if self.isNull(s):
                return ('null',True)

        return ("text",False)

    def _reconcileTypes(self):

        for i, currentType in enumerate(self._currentTypes):
            previousType = self._previousTypes[i]
            (currentBaseType,currentIsNullable) = currentType
            (previousBaseType,previousIsNullable) = previousType

            # The idea is that previousType is the most general datatype
            # of the rows that we've seen thus far.
            # So, easy case to deal with: previousType == currentType

            if currentType == previousType:
                # includes both being None
                self.types[i] = currentType
            elif currentBaseType == previousBaseType:
                self.types[i] = (currentBaseType,currentIsNullable or previousIsNullable)
            else:
                # If one of currentType or previousType is None,
                # take whichever isn't None

                if currentBaseType is None:
                    self.types[i] = currentType
                elif previousBaseType is None:
                    self.types[i] = previousType

                # If we find a null value, then take the previous base type and use IsNullable
                if currentBaseType == "null":
                    self.types[i] = (previousBaseType,True)

                # With that out of the way, we'll start with the largest type
                # first:
                elif previousBaseType == "text":
                    self.types[i] = previousType

                # Now, we'll worry about numeric, we switch only if currentType
                # is not a number.
                elif previousBaseType == "numeric":
                    if currentType in ["numeric", "bigint", "int", "smallint", "boolean"]:
                        self.types[i] = (previousBaseType,currentIsNullable or previousIsNullable)
                    else:
                        self.types[i] = ("text",currentIsNullable or previousIsNullable)
                # For bigint, we switch only if currentType is numeric or not a
                # number
                elif previousType == "bigint":
                    if currentType in ["bigint", "int", "smallint", "boolean"]:
                        self.types[i] = (previousBaseType,currentIsNullable or previousIsNullable)
                    elif currentType == "numeric":
                        self.types[i] = ("numeric",currentIsNullable or previousIsNullable)
                    else:
                        self.types[i] = ("text",currentIsNullable or previousIsNullable)
                # Same idea...
                elif previousType == "int":
                    if currentType in ["int", "smallint", "boolean"]:
                        self.types[i] = previousType
                    elif self.types[i] in ["numeric", "bigint"]:
                        self.types[i] = currentType
                    else:
                        self.types[i] = "text"
                # TODO: Set up a tree of types to replace this non-DRY
                # stuff....blarg...
                elif previousType == "smallint":
                    if currentType in ["smallint", "boolean"]:
                        self.types[i] = previousType
                    elif currentType in ["numeric", "bigint", "int"]:
                        self.types[i] = currentType
                    else:
                        self.types[i] = ("text",currentIsNullable or previousIsNullable)
                elif previousType == "boolean":
                    if currentType in ["numeric", "bigint", "int", "smallint", "boolean"]:
                        self.types[i] = currentType
                    else:
                        self.types[i] = ("text",currentIsNullable or previousIsNullable)
                # We just have two cases left...
                elif previousType == "timestamp":
                    if currentType in ["timestamp", "date"]:
                        self.types[i] = currentType
                    else:
                        self.types[i] = ("text",currentIsNullable or previousIsNullable)

    def _guessTypes(self):

        if not self.fileSample:

            self._sampleFile()

            if not self.fileSample:
                warn("No lines found in file %s" % self.file)
                return

        for row in self.fileSample:
            self._currentTypes = [None] * len(row)

            for i, field in enumerate(row):
                self._currentTypes[i] = self._guessType(field)

            if self._previousTypes:
                self._reconcileTypes()

            self._previousTypes = self._currentTypes

        # At this point, we *could* have Nones in self.types if a column has all null values.
        # In that case, we'll guess a type of "text".

        self.types = [(x,isNullable) if x is not None else ("text",False) for (x,isNullable) in self.types]

        self.columnInfos = OrderedDict()
        for i, (columnName,(type,isNullable)) in enumerate(zip(self._columnNames, self.types)):
            self.columnInfos[columnName] = {}
            self.columnInfos[columnName]['indice']=i
            self.columnInfos[columnName]['type']=type
            self.columnInfos[columnName]['isNullable']=isNullable



    def getRowsDict(self):
        """
        Returns a list of rows, each row being a ordered dictionary indexded by column name
        and giving a string representing the value. WARNING: all values are represented
        by their original string without any kind of distinction with respect to type.
        """
        rows = OrderedDict()
        columnNames = self.columnInfos.keys()

        with open(self.file) as f:
            reader = csv.reader(f, delimiter=self.delimiter,
                                quotechar=self.quoteChar)
            rows = list(reader)[1:]
        result = []
        for row in rows:
            d = OrderedDict()
            for column_name, column_value in zip(columnNames,row):
               d[column_name] = column_value
            result.append(d)
        return result

    def _getSQLValue(self, stringValue, type):
        if stringValue.lower() == 'null':
            return 'NULL'
        elif type in ['date', 'timestamp']:
            return "'%s'" % stringValue
        else:
            return "'%s'" %  (stringValue.replace("'","''"))

    def _getSQLInsertStatement(self, rowDict):
        values = [self._getSQLValue(rowDict[column_name], self.columnInfos[column_name]['type'])
                  for column_name in rowDict.keys()]
        return 'INSERT INTO %s VALUES (%s);' % (self.tableName, ','.join(values))

    def getSQLInsertStatements(self):
        rows = self.getRowsDict()
        return '\n'.join(
            [ self._getSQLInsertStatement(row) for row in rows])

    def getSQLCreateStatement(self):
        lines = ["CREATE TABLE %s (" % self.tableName ]
        for i, column in enumerate(self._columnNames):
            (baseType,isNullable) = self.types[i]
            nextLine = "\t" + column + " " + baseType.upper() + ('' if isNullable else ' NOT NULL')
            if i < len(self._columnNames) - 1:
                nextLine += ","
            lines.append(nextLine)
        lines.append(");")

        return "\n".join(lines)


