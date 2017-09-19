# coding: utf-8
import json
import os

def load_json(filename):
    return json.loads(open(filename).read())


def file_content(filename):
    filename = os.path.expanduser(filename)
    with open(filename, 'r') as f:
        return f.read()
