#!/usr/bin/env bash
"""
cat $1 \
    | egrep '(: WARNING: |: SEVERE:)' \
    | sed \
        -e 's/.*WARNING/WARNING:/' \
        -e 's/undecodable source characters,.*/undecodable source characters/' \
        -e 's/download file not readable:.*/download file not readable/' \
        -e 's/Include file .* not found or reading it failed/Include file not found or reading it failed/' \
        -e 's/.*SEVERE/SEVERE:/' \
        -e 's/toctree contains reference to nonexisting document .*/XXXX/' \
    | sort \
    | uniq -c

echo
echo 'Errors sorted by file'
echo

cat $1 \
    | egrep '(: WARNING: |: SEVERE:)' \
    | sed \
        -e 's/WARNING:.*//' \
        -e 's/SEVERE:.*//' \
        -e 's/:[0-9]*://' \
    | sort \
    | uniq -c
"""

import re

import problems


def shortenedMessage(message):
    """
    Check if the message should be shortened or is parametrized by some value(s).
    If this is the case return the shortened form as well as a detail message.
    Otherwise return the message and the empty string since no details is needed.
    :param message: the message to shorten
    :return: (str,str)
    """
    patterns = [
        ('Include file (?P<file>.*) not found or reading it failed',
            'Include file not found'),
        ('download file not readable: (?P<file>.*)',
            'Download file not readable'),
        ('toctree contains reference to nonexisting document (?P<document>.*)',
            'Non existing document'),
        ('.*undecodable source characters, replacing with.*',
            'Undecodable characters'),
        ('.* reference target not found: .*',
            'Reference not found'),
        ('reference not found: .*',   # warning generated by missingrefs
            'Reference not found'),
        ('image file not readable: .*',
            'Image file not readable'),
        ('duplicate label .*',
            'Duplicate label'),
        ('toctree contains reference to document .* that doesn\'t have a title',
            'Untitled document in toctree'),
        ('Duplicate ID:.*',
            'Duplicate ID')
    ]
    for (pattern,replacement) in patterns:
        m = re.match(pattern, message)
        if m:
            return (replacement, message)
    return (message,'')



def parseErrorFile(sphinxRootDirectory, file, problemManager):
    """
    Parse the output of sphinx errors and add the problems to the problems.MANAGER.
    Unrecognized lines (e.g. lines at the begining of the file that are not
    WARNING,ERROR,SEVERER) produce UnknownProblem.
    :param file: an error file generated by sphinx
    :return: list[problems.Problem] the list of problem created.
    """
    problem_pattern = \
        "^(?P<file>.*):(?P<line>\d*): *(?P<type>WARNING|ERROR|SEVERE): *(?P<message>.*)"

    lines = [line.rstrip('\n') for line in open(file)]
    current_problem = None   # could be set to an UnknownProblem
    problem_list = []
    for line in lines:
        m=re.match(problem_pattern, line)
        if m:
            (short_message, detail) = shortenedMessage(m.group('message'))
            current_problem = problems.Problem(
                    sphinxRootDirectory=sphinxRootDirectory,
                    source=m.group('file'),
                    type=m.group('type'),
                    line=int(m.group('line')) if m.group('line') != '' else 0,
                    message=short_message,
                    content=detail
                )
            problemManager.addProblem(current_problem)
            problem_list.append(current_problem)
        else:
            if current_problem is None:
                # a unrecognized line at the beginning of the file
                current_problem = problems.UnknownProblem(content=line)
                problemManager.addProblem(current_problem)
                problem_list.append(current_problem)
            else:
                # content line for last problem
                current_problem.appendToContent(line)



# ^(?P<file>:\d+\:WARNING:)/media/jmfavre/Windows/DEV/m2cci/m2cci-pi-groups/m2cci-pi-GPI01/Donnees/ModeleLogique/Index.rst:29: WARNING: Title underline too short.