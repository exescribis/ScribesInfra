sphinxuseocl
============

The sphinxuseocl extension allow to document `USE OCL`_ projects with the sphinx
documentation generator. It provides syntax highlighting for `USE OCL`_ language.

..  _`USE OCL`: http://scribetools.readthedocs.io/en/latest/useocl/

Installation
------------
Just include the extension in ``conf.py`` (if not already done)::

    extensions = [
        ...
        'sphinxuseocl',
        ...
    ]

Usage
-----

USE OCL code can be highlighted as following::

    ..  code-block:: useocl

        model SimpleModel

        enum Season {winter, autumn, spring, summer}

        class Yellow
        end

Alternatively a USE OCL file can be included like that::

    ..  literalinclude:: state001.soil
        :language: useocl

Options of the `literalinclude`_ directive can be used::

    ..  literalinclude:: state001.soil
        :language: useocl
        :emphasize-lines: 12,15-18
        :linenos:

..  _`literalinclude`: http://www.sphinx-doc.org/en/stable/markup/code.html#includes

Development
-----------

The structure of the extension is the following::

    index.rst               documentation of the extension
    __init__.py             extension main code
    useocllexer.py          lexer for code highlighting
    test/                   directory with some tests

Some tests are available in the ``test`` directory::

    cd test/sphinxuseocl
    make clean
    make viewdoc