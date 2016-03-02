"""
    derived from sphinx.domains.std
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The standard domain.
    :copyright: Copyright 2007-2015 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.

    https://github.com/sphinx-doc/sphinx/blob/e4b9eb51f6c1af894b4fc6da08e54035b5dd5f36/sphinx/domains/std.py
"""



from docutils.parsers.rst import directives
from sphinx.util.compat import Directive
from sphinx import addnodes
from docutils.statemachine import ViewList
from docutils import nodes
import unicodedata




class XGlossary(Directive):
    """
    Directive to create a glossary with cross-reference targets for :term:
    roles.
    """

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'sorted': directives.flag,
    }

    def run(self):


        def _make_termnodes_from_paragraph_node(env, node, new_id=None):
            gloss_entries = env.temp_data.setdefault('gloss_entries', set())
            objects = env.domaindata['std']['objects']

            termtext = node.astext()
            if new_id is None:
                new_id = nodes.make_id('term-' + termtext)
            if new_id in gloss_entries:
                new_id = 'term-' + str(len(gloss_entries))
            gloss_entries.add(new_id)
            objects['term', termtext.lower()] = env.docname, new_id

            # add an index entry too
            indexnode = addnodes.index()
            indexnode['entries'] = [('single', termtext, new_id, 'main')]
            new_termnodes = []
            new_termnodes.append(indexnode)
            new_termnodes.extend(node.children)
            new_termnodes.append(addnodes.termsep())
            for termnode in new_termnodes:
                termnode.source, termnode.line = node.source, node.line

            return new_id, termtext, new_termnodes


        def make_term_from_paragraph_node(termnodes, ids):
            # make a single "term" node with all the terms, separated by termsep
            # nodes (remove the dangling trailing separator)
            term = nodes.term('', '', *termnodes[:-1])
            term.source, term.line = termnodes[0].source, termnodes[0].line
            term.rawsource = term.astext()
            term['ids'].extend(ids)
            term['names'].extend(ids)
            return term



        # %JFE+[
        if len(self.arguments) >= 1:
            self.glossaryName = self.arguments[0]
        else:
            self.glossaryName = ''

        # %JFE+]

        env = self.state.document.settings.env
        node = addnodes.glossary()     # %JFE= TODO:
        node.document = self.state.document

        # This directive implements a custom format of the reST definition list
        # that allows multiple lines of terms before the definition.  This is
        # easy to parse since we know that the contents of the glossary *must
        # be* a definition list.

        # first, collect single entries
        entries = []
        in_definition = True
        was_empty = True
        messages = []
        for line, (source, lineno) in zip(self.content, self.content.items):
            # empty line -> add to last definition
            if not line:
                if in_definition and entries:
                    entries[-1][1].append('', source, lineno)
                was_empty = True
                continue
            # unindented line -> a term
            if line and not line[0].isspace():
                # enable comments
                if line.startswith('.. '):
                    continue
                # first term of definition
                if in_definition:
                    if not was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary term must be preceded by empty line',
                            source=source, line=lineno))
                    entries.append(([(line, source, lineno)], ViewList()))
                    in_definition = False
                # second term and following
                else:
                    if was_empty:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary terms must not be separated by empty '
                            'lines', source=source, line=lineno))
                    if entries:
                        entries[-1][0].append((line, source, lineno))
                    else:
                        messages.append(self.state.reporter.system_message(
                            2, 'glossary seems to be misformatted, check '
                            'indentation', source=source, line=lineno))
            else:
                if not in_definition:
                    # first line of definition, determines indentation
                    in_definition = True
                    indent_len = len(line) - len(line.lstrip())
                if entries:
                    entries[-1][1].append(line[indent_len:], source, lineno)
                else:
                    messages.append(self.state.reporter.system_message(
                        2, 'glossary seems to be misformatted, check '
                        'indentation', source=source, line=lineno))
            was_empty = False

        # for (headers,body) in entries:
        #    for (term, source, line) in headers:
        #        print term
        #    for line in body:
        #        print '  ',line
        #    print '-'*50

        # TODO: save this to a file in env.doctreedir

        # now, parse all the entries into a big definition list
        items = []
        for terms, definition in entries:
            termtexts = []
            termnodes = []
            system_messages = []
            ids = []
            for line, source, lineno in terms:
                # parse the term with inline markup
                res = self.state.inline_text(line, lineno)
                system_messages.extend(res[1])

                # get a text-only representation of the term and register it
                # as a cross-reference target
                tmp = nodes.paragraph('', '', *res[0])
                tmp.source = source
                tmp.line = lineno
                new_id, termtext, new_termnodes = \
                    _make_termnodes_from_paragraph_node(env, tmp)
                ids.append(new_id)
                termtexts.append(termtext)
                termnodes.extend(new_termnodes)

            term = make_term_from_paragraph_node(termnodes, ids)
            term += system_messages

            defnode = nodes.definition()
            if definition:
                self.state.nested_parse(definition, definition.items[0][1],
                                        defnode)

            items.append((termtexts,
                          nodes.definition_list_item('', term, defnode)))

        if 'sorted' in self.options:
            items.sort(key=lambda x:
                       unicodedata.normalize('NFD', x[0][0].lower()))
        # for item in items:
        #    for x in item:
        #        print type(x),'---',x
        #    print '.'*50
        dlist = nodes.definition_list()
        dlist['classes'].append('glossary')        # %JFE= TODO:?
        dlist.extend(item[1] for item in items)
        node += dlist
        return messages + [node]





def setup(app):
    # wrong app.add_config_value('xglossary_unknowns',{},'html') # TODO: check if {} and 'html' are necessary
    app.add_directive('xglossary',XGlossary)
