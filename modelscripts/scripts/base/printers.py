# coding=utf-8
"""
Base classes for printers and string/color utilities.
"""
from __future__ import unicode_literals, print_function, absolute_import, division
from abc import ABCMeta
from typing import Optional

from modelscripts.base.printers import (
    ContentPrinter,
    ContentPrinterConfig
)
from modelscripts.base.styles import Styles

from modelscripts.metamodels.textblocks import (
    TextBlock
)
from modelscripts.scripts.textblocks.printer import (
    TextBlockPrinter
)

__all__ = (
    'ModelPrinterConfig',
    'ModelPrinter',
    'ModelSourcePrinterConfig',
    'ModelSourcePrinter'
)

class ModelPrinterConfig(ContentPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top',
                 #------------------------
                 contentMode='self', #self|source|model|no
                 summaryMode='top', # top | down | no
                ):
        super(ModelPrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet,
            title=title,
            issuesMode=issuesMode,
            contentMode=contentMode,
            summaryMode=summaryMode
        )


class ModelPrinter(ContentPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theModel,
                 config=None):
        #type: ('Model', Optional[ModelPrinterConfig]) -> None
        assert theModel is not None
        # don't move this line after as getIssueBox
        # is used in __init__
        self.theModel = theModel
        if config is None:
            config=ModelPrinterConfig()
        # TODO: use abstractView parameter
        super(ModelPrinter, self).__init__(
            config=config,
        )

    def getIssueBox(self):
        return self.theModel.issues


    def doContent(self):

        if (self.config.contentMode=='source'
            and self.theModel.source is not None):
            self.doSourceContent()
        else:
            self.doModelContent()
        return self.output

    def doSourceContent(self):
        #FIXME: the called method is not defined  (???)

        self.out(self.theModel.source.str(
            # method='doSourceContent',
            # displayContent=True,
            # preferStructuredContent=False,
            # displaySummary=self.config.summaryMode!='no',
            # summaryFirst=self.config.summaryMode=='top',
            config=self.config
        ))
        return self.output

    def doModelContent(self):
        #FIXME: Change this impl when model has dependency box
        #       Currently only sources has a import box
        #       The model do not have this. See the comment
        #       in the model.py.
        #       The code below  should be changed when
        #       dependency box has been implemented
        from modelscripts.scripts.megamodels.printer.imports import (
            ImportBoxPrinter
        )

        if self.theModel.source is not None:
            ib=self.theModel.source.importBox
            p=ImportBoxPrinter(
                importBox=ib,
                config=self.config
            )
            self.out(p.do())

        return self.output

    def doModelTextBlock(self, textBlock):
        assert isinstance(textBlock, TextBlock)
        s = TextBlockPrinter(textBlock).do()
        self.outLine(s)
        return self.output


class ModelSourcePrinterConfig(ContentPrinterConfig):
    def __init__(self,
                 styled=True,
                 width=120,
                 baseIndent=0,
                 displayLineNos=True,
                 lineNoPadding=' ',
                 verbose=0,
                 quiet=False,
                 #------------------------
                 title=None,
                 issuesMode='top',
                 #------------------------
                 contentMode='self', #self|source|model|no
                 summaryMode='top', # top | down | no
                ):
        super(ModelSourcePrinterConfig, self).__init__(
            styled=styled,
            width=width,
            baseIndent=baseIndent,
            displayLineNos=displayLineNos,
            lineNoPadding=lineNoPadding,
            verbose=verbose,
            quiet=quiet,
            title=title,
            issuesMode=issuesMode,
            contentMode=contentMode,
            summaryMode=summaryMode
        )


class ModelSourcePrinter(ContentPrinter):
    __metaclass__ = ABCMeta

    def __init__(self,
                 theSource,
                 config=None):
        #type: ('ModelSourceFile', Optional[ContentPrinterConfig]) -> None
        assert theSource is not None
        if config is None:
            config=ModelSourcePrinterConfig()
        # don't move this line after as getIssueBox
        # is used in __init__
        self.theSource = theSource  # don't move
        super(ModelSourcePrinter, self).__init__(
            config=config,
        )

    def getIssueBox(self):
        return self.theSource.fullIssueBox


    def doContent(self):
        if (self.config.contentMode in 'model'
            and self.theSource.model is not None):
            self.doModelContent()
        else:
            self.doSourceContent()
        return self.output

    def doModelContent(self):
        # call the str method of the model
        self.out(self.theSource.model.str(
            method='doModelContent',
            # displayContent=True,
            # preferStructuredContent=True,
            # displaySummary=self.config.summaryMode!='no',
            # summaryFirst=self.config.summaryMode=='top',
            config=self.config
        ))
        return self.output

    def doSourceContent(self):
        # display issues with no location included
        self.currentLineNoDisplay=False
        if self.config.issuesMode == 'inline':
            self.doIssues(line=0)
        # display each line of the source
        for (index, line) in enumerate(self.theSource.sourceLines):
            line_no = index + 1
            self.currentLineNoDisplay = True
            self.outLine(line, lineNo=line_no)
            if self.config.issuesMode=='inline':
                self.currentLineNoDisplay = False
                self.doIssues(line=line_no)
        if self.config.issuesMode == 'inline':
            self.currentLineNoDisplay = False
            self.doIssues(
                line=len(self.theSource.sourceLines)+1)
        return self.output

    def doSummary(self):
        super(ModelSourcePrinter, self).doSummary()
        self.out(
            Styles.comment.do(
                str(self.theSource.fullMetrics),
                self.config.styled)
        )
        return self.output
