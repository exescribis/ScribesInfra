
from sphinxdata.lexers.ra import RelationalAlgebraLexer
from sphinxdata.lexers.camelcasesql import CamelCaseSqlLexer
from sphinxdata.sqldomain import SQLTableSignatureNode, html_argumentlist_visit, html_argumentlist_depart, \
    argumentlist_visit, argumentlist_depart, SQLTableColumnNode, html_argument_visit, html_argument_depart, \
    argument_visit, argument_depart, parse_signature_with_kind, \
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