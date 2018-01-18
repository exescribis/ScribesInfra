# coding=utf-8
from __future__  import print_function

from typing import Text, Dict, Optional
import os

from modelscripts.base.issues import (
    IssueBox,
    Level,
    Levels,
)

from test.modelscripts import (
    getTestFiles,
    getTestFile
)
from modelscripts.megamodels import Megamodel

F=Levels.Fatal
E=Levels.Error
W=Levels.Warning
I=Levels.Info
H=Levels.Hint

ExpectedIssueDict=Optional[Dict[Level, int]]

from modelscripts.megamodels.metamodels import Metamodel

def assertIssueBox(issues, expected=None):
    #type: (IssueBox, ExpectedIssueDict) -> None
    unexpected=False
    if expected is not None:
        actual=issues.summaryMap
        for level in expected:
            if actual[level] != expected[level]:
                print(
                    '##'*6+ \
                    ' TEST FAILED ##### %i %s found. %i expected ' % (
                    actual[level],
                    level.label,
                    expected[level]
                ))
                unexpected = True
        assert not unexpected, 'Unexpected number of issues'



def checkFileIssues(relDir, extension, expectedIssues):
    # For some reason this function is called twice
    # Does not matter too much.
    test_files=getTestFiles(
        relDir,
        relative=True,
        extension=extension)

    l=[]
    for test_file in test_files:
        basename = os.path.basename(test_file)
        expected_issues=(
            None if basename not in expectedIssues
            else expectedIssues[basename])
        l.append((test_file, expected_issues))
    return l

def checkValidIssues(reltestfile, metamodel, expectedIssues):
    #type: (Text, Metamodel, ExpectedIssueDict) -> None
    file=' %s %s ' % (
        metamodel.label,
        os.path.basename(reltestfile)
    )
    print('\ntes:'+'=='*10+' testing '+file+'='*35+'\n' )
    source = metamodel.sourceClass(getTestFile(reltestfile))
    print('\n'+'--' * 10 + ' printing source '+file+'-'*35+'\n')

    metamodel.sourcePrinterClass(source).display()
    print('\n'+'--' * 10 + ' printing model '+'-'*40+'\n')
    metamodel.modelPrinterClass(source.model).display()
    if expectedIssues is None:
        expectedIssues={F: 0, E: 0, W: 0, I: 0, H: 0}
    assertIssueBox(source.fullIssueBox, expectedIssues)
    print('tes:'+'=='*10+' tested '+file+'='*35+'\n' )

def scriptsIterator(m2id, expectedIssues):
    metamodel=Megamodel.theMetamodel(id=m2id)
    res = checkFileIssues(
        metamodel.extension[1:],
        [metamodel.extension],
        expectedIssues)
