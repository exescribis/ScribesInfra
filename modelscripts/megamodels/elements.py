# coding=utf-8

from abc import ABCMeta, abstractproperty
from modelscripts.base.sources import SourceElement
from typing import Optional, List

__all__=(
    'ModelElement',
    'SourceModelElement'
)

from modelscripts.base import py
from modelscripts.megamodels.checkers import (
    CheckList
)

class ModelElement(object):
    __metaclass__ = ABCMeta

    def __init__(self, model):
        assert model is not None
        self._model=model
        self.stereotypes=[]
        self.tags=[]
        from modelscripts.metamodels.textblocks import (
            TextBlock
        )
        self.description=TextBlock(
            container=self)

    @property
    def model(self):
        #type: () -> 'Model'
        return self._model

    @model.setter
    def model(self, model):
        self._model=model

    @property
    def children(self):
        r = []
        if hasattr(self, 'META_COMPOSITIONS'):
            for child_name in getattr(self, 'META_COMPOSITIONS'):
                l = py.getObjectValues(
                    self, child_name, asList=True)
                for e in l:
                    if e not in r:
                        r.append(e)
        return r

    def check(self):
        CheckList.check(self)
        for child in self.children:
            child.check()

    # @abstractproperty
    # def parent(self):
    #     #type: () -> Optional[ModelElement]
    #     raise NotImplementedError('no parent for ' % type(self).__name__)
    #
    # @property
    # # type: () -> List[ModelElement]
    # def children(self):
    #     return []
    #
    # @property
    # # type: () -> List[ModelElement]
    # def descendents(self):
    #     all=[d
    #          for c in self.children
    #             for d in c.children]
    #     return all


class SourceModelElement(ModelElement, SourceElement):
    __metaclass__ = ABCMeta


    def __init__(self,
                 model,
                 name=None,
                 code=None,
                 lineNo=None,
                 docComment=None,
                 eolComment=None):
        assert model is not None
        from modelscripts.megamodels.models import Model
        assert isinstance(model, Model)
        SourceElement.__init__(self,
            name = name,
            code = code,
            lineNo = lineNo,
            docComment = docComment,
            eolComment = eolComment)
        ModelElement.__init__(self, model)
        if self.source is not None:
            self.source._addSourceModelElement(self)

    @property
    def source(self):
        return self.model.source


