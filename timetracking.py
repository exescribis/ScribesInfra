import re
import os
import datetime
import timeparse

RE_TRIGRAM = '[A-Z][A-Z][A-Z]'
RE_ISSUE = '#[0-9]+'
RE_DATE= '[0-9][0-9]/[0-9][0-9]/20[0-9][0-9]'
RE_DURATION = '[0-9]*h[0-9]*'
RE_ALL='\s*(?P<trigram>%s)' \
       '\s+(?P<issue>%s)' \
       '\s+(?P<date>%s)' \
       '\s+(?P<duration>%s)' \
       '\s*' \
       % (RE_TRIGRAM, RE_ISSUE, RE_DATE, RE_DURATION)

def minutes(duration):
    """
    Return the number of minutes of the duration given as parameters.
    Acceptable formats are   12h   12h30  15m  plus all formats
    accepted by timeparse. If there is a problem the function returns
    None
    :param duration: The duration
    :return: The number of secondes or None if the parameter is not in
        a valid format.
    """
    if re.match('^[0-9]+h$',duration):
        _ = duration
    elif re.match('^[0-9]+h[0-9]+$', duration):
        _ = duration+'m'
    else:
        _ = duration
    seconds = timeparse.timeparse(_)
    if seconds is None:
        return None
    else:
        return seconds / 60


def _isTimeLine(line):
    m = re.search(RE_DATE, line)
    return m is not None

def _numeredLines(lines, start=1):
    no = start
    _ = []
    for line in lines:
        _ = _ + [(no,line)]
        no += 1
    return _

def _readTimeLines(filename):
    """
    Read a file name and return two lists. The first one is the list
    numbered lines that contains a date (_isTimeLine), the second list
    is those numbered lines that don't seems to contains time information.
    :param filename: The file to be parsed.
    :return: two list. The first one is the numberlist[(noline,line)],list[(noline,line)]
    """
    with open(filename) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    nLines = _numeredLines(lines)

    nTimeLines = []
    nLinesSkipped = []
    for (no,line) in nLines:
        if _isTimeLine(line):
            nTimeLines += [(no,line)]
        else:
            nLinesSkipped += [(no,line)]
    return (nTimeLines, nLinesSkipped)


def _parseTimeLine(lineno, line):
    """
    Parse a time tracking line. Return a ValidTimeTrackingEntry or InvalidTimeTrackingEntry.
    :param lineno: line number of the line
    :param line: text of the line
    :return: TimeTrackingEntry, either valid or invalid
    """
    m = re.match(RE_ALL, line)
    if m is None:
        return InvalidTimeTrackingEntry(
            lineno=lineno,
            line=line,
            errorMessage="Bad format")
    else:
        trigram = m.group('trigram')

        dt = m.group('date')
        try:
            date = datetime.datetime.strptime(dt,'%d/%m/%Y')
        except:
            return InvalidTimeTrackingEntry(
                lineno=lineno,
                line=line,
                errorMessage="Error with the date '%s'. Format is 03/12/2017" % dt)

        duration = minutes(m.group('duration'))
        if duration is None:
            return InvalidTimeTrackingEntry(
                lineno=lineno,
                line=line,
                errorMessage="Invalid duration '%d'. Format is 10h or 1h30 or 30m" % duration)

        issue = m.group('issue')
        if issue[0] != '#':
            return InvalidTimeTrackingEntry(
                lineno=lineno,
                line=line,
                errorMessage= "Issue must start with #. Found '%s'" % issue)
        else:
            try:
                issueNb = int(issue[1:])
            except:
                return InvalidTimeTrackingEntry(
                    lineno=lineno,
                    line=line,
                    errorMessage="Issue specification is incorrect."
                                 " Should be like #23. Found '%s'" \
                                % issue )
        return ValidTimeTrackingEntry(
            lineno=lineno,
            line=line,
            trigram=trigram,
            date=date,
            duration=duration,
            issueNb = issueNb
        )



    # timeTrackingEntries = []
    # nKOTimeLines = []
    # for (no, line) in nTimeLines:
    #     m = re.match(RE_ALL, line)
    #     if m:
    #         te = ValidTimeTrackingEntry(
    #             lineno=no,
    #             line=line,
    #             trigram = m.group('trigram'),
    #             date = m.group('date'),
    #             duration = m.group('duration'),
    #             issueNb = m.group('issue')
    #         )
    #         timeTrackingEntries += [te]
    #     else:
    #         nKOTimeLines += [(no, line)]
    # return (timeTrackingEntries, nKOTimeLines)


# def _readTimeFiles(filename):
#     (nTimeLines, nLinesSkipped) = _readTimeLines(TEST_FILE)
#     (invalidEntries, nKOTimeLines) = _parseTimeLines(nTimeLines)
#     return {
#
#     }

class TimeTrackingEntry(object):
    pass


class InvalidTimeTrackingEntry(TimeTrackingEntry):

    def __init__(self, lineno, line, errorMessage):

        #: line number of the line
        self.lineno = lineno

        #: text of the line
        self.line = line

        #: error message
        self.errorMessage = errorMessage


class ValidTimeTrackingEntry(TimeTrackingEntry):

    def __init__(self, lineno, line, trigram, date, duration, issueNb):

        #: line number of the line
        self.lineno = lineno

        #: text of the line
        self.line = line

        #: trigram
        self.trigram = trigram

        #: date as datetime.datetime
        self.date = date

        #: duration in minutes
        self.duration = duration

        #: issue number (int)
        self.issueNb = issueNb


class TimeTrackingFile(object):

    def __init__(self, filename):
        self.filename = filename
        (nTimeLines, nLinesSkipped) = _readTimeLines(self.filename)


        #: list[(lineno,string)] list of numbered lines that do not
        #: contains a date
        self.nLinesSkipped = nLinesSkipped

        #: valid entries. Initialized by __parseTimeLines
        self.validTimeTrackingEntries = []

        #: valid entries. Initialized by __parseTimeLines
        self.invalidTimeTrackingEntries = []

        self.__parseTimeLines(nTimeLines)


    def __parseTimeLines(self, nTimeLines):
        for (no, line) in nTimeLines:
            entry = _parseTimeLine(no, line)
            if isinstance(entry, InvalidTimeTrackingEntry):
                self.invalidTimeTrackingEntries += [entry]
            else:
                self.validTimeTrackingEntries += [entry]

    def __str__(self):
        return '%s OK, %s KO, %s skipped' % (
            len(self.validTimeTrackingEntries),
            len(self.invalidTimeTrackingEntries),
            len(self.nLinesSkipped)
        )


    def entries(self, trigram=None, date=None):
        _ = []


TEST_DIR = 'test/timetracking/testcases'
TEST_FILE = TEST_DIR+'/case0.rst'



#print '\n'.join(readTimeLines(TEST_FILE))

print TimeTrackingFile(TEST_FILE)

