"""
sphinxdata extension for sphinx processor.

Adds a 'sql' domain.
Adds lexer for 'sql' and 'relational_algebra'.
"""
from sphinxdata.lexers.ra import RelationalAlgebraLexer
from sphinxdata.lexers.camelcasesql import CamelCaseSqlLexer
from sphinxdata.sqldomain import \
    app_add_node_addSQLTableSignatureNode, \
    app_add_node_addSQLTableColumnNode, \
    sql_custom_domain


def setup(app):

    app.add_lexer('relational_algebra', RelationalAlgebraLexer() )
    app.add_lexer('sql', CamelCaseSqlLexer())

    #--- Add node for signatures are parameters
    app_add_node_addSQLTableSignatureNode(app)
    app_add_node_addSQLTableColumnNode(app)

    app.add_domain(sql_custom_domain)