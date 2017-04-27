# -*- coding: utf-8 -*-

import re

from docutils import nodes
from sphinx import addnodes

from sphinx.util.docfields import GroupedField
from sphinxcontrib_domaintools import custom_domain
#
# view = dict(
#     role='view',
#     objtype='view',
#     objname="SQL View",
#     indextemplate="pair: %s; SQL view",
#     parse=parse_signature_with_kind('view'),
#     fields=[
#         GroupedField('column',
#                      label="Columns",
#                      names=['column', 'col']),
#         GroupedField('constraint',
#                      label='Constraints',
#                      names=['constraint', 'con']),
#         GroupedField('example',
#                      label='Examples',
#                      names=['example', 'ex']),
#     ]
# ),

se_custom_domain = \
    custom_domain('SEDomain',
        name  = 'se',
        label = "SE",

        elements = dict(

            # ------------------------------------------------------
            #       Requirements models
            # ------------------------------------------------------

            requirement = dict(
                role = 'requirement',
                objtype = 'requirement',
                objname       = "Requirement",
                indextemplate = "pair: %s; Requirement",
            ),

            
            #------------------------------------------------------
            #       Use case models
            #------------------------------------------------------

            actor=dict(
                role='actor',
                objtype='actor',
                objname="actor",
                indextemplate="pair: %s; Actor",
                fields=[
                    GroupedField('super',
                                 label="Super actors",
                                 names=['superactor', 'SuperActor', 'super']),
                    GroupedField('instance',
                                 label="Instances",
                                 names=['instance', 'Instances'])
                ]
            ),

            iactor=dict(
                role='iactor',
                objtype='iactor',
                objname="iactor",
                indextemplate="pair: %s; Instanciated actor",
                fields=[
                    GroupedField('actor',
                                 label="Actor",
                                 names=['actor', 'Actor']),
                ]
            ),


            usecase=dict(
                role='usecase',
                objtype='usecase',
                objname="usecase",
                indextemplate="pair: %s; Usecase",
                fields=[
                    GroupedField('access',
                                 label="Accesses",
                                 names=['access', 'Access', 'a']),
                    GroupedField('actors',
                                 label='Actors',
                                 names=['actors']),
                    GroupedField('interface',
                                 label='Interface',
                                 names=['interface']),
                    GroupedField('scenario',
                                 label='Scenario',
                                 names=['scenario', 'scn']),
                ]
            ),

            iusecase=dict(
                role='iusecase',
                objtype='iusecase',
                objname="iusecase",
                indextemplate="pair: %s; Instanciated usecase",
            ),



            scenario=dict(
                role='scenario',
                objtype='scenario',
                objname="scenario",
                indextemplate="pair: %s; Scenario"
            ),


            # ------------------------------------------------------
            #       Class models
            # ------------------------------------------------------

            classe=dict(
                role='class',
                objtype='class',
                objname='class',
                indextemplate="pair: %s; Class",
                fields=[
                    GroupedField('superclass',
                                 label="Superclasses",
                                 names=['superclass', 'Superclass', 'super']),
                    GroupedField('attribute',
                                 label="Attributes",
                                 names=['attribute', 'Attribute', 'att']),
                    GroupedField('operation',
                                 label='Operations',
                                 names=['operation', 'Operation', 'op']),
                    GroupedField('invariant',
                                 label='Invariants',
                                 names=['invariant', 'Invariant', 'inv']),
                ]
            ),

            attribute=dict(
                role='attribute',
                objtype='attribute',
                objname='attribute',
                indextemplate="pair: %s; Attribute",
            ),

            association=dict(
                role='association',
                objtype='association',
                objname="association",
                indextemplate="pair: %s; Association",
                fields=[
                    GroupedField('from',
                                 label="From",
                                 names=['from','From']),
                    GroupedField('to',
                                 label="To",
                                 names=['to', 'To']),
                    GroupedField('role',
                                 label="role",
                                 names=['role', 'Role']),
                ]
            ),

            role=dict(
                role='role',
                objtype='role',
                objname='role',
                indextemplate="pair: %s; Role",
            ),

            associationclass=dict(
                role='associationclass',
                objtype='associationclass',
                objname="associationclass",
                indextemplate="pair: %s; AssociationClass",
            ),

            # ------------------------------------------------------
            #       Quality models
            # ------------------------------------------------------

            check=dict(
                role='check',
                objtype='check',
                objname="check",
                indextemplate="pair: %s; Check",
            ),

            # ------------------------------------------------------
            #       Suivi
            # ------------------------------------------------------

            question = dict(
                role = 'question',
                objtype = 'question',
                objname       = "Question",
                indextemplate = "pair: %s; Question",
            ),

            hypothesis = dict(
                role = 'hypothesis',
                objtype = 'hypothesis',
                objname       = "Hypothesis",
                indextemplate = "pair: %s; Hypothesis",
            ),

            remark = dict(
                role = 'remark',
                objtype = 'remark',
                objname       = "Remark",
                indextemplate = "pair: %s; Remark",
            ),

            decision = dict(
                role = 'decision',
                objtype = 'decision',
                objname       = "Decision",
                indextemplate = "pair: %s; Decision",
            ),

        )
    )





