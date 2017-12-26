# coding=utf-8

from modelscripts.megamodels.checks import Checker
from modelscripts.base.issues import (
    Levels
)

from modelscripts.metamodels.scenarios.evaluations.operations import (
    _USEImplementedAssertQueryEvaluation
)

class QueryAssertChecker(Checker):

    def __init__(self, level, params=None):
        super(QueryAssertChecker, self).__init__(
            classes=[_USEImplementedAssertQueryEvaluation ],
            name='QueryAssertChecker',
            level=level,
            params=params
        )


    def doCheck(self, e):
        #:type ('EnumerationLiteral') -> None
        if e.status != 'OK':
            return (
                'Assert is %s (%s : %s)' % (
                    e.status,
                    e.resultValue,
                    e.resultType
            ))
        else:
            return None

QueryAssertChecker(
    level=Levels.Error
)