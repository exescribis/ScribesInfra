# coding: utf-8

import os.path
import subprocess
import re
import shutil

_login_ = None
_password_ = None
_gh_ = None
_user_ = None
_org_ = None
_repo_ = None


def runCommand(
        commandPattern, keys=None, verbose=False, shell=True,
        raiseOnErrorCode=True, fake=False):
    if keys is None:
        keys = ['key']
    results = {}
    for key in keys:
        command = commandPattern.format(key=key)
        directory = os.getcwd()
        if verbose:
            print '>>> %s     from %s' % (command,directory)

        if fake:
            code = 0
        else:
            code = subprocess.call(
                command,
                shell=shell
            )
        if raiseOnErrorCode and code != 0:
            raise Exception('Command return error %s: %s' % (code, command))
        results[key] = code
    return results


def file_content(filename):
    filename = os.path.expanduser(filename)
    with open(filename, 'r') as f:
        return f.read()

def file_lines(filename):
    return [line.rstrip('\n') for line in open(filename)]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def ensure_no_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def ensure_empty_dir(directory):
    """
    FROM SphinxZone

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
        ensure_dir(directory)

import json

def load_json(filename):
    return json.loads(open(filename).read())

def nameFilter(regexpr=None):
    if regexpr is None:
        return (lambda x: True)
    else:
        return (lambda x: re.match(regexpr, x.name))



import github.GithubObject

def toNotSet(value):
    if value is None:
        return github.GithubObject.NotSet
    else:
        return value