# #-----------------------------------------------------------------------
#
# class SQLTableSignatureNode(nodes.Part, nodes.Inline, nodes.TextElement):
#     """Node for a general parameter list."""
#     child_text_separator = ', '
#
# def argumentlist_visit(self, node):
#     self.visit_desc_parameterlist(node)
#
# def argumentlist_depart(self, node):
#     self.depart_desc_parameterlist(node)
#
# def html_argumentlist_visit(self, node):
#     self.visit_desc_parameterlist(node)
#     if len(node.children) > 3:
#         self.body.append('<span class="long-argument-list">')
#     else:
#         self.body.append('<span class="argument-list">')
#
# def html_argumentlist_depart(self, node):
#     self.body.append('</span>')
#     self.depart_desc_parameterlist(node)
#
#
# def app_add_node_addSQLTableSignatureNode(app):
#     app.add_node(
#         node = SQLTableSignatureNode,
#         html = (html_argumentlist_visit, html_argumentlist_depart),
#         latex = (argumentlist_visit, argumentlist_depart),
#     )
#
#
#
#
# #-----------------------------------------------------------------------
#
# class SQLTableColumnNode(nodes.Part, nodes.Inline, nodes.TextElement):
#     """Node for an argument wrapper"""
#
# def argument_visit(self, node):
#     pass
#
# def argument_depart(self, node):
#     pass
#
# def html_argument_visit(self, node):
#     self.body.append('<span class="arg">')
#
# def html_argument_depart(self, node):
#     self.body.append("</span>")
#
# def app_add_node_addSQLTableColumnNode(app):
#     app.add_node(
#         node = SQLTableColumnNode,
#         html = (html_argument_visit, html_argument_depart),
#         latex = (argument_visit, argument_depart),
#     )
#
#
#
# sql_table_signature_re = re.compile(r'(\w+)\s*\(([^)]*)\)')
#
# sql_column_re = re.compile(
#         r'(?P<key>#)?\s*(?P<name>\w+)\s*(:\s*(?P<type>\w+))?\s*(?P<optional>\?)?\s*(?P<reference>>+)?\s*')
#
#
#
#
#
# def _get_column_node(m):
#     if m.group('name'):
#         node = addnodes.desc_parameter()
#
#         if m.group('key'):
#             node += nodes.Text("#", "#")
#
#         key = nodes.strong(m.group('name'), m.group('name'))
#         key['classes'].append('arg-key')
#         node += key
#
#         if m.group('type'):
#             node += nodes.Text(" : ", " : ")
#             value = nodes.inline(m.group('type'), m.group('type'))
#             value['classes'].append('arg-value')  # FIXME: should vbe arg type probably
#             node += value
#
#         if m.group('optional'):
#             node += nodes.Text("? ", "?")  # FIXME: find a better type
#
#         if m.group('reference'):
#             value = nodes.inline(m.group('reference'), m.group('reference'))
#             value['classes'].append('arg-value')  # FIXME: should vbe arg type probably
#             node += value
#
#         return node
#
#     else:
#         return addnodes.desc_parameter(m.group(0), m.group(0))
#
#
#
# def parse_signature_with_kind(kind):
#
#     def parse_signature(env, sig, signode):
#         m = sql_table_signature_re.match(sig)
#         if not m:
#             signode += addnodes.desc_name(sig, sig)
#             return sig
#         name, args = m.groups()
#         # TODO: This should be improved with a more appropriate node.
#         # Look for instance at the code generated by ..  py:class:: babar
#         signode += addnodes.desc_type(kind+' ',kind+' ')
#
#         # Add the name of the class
#         signode += addnodes.desc_name(name, name)
#         plist = SQLTableSignatureNode()
#         for m in sql_column_re.finditer(args):
#             x = SQLTableColumnNode()
#             x += _get_column_node(m)
#             plist += x
#
#         signode += plist
#         return name
#
#     return parse_signature


#-----------------------------------------------------------------------------

