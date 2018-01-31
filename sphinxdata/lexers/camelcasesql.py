"""
Pygment lexer for "camel case" SQL:
* KEYWORDS must be in uppercases
* CamelCase words are expected to be relation names
* camelCase words are expected to be column names

This code is derived the official lexer `sql.py`_.

..  _`sql.py`:
    https://bitbucket.org/birkenfeld/pygments-main/src/91624f2da452d5e01f3df63f00dd4e82c949274f
    /pygments/lexers/sql.py?at=default&fileviewer=file-view-default

"""

import re
from pygments.lexer import RegexLexer, words
from pygments.token import *




class CamelCaseSqlLexer(RegexLexer):
    """
    Lexer for Structured Query Language. Currently, this lexer does
    not recognize any special syntax except ANSI SQL.
    """

    name = 'SQL'
    aliases = ['sql']
    filenames = ['*.sql']
    mimetypes = ['text/x-sql']

    #%JFE= removed, so that case matters flags = re.IGNORECASE
    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*?\n', Comment.Single),
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (words((
                'ABORT', 'ABS', 'ABSOLUTE', 'ACCESS', 'ADA', 'ADD', 'ADMIN', 'AFTER', 'AGGREGATE',
                'ALIAS', 'ALL', 'ALLOCATE', 'ALTER', 'ANALYSE', 'ANALYZE', 'AND', 'ANY', 'ARE', 'AS',
                'ASC', 'ASENSITIVE', 'ASSERTION', 'ASSIGNMENT', 'ASYMMETRIC', 'AT', 'ATOMIC',
                'AUTHORIZATION', 'AVG', 'BACKWARD', 'BEFORE', 'BEGIN', 'BETWEEN', 'BITVAR',
                'BIT_LENGTH', 'BOTH', 'BREADTH', 'BY', 'C', 'CACHE', 'CALL', 'CALLED', 'CARDINALITY',
                'CASCADE', 'CASCADED', 'CASE', 'CAST', 'CATALOG', 'CATALOG_NAME', 'CHAIN',
                'CHARACTERISTICS', 'CHARACTER_LENGTH', 'CHARACTER_SET_CATALOG',
                'CHARACTER_SET_NAME', 'CHARACTER_SET_SCHEMA', 'CHAR_LENGTH', 'CHECK',
                'CHECKED', 'CHECKPOINT', 'CLASS', 'CLASS_ORIGIN', 'CLOB', 'CLOSE', 'CLUSTER',
                 'FORCE', 'FOREIGN', 'FORTRAN', 'FORWARD', 'FOUND', 'FREE', 'FREEZE', 'FROM', 'FULL',
                'FUNCTION', 'G', 'GENERAL', 'GENERATED', 'GET', 'GLOBAL', 'GO', 'GOTO', 'GRANT', 'GRANTED',
                'GROUP', 'GROUPING', 'HANDLER', 'HAVING', 'HIERARCHY', 'HOLD', 'HOST', 'IDENTITY',
                'IGNORE', 'ILIKE', 'IMMEDIATE', 'IMMUTABLE', 'IMPLEMENTATION', 'IMPLICIT', 'IN',
                'INCLUDING', 'INCREMENT', 'INDEX', 'INDITCATOR', 'INFIX', 'INHERITS', 'INITIALIZE',
                'INITIALLY', 'INNER', 'INOUT', 'INPUT', 'INSENSITIVE', 'INSERT', 'INSTANTIABLE',
                'INSTEAD', 'INTERSECT', 'INTO', 'INVOKER', 'IS', 'ISNULL', 'ISOLATION', 'ITERATE', 'JOIN',
                'COALSECE', 'COBOL', 'COLLATE', 'COLLATION', 'COLLATION_CATALOG',
                'COLLATION_NAME', 'COLLATION_SCHEMA', 'COLUMN', 'COLUMN_NAME',
                'COMMAND_FUNCTION', 'COMMAND_FUNCTION_CODE', 'COMMENT', 'COMMIT',
                'COMMITTED', 'COMPLETION', 'CONDITION_NUMBER', 'CONNECT', 'CONNECTION',
                'CONNECTION_NAME', 'CONSTRAINT', 'CONSTRAINTS', 'CONSTRAINT_CATALOG',
                'CONSTRAINT_NAME', 'CONSTRAINT_SCHEMA', 'CONSTRUCTOR', 'CONTAINS',
                'CONTINUE', 'CONVERSION', 'CONVERT', 'COPY', 'CORRESPONTING', 'COUNT',
                'CREATE', 'CREATEDB', 'CREATEUSER', 'CROSS', 'CUBE', 'CURRENT', 'CURRENT_DATE',
                'CURRENT_PATH', 'CURRENT_ROLE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP',
                'CURRENT_USER', 'CURSOR', 'CURSOR_NAME', 'CYCLE', 'DATA', 'DATABASE',
                'DATETIME_INTERVAL_CODE', 'DATETIME_INTERVAL_PRECISION', 'DAY',
                'DEALLOCATE', 'DECLARE', 'DEFAULT', 'DEFAULTS', 'DEFERRABLE', 'DEFERRED',
                'DEFINED', 'DEFINER', 'DELETE', 'DELIMITER', 'DELIMITERS', 'DEREF', 'DESC',
                'DESCRIBE', 'DESCRIPTOR', 'DESTROY', 'DESTRUCTOR', 'DETERMINISTIC',
                'DIAGNOSTICS', 'DICTIONARY', 'DISCONNECT', 'DISPATCH', 'DISTINCT', 'DO',
                'DOMAIN', 'DROP', 'DYNAMIC', 'DYNAMIC_FUNCTION', 'DYNAMIC_FUNCTION_CODE',
                'EACH', 'ELSE', 'ENCODING', 'ENCRYPTED', 'END', 'END-EXEC', 'EQUALS', 'ESCAPE', 'EVERY',
                'EXCEPTION', 'EXCEPT', 'EXCLUDING', 'EXCLUSIVE', 'EXEC', 'EXECUTE', 'EXISTING',
                'EXISTS', 'EXPLAIN', 'EXTERNAL', 'EXTRACT', 'FALSE', 'FETCH', 'FINAL', 'FIRST', 'FOR',

                'KEY', 'KEY_MEMBER', 'KEY_TYPE', 'LANCOMPILER', 'LANGUAGE', 'LARGE', 'LAST',
                'LATERAL', 'LEADING', 'LEFT', 'LENGTH', 'LESS', 'LEVEL', 'LIKE', 'LIMIT', 'LISTEN', 'LOAD',
                'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCATOR', 'LOCK', 'LOWER',
                'MAP', 'MATCH', 'MAX', 'MAXVALUE', 'MESSAGE_LENGTH', 'MESSAGE_OCTET_LENGTH',
                'MESSAGE_TEXT', 'METHOD', 'MIN', 'MINUTE', 'MINVALUE', 'MOD', 'MODE', 'MODIFIES',
                'MODIFY', 'MONTH', 'MORE', 'MOVE', 'MUMPS', 'NAMES', 'NATIONAL', 'NATURAL', 'NCHAR',
                'NCLOB', 'NEW', 'NEXT', 'NO', 'NOCREATEDB', 'NOCREATEUSER', 'NONE', 'NOT', 'NOTHING',
                'NOTIFY', 'NOTNULL', 'NULL', 'NULLABLE', 'NULLIF', 'OBJECT', 'OCTET_LENGTH', 'OF', 'OFF',
                'OFFSET', 'OIDS', 'OLD', 'ON', 'ONLY', 'OPEN', 'OPERATION', 'OPERATOR', 'OPTION', 'OPTIONS',
                'OR', 'ORDER', 'ORDINALITY', 'OUT', 'OUTER', 'OUTPUT', 'OVERLAPS', 'OVERLAY', 'OVERRIDING',
                'OWNER', 'PAD', 'PARAMETER', 'PARAMETERS', 'PARAMETER_MODE', 'PARAMATER_NAME',
                'PARAMATER_ORDINAL_POSITION', 'PARAMETER_SPECIFIC_CATALOG',
                'PARAMETER_SPECIFIC_NAME', 'PARAMATER_SPECIFIC_SCHEMA', 'PARTIAL',
                'PASCAL', 'PENDANT', 'PLACING', 'PLI', 'POSITION', 'POSTFIX', 'PRECISION', 'PREFIX',
                'PREORDER', 'PREPARE', 'PRESERVE', 'PRIMARY', 'PRIOR', 'PRIVILEGES', 'PROCEDURAL',
                'PROCEDURE', 'PUBLIC', 'READ', 'READS', 'RECHECK', 'RECURSIVE', 'REF', 'REFERENCES',
                'REFERENCING', 'REINDEX', 'RELATIVE', 'RENAME', 'REPEATABLE', 'REPLACE', 'RESET',
                'RESTART', 'RESTRICT', 'RESULT', 'RETURN', 'RETURNED_LENGTH',
                'RETURNED_OCTET_LENGTH', 'RETURNED_SQLSTATE', 'RETURNS', 'REVOKE', 'RIGHT',
                'ROLE', 'ROLLBACK', 'ROLLUP', 'ROUTINE', 'ROUTINE_CATALOG', 'ROUTINE_NAME',
                'ROUTINE_SCHEMA', 'ROW', 'ROWS', 'ROW_COUNT', 'RULE', 'SAVE_POINT', 'SCALE', 'SCHEMA',
                'SCHEMA_NAME', 'SCOPE', 'SCROLL', 'SEARCH', 'SECOND', 'SECURITY', 'SELECT', 'SELF',
                'SENSITIVE', 'SERIALIZABLE', 'SERVER_NAME', 'SESSION', 'SESSION_USER', 'SET',
                'SETOF', 'SETS', 'SHARE', 'SHOW', 'SIMILAR', 'SIMPLE', 'SIZE', 'SOME', 'SOURCE', 'SPACE',
                'SPECIFIC', 'SPECIFICTYPE', 'SPECIFIC_NAME', 'SQL', 'SQLCODE', 'SQLERROR',
                'SQLEXCEPTION', 'SQLSTATE', 'SQLWARNINIG', 'STABLE', 'START', 'STATE', 'STATEMENT',
                'STATIC', 'STATISTICS', 'STDIN', 'STDOUT', 'STORAGE', 'STRICT', 'STRUCTURE', 'STYPE',
                'SUBCLASS_ORIGIN', 'SUBLIST', 'SUBSTRING', 'SUM', 'SYMMETRIC', 'SYSID', 'SYSTEM',
                'SYSTEM_USER', 'TABLE', 'TABLE_NAME', ' TEMP', 'TEMPLATE', 'TEMPORARY', 'TERMINATE',
                'THAN', 'THEN', 'TIMESTAMP', 'TIMEZONE_HOUR', 'TIMEZONE_MINUTE', 'TO', 'TOAST',
                'TRAILING', 'TRANSATION', 'TRANSACTIONS_COMMITTED',
                'TRANSACTIONS_ROLLED_BACK', 'TRANSATION_ACTIVE', 'TRANSFORM',
                'TRANSFORMS', 'TRANSLATE', 'TRANSLATION', 'TREAT', 'TRIGGER', 'TRIGGER_CATALOG',
                'TRIGGER_NAME', 'TRIGGER_SCHEMA', 'TRIM', 'TRUE', 'TRUNCATE', 'TRUSTED', 'TYPE',
                'UNCOMMITTED', 'UNDER', 'UNENCRYPTED', 'UNION', 'UNIQUE', 'UNKNOWN', 'UNLISTEN',
                'UNNAMED', 'UNNEST', 'UNTIL', 'UPDATE', 'UPPER', 'USAGE', 'USER',
                'USER_DEFINED_TYPE_CATALOG', 'USER_DEFINED_TYPE_NAME',
                'USER_DEFINED_TYPE_SCHEMA', 'USING', 'VACUUM', 'VALID', 'VALIDATOR', 'VALUES',
                'VARIABLE', 'VERBOSE', 'VERSION', 'VIEW', 'VOLATILE', 'WHEN', 'WHENEVER', 'WHERE',
                'WITH', 'WITHOUT', 'WORK', 'WRITE', 'YEAR', 'ZONE',
                'INTEGER', #%JFE+
                ), suffix=r'\b'),
             Keyword),
            (words((
                'ARRAY', 'BIGINT', 'BINARY', 'BIT', 'BLOB', 'BOOLEAN', 'CHAR', 'CHARACTER', 'DATE',
                'DEC', 'DECIMAL', 'FLOAT', 'INT', 'INTEGER', 'INTERVAL', 'NUMBER', 'NUMERIC', 'REAL',
                'SERIAL', 'SMALLINT', 'VARCHAR', 'VARYING', 'INT8', 'SERIAL8', 'TEXT'), suffix=r'\b'),
             Name.Builtin),
            (r'[+*/<>=~!@#%^&|`?-]', Operator),
            (r'[0-9]+', Number.Integer),
            # TODO: Backslash escapes?
            (r"'(''|[^'])*'", String.Single),
            (r'"(""|[^"])*"', String.Symbol),  # not a real string literal in ANSI SQL
            (r'[A-Z]\w*', Name.Class),     # %JFE+=   added for relation names starting with upper case
            (r'[a-z]\w*', Name.Attribute), # %JFE+=   added for attribute names starting with lower case
            (r'[a-z_][\w$]*', Name),  # allow $s in strings for Oracle
            (r'[;:()\[\],.]', Punctuation)
        ],
        'multiline-comments': [
            (r'/\*', Comment.Multiline, 'multiline-comments'),
            (r'\*/', Comment.Multiline, '#pop'),
            (r'[^/*]+', Comment.Multiline),
            (r'[/*]', Comment.Multiline)
        ]
    }
