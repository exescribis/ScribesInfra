# coding=utf-8

from modelscripts.megamodels.checkers import NamingChecker
from modelscripts.base.issues import (
    Levels
)
from modelscripts.base .symbols import Symbol

from modelscripts.metamodels.classes import (
    EnumerationLiteral
)

class EnumLiteralNomenclatureChecker(NamingChecker):
    def __init__(self, **params):
        super(EnumLiteralNomenclatureChecker, self).__init__(
            metaclasses=[EnumerationLiteral],
            fun=Symbol.is_camlCase,
            namingName='camlCase',
            **params
        )

EnumLiteralNomenclatureChecker(
    level=Levels.Warning
)