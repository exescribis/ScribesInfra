# coding=utf-8

import os
import codecs
import shutil

def ensureDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensureNoFile(file):
    if os.path.isfile(file):
        os.remove(file)

def ensureEmptyDir(directory):
    """
    Ensure that the directory exists but that is empty.
    If it does not exist, create it.
    If it exist remove everything in it.
    :param directory: The directory to create/empty
    """
    # http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    if os.path.isdir(directory):
        for file_object in os.listdir(directory):
            file_object_path = os.path.join(directory, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)
            # TODO: this will fail for symbolic link
    else:
        ensureDirectory(directory)

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
