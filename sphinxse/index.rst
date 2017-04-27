sphinxse
========

The sphinxse extension allows to represents some "Software Engineering" (SE)
artefacts using the sphinx documentation generator.

The ``se`` domains introduce directives to define the following objects:
* requirements
* questions
* hypothesis
* remarks
* decisions




Installation
------------

Just include the extension in ``conf.py`` (if not already done)::

    extensions = [
        ...
        'sphinxse',
        ...
    ]

Usage
-----

The extension adds the following directives:

* ``.. se:requirement::``
* ``.. se:question::``
* ``.. se:hypothesis::``
* ``.. se:remark::``
* ``.. se:decision::``

..  todo:: examples to be used

..  todo:: mention to the index and to inline references

..  todo:: add the documentation about xglossary



Development
-----------

The structure of the extension is the following::

    index.rst               documentation of the extension
    __init__.py             extension main code
    sedomain.py             se custom domain
    xglossary.py            xglossary directive
    test/                   directory with some test

Some tests are available in the ``test`` directory::

    cd test/sphinxse
    make clean
    make viewdoc