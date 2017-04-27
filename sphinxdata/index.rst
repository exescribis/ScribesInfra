sphinxdata
==========

``sphinxdata`` provide support for documenting relation algebra and relation models with
the sphinx_ documentation generator.

It provides syntax highlighting for
* relational algebra expressions
* camlCased SQL

It also provides a `sphinx domain` to define sql objects (table, queries, views and constraints),
reference them and include them in the document index.

Installation
------------

Add the extension in your configuration file (if not already done). ``conf.py`` should look like::

    extensions = [
        ...                # some extensions
        'sphinxdata',
        ...                # other extensions
    ]

The sql domain
--------------

The sql domain is a `sphinx domain`_ for SQL. It adds 4 directives allowing to
define 4 kinds of top-level sql objects.

* ``.. sql:table::`` for describing tables,
* ``.. sql:query::`` for describing queries,
* ``.. sql:view::`` for describing views,
* ``.. sql:constraint::`` for describing constraints.

Global objects defined with these directives are added to the index.
They can also be referenced inline (anywhere within regular text) with corresponding roles:
* ``:sql:table:`MyTable``` refers to the table ``MyTable``
* ``:sql:query:`MyQuery``` refers to the query ``MyQuery``
* ``:sql:view:`MyView``` refers to the view ``MyView``
* ``:sql:constraint:`MyConstraint``` refers to the view ``MyConstraint``

The definition of tables, queries and views have the same structure.
* a signature
* a blank line
* the description of the table
* the list of fields description

Possible fields are:
* **col**umns.
* **con**straints.
* **ex**amples.

Note that constraints can be described locally (within tables, queries and views) or globally with the
directive ``sql:table::``. Only global constraints are included in the index.


The ``.. sql:table::`` directive allows to describe a table::

    ..  sql:table:: MyTable( #key1:i, #key2:s, att1:d, att2:d?, fkA:i?>, fkB:i> )

        Description of the table.

        :col key1: description of key1. Part of a key because it starts with '#' character.
        :col key2: second part of the key.
        :col att: description of regular column att of type date.
        :col fkA: description of the foreign key A

        :con con1: description of the constraint

        :con con2: description of the constraint

        :ex: here is an example.

To keep the notation short and concise the following codes are used.

==== ============ =============== ====================================================================================
code meaning      context         description
==== ============ =============== ====================================================================================
col  column       table element   Declare a column with its name.  e.g. ``:col age: Age of the person.``
con  constraint   table element   Declare a [named] constraint.   e.g.``:con ageRange: age must be between 0 and 120.
ex   example      table element   Provide an example of a tuple.  e.g. ``:ex example1: (3,'paul',18) means that ... ``
i    integer      attribute type  Represents any integer type.
s    string       attribute type  Represents any string type.
r    real         attribute type  Represents any floating number type.
d    date         attribute type  Represents a date.
#    key          attribute kind  The attribute is part of the table primary key.
>    foreign key  attribute kind  The attribute is (part) of a reference to another table.
?    optional     attribute kind  The attribute is optional (can be NULL)
!    mandatory    attribute kind  The attribute is mandatory (is NOT NULL)
==== ============ =============== ====================================================================================


To simply (a bit) the rst source one can set ``sql`` as the default domain with the following directive::

    ..  default-domain:: sql

Then all following references will be interpreted according to the sql domain.
For instance the reference ``:table:`Products``` will just mean ``:sql:table:`Products```.


Relational algebra
------------------

Block of relational algebra code could be highlighted like that::

    ..  code-block:: relational_algebra

        Spectators(id,birthYear,city) := Bands[band,city]:(city = 'Brisbane')
        Spectators[id,city]


CamelCased SQL
--------------

SQL code can be highlighted as following::

    ..  code-block:: sql

        /* example of table */
        CREATE TABLE Spectators(
            name VARCHAR(100),     -- some inline comment
            birthYear INTEGER,
            city VARCHAR(100)
        );

Alternatively a sql file can be included::

    ..  literalinclude:: mySqlFile.sql
        :language: sql

Options of the `literalinclude`_ directive can be used::

    ..  literalinclude:: mySqlFile.sql
        :language: sql
        :emphasize-lines: 12,15-18
        :linenos:


The following coding conventions are assumed:
* SQL keywords must be in UPPERCASES.
* Identifiers in CamelCase are assumed to be global identifiers (tables, views).
* Identifiers in camelCase are assumed to be column names.
The syntax is not checked and the coding conventions are just helpers.


Development
-----------

The structure of the extension is the following::

    index.rst               documentation of the extension
    __init__.py             extension main code
    sqldomain.py            sql custom domain
    lexers/                 lexers for code highligthing
        camelcasedsql.py    lexer for camel case sql
        ra.py               lexer for relation algebra
    test/                   directory with some test

Some tests are available in the ``test`` directory::

    cd test/sphinxdata
    make clean
    make viewdoc


..  _sphinx:
    http://www.sphinx-doc.org

..  _`sphinx domain`:
    http://www.sphinx-doc.org/en/stable/domains.html#domains


..  _`literalinclude`: http://www.sphinx-doc.org/en/stable/markup/code.html#includes