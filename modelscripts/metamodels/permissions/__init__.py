# coding=utf-8
"""

"""


from __future__ import absolute_import, division, print_function, unicode_literals
from typing import List, Optional
from modelscripts.megamodels.dependencies.metamodels import (
    MetamodelDependency
)
from modelscripts.megamodels.metamodels import Metamodel
from modelscripts.base.metrics import Metrics

# ---------------------------------------------------------------
#  Abstract syntax
# ---------------------------------------------------------------
from modelscripts.metamodels.permissions.gpermissions import (
    Permission,
    PermissionSet,
    PermissionModel,
    PermissionRule
)
from modelscripts.metamodels.permissions.sar import (
    Action,
    SAR
)
from modelscripts.metamodels.permissions.sar import (
    Subject,
    Resource,
    Action,
)
from modelscripts.metamodels.usecases import (
    UsecaseModel
)


ClassModel='ClassModel'

#------------------------------------------------------------------------------
#    Usecases/Classes specific
#------------------------------------------------------------------------------

CreateAction = Action('C', None)
ReadAction = Action('R', None)
UpdateAction = Action('U', None)
DeleteAction = Action('D', None)
ExecuteAction = Action('X', None)


class FactorizedPermissionRule(PermissionRule):
    def __init__(self, model, subjects, actions, resources, lineNo=None):
        #type: (UCPermissionModel, List[Subject], List[Action], List[Resource])->None
        super(FactorizedPermissionRule, self).__init__(
            model=model,
            lineNo=lineNo)
        self.subjects=subjects      #type: List[Subject]
        self.actions=actions        #type: List[Action]
        self.resources=resources    #type: List[Resource]

    def __str__(self):
        return '%s %s %s' % (
            ','.join([s.subjectLabel for s in self.subjects]),
            ','.join([s.actionLabel for s in self.actions]),
            ','.join([s.resourceLabel for s in self.resources]),
        )


class UCPermissionModel(PermissionModel):

    def __init__(self):
        # #type: (UsecaseModel, ClassModel, SourceFile) -> None
        super(UCPermissionModel, self).__init__()

        self.usecaseModel=None #type: Optional[UsecaseModel]
        #set later

        self.classModel=None #type: Optional[ClassModel]

        self.rules=[]             #type: List[FactorizedPermissionRule]

        self._permissionSet=None   #type: Optional[PermissionSet]

    @property
    def metamodel(self):
        #type: () -> Metamodel
        return METAMODEL

    @property
    def permissionSet(self):
        #type: ()->PermissionSet
        if self._permissionSet is None:
            self._interpret()
        # noinspection PyTypeChecker
        return self._permissionSet

    @property
    def metrics(self):
        #type: () -> Metrics
        ms=super(UCPermissionModel, self).metrics
        ms.addList((
            ('rule', len(self.rules)),
            ('permission', len(self.permissionSet.permissions) ),
        ))
        return ms

    def _interpret(self):
        #type: ()->None
        self._permissionSet= PermissionSet()
        for rule in self.rules:
            for s in rule.subjects:
                for r in rule.resources:
                    for a in rule.actions:
                        p= Permission(s, a, r, rule)
                        self._permissionSet.permissions.add(p)
                        rule.permissions.append(p)

    def __str__(self):
        return '\n'.join([str(r) for r in self.rules])


METAMODEL=Metamodel(
    id='pe',    # other model could be registered
    label='permission',
    extension='.pes',
    modelClass=UCPermissionModel
)
MetamodelDependency(
    sourceId='pe',
    targetId='gl',
    optional=True,
    multiple=True,
)
MetamodelDependency(
    sourceId='pe',
    targetId='us',
    optional=False,
    multiple=False,
)
MetamodelDependency(
    sourceId='pe',
    targetId='cl',
    optional=False,
    multiple=False,
)