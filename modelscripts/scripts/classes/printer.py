# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import, division
from typing import Text, Union, Optional, Dict, List

from modelscripts.scripts.base.printers import (
    ModelPrinterConfig,
    ModelSourcePrinter
)
from modelscripts.use.use.printer import (
    UseModelPrinter
)
from modelscripts.metamodels.classes import (
    METAMODEL,
    ClassModel
)



class ClassModelPrinter(UseModelPrinter):
    def __init__(self,
                 theModel,
                 config=None):
        #type: (ClassModel, Optional[ModelPrinterConfig]) -> None
        super(ClassModelPrinter, self).__init__(
            theModel=theModel,
            config=config
        )

METAMODEL.registerModelPrinter(ClassModelPrinter)
METAMODEL.registerSourcePrinter(ModelSourcePrinter)

