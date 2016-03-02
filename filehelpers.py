# coding=utf-8

import os
import codecs

def ensureDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensureNoFile(file):
    if os.path.isfile(file):
        os.remove(file)

def touchFile(file, times=None):
    with open(file, 'a'):
        os.utime(file, times)

def fileContent(file):
    with codecs.open(file, 'r', 'utf-8') as f:
        content = f.read()
    return content

def saveContent(file, content):
    with codecs.open(file, "w", "utf-8") as f:
        f.write(content)

def directoryItemPaths(directory, predicate=os.path.isdir):
    _ = []
    for name in os.listdir(directory):
        path = os.path.join(directory,name)
        if predicate(path):
            _.append(path)
    return _

def generateFile(inputFilename, outputFilename, str2strFun):
    input = fileContent(inputFilename)
    output = str2strFun(input)
    saveContent(outputFilename, output)

def removeTrailingSeparator(filename):
    if filename.endswith(os.sep):
        return filename[:-1]
    else:
        return filename
