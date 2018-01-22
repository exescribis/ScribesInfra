# coding: utf-8

from collections import OrderedDict
import re

class Field(object):
    def __init__(self, name):
        self.name=name

class PresetField(Field):
    def __init__(self, name, value):
        super(PresetField, self).__init__(name)
        self.value=value

class InputField(Field):
    def __init__(self, name, question, regexp=None):
        super(InputField, self).__init__(name)
        self.question=question
        self.regexp=regexp
        self.value=None

    def getValue(self):
        while True:
            value=raw_input(self.question + ' ?')
            if re.match(self.regexp, value):
                break
            else:
                print('Illegal value: %s' % value)
        self.value=value
        return value


FIELDS=[
    InputField(
        'firstName',
        'Votre prénom en minuscules:',
        '[a-z \-]+'),
    InputField(
        'lastName',
        'Votre nom en majuscules   :',
        '[A-Z \-]+'),
    InputField(
        'email',
        'Votre email               :',
        '[A-Za-z0-9_\.\-]+@[A-Za-z0-9_\.\-]+'),
    InputField(
        'group',
        'Votre groupe (exemple G07):',
        'G[0-1][0-9]'),
    PresetField(
        'proxy',
        'http://www-cache.ujf-grenoble.fr:3128'),
    PresetField(
        'editor',
        'editor=gedit -w -s'),
    PresetField(
        'classroom',
        'm2r'),
    PresetField(
        'course',
        'aeis'),
    PresetField(
        'years',
        '1718')
]

TEMPLATE="""
# enter the folowing commands, one by one, in a shell window
git config --global user.name "{firstName} {lastName}"
git config --global user.email "{email}"
git config --global credential.helper "cache --timeout=7200"
git config --global http.proxy {proxy}
git config --global core.editor "{editor}"
git clone https://github.com/{classroom}/{classroom}-{years}-{course}-{group}
cd {classroom}-{years}-{course}-{group}
git remote add root https://github.com/{classroom}/{classroom}-{years}-{course}-root.git
git pull root master
"""

"""


----
git add .
git commit -a -m "Set the authors for this repository"
git push origin master
"""


def getMap(fields):
    map=OrderedDict()
    for field in fields:
        if isinstance(field, PresetField):
            map[field.name]=field.value
        elif isinstance(field, InputField):
            map[field.name]=field.getValue()
        else:
            raise NotImplementedError()
    return map

def replace(template, map):
    return template.format(**map)

m=getMap(FIELDS)
print( replace(TEMPLATE, m))