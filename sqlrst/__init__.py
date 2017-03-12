# coding=utf-8

"""
Transform a RST-annotated SQL piece of text into a RST blocks.
The comments can contain REST text.
"""

import filehelpers

import parser
import printer

__all__ = ['sqlRst2Rst']

def sqlRst2Rst(sqlrstText):
    """
    Convert a sql-rst text into a rst text.
    :param sqlrstText: the sql-rst file
    :return:
    """
    blocks = parser.sqlRstToBlockSequence(sqlrstText)
    return printer.blockSequenceToRst(blocks)

def sqlRstFile2RstFile(inputFile, outputFile):
    """
    Convert a sql-rst file into a rst file
    :param inputFile: the sql-rst file.
    :param outputFile: the rst file.
    """
    filehelpers.generateFile(inputFile, outputFile, sqlRst2Rst)
