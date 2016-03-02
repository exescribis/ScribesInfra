# coding=utf-8

"""

"""



import structure

__all__ = ['blockSequenceToRst']

def indent(n, s):
    return '\n'.join([' '*n*4+l for l in s.split('\n')])

def codeBlock(text, indentation=0, language='sql'):
    return indent(
                indentation,
                '.. code-block:: %s\n' % language
                + '    :linenos: \n'
                + '\n'
                + indent(1, text)
                + '\n'
    )

def commentToRst(block):
    return block.content()

def selectStatementToRst(block, indentSQL):
    return codeBlock(block.content(), indentation=indentSQL)

def createTableStatementToRst(block, indentSQL):
    return codeBlock(block.content(),  indentation=indentSQL)

def createViewTStatementToRst(block, indentSQL):
    return codeBlock(block.content(),  indentation=indentSQL)

def unknownTStatementToRst(block, indentSQL):
    return codeBlock(block.content(), indentation=indentSQL)


def blockToRst(block, indentSQL=0):
    """
    :param block: the block to convert into rst
    :param indentSQL: the indentation for the block. 0 by default
    :return: the block represented in rst
    """
    if (isinstance(block, structure.CommentBlock)):
        return commentToRst(block)
    elif (isinstance(block, structure.SelectStatementBlock)):
        return selectStatementToRst(block, indentSQL)
    elif (isinstance(block, structure.CreateTableStatementBlock)):
        return createTableStatementToRst(block, indentSQL)
    elif (isinstance(block, structure.CreateViewStatementBlock)):
        return createViewTStatementToRst(block, indentSQL)
    elif (isinstance(block, structure.UnknownStatementBlock)):
        return unknownTStatementToRst(block, indentSQL)
    else:
        raise NotImplementedError(
                'unknown block: %s' % str(type(block)))

def blockSequenceToRst(blocks, indentSQL=0):
    return '\n'.join([ blockToRst(block,indentSQL) for block in blocks])