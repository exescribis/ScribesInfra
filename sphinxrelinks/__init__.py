# -*- coding: utf-8 -*-
"""
    sphinxrelinks
    =============

    This extension is directly derived from `sphinx.ext.extlinks`_ standard
    sphinx extension. Changed (a bit) by Jean-Marie Favre in order to support
    multiple arguments like :gh_issue:`m2cci/m2cci-pi-GPI01/23`

    current state
    -------------
        work with the couple examples in test
        should be improved for refspec parsing (e.g. use a regexp)
        currently / is used as a separator so roles should looks like
          :gh_issue:`m2cci/m2cci-pi-GPI01/23`
        see sandbox/conf.py for examples of url definitions.

        interesting patterns are in test/conf.py  for github and scribesquality
        this should be externalized somehow.

    original documentation
    ----------------------

    Extension to save typing and prevent hard-coding of base URLs in the reST
    files.

    This adds a new config value called ``extlinks`` that is created like this::

       extlinks = {'exmpl': ('http://example.com/%s.html', prefix), ...}

    Now you can use e.g. :exmpl:`foo` in your documents.  This will create a
    link to ``http://example.com/foo.html``.  The link caption depends on the
    *prefix* value given:

    - If it is ``None``, the caption will be the full URL.
    - If it is a string (empty or not), the caption will be the prefix prepended
      to the role content.

    You can also give an explicit caption, e.g. :exmpl:`Foo <foo>`.

    :copyright: Copyright 2007-2016 by the Sphinx team, see AUTHORS.
    :license: BSD, see LICENSE for details.

    ..  _`sphinx.ext.extlinks`:
        http://www.sphinx-doc.org/en/stable/ext/extlinks.html



"""

from six import iteritems
from docutils import nodes, utils

import sphinx
from sphinx.util.nodes import split_explicit_title


def get_url(url_pattern, refspec, separator='/'):
    """
    Generate a url from the url_pattern and the ref specification
    :param url_pattern: the pattern. Something like http://github.com/{0}/{1}
    :param refspec: the reference specification given in the role (e.g.  :gh_repo:`m2cci/m2cci_gi_hq`)
    :return: the final url
    """
    refparts = refspec.split(separator)
    full_url = url_pattern.format(*refparts)
    return full_url

def get_display(display_pattern, refspec, separator='/'):
    """
    Generate a display string from the url_pattern and the ref specification
    :param url_pattern: the pattern. Something like http://github.com/{0}/{1}
    :param refspec: the reference specification given in the role (e.g.  :gh_repo:`m2cci/m2cci_gi_hq`)
    :return: the final url
    """
    refparts = refspec.split(separator)
    return display_pattern.format(*refparts)

def make_link_role(url_pattern, display_pattern):
    def role(typ, rawtext, text, lineno, inliner, options={}, content=[]):
        text = utils.unescape(text)

        has_explicit_title, title, refspec = split_explicit_title(text)

        # TODO: this code with exception handling should go get_url
        #       the warning should style be generated with typ and lineno parameters,
        try:
            full_url = get_url(url_pattern, refspec)
        except (TypeError, ValueError):
            # TODO: check which exception can be raised by get_url and add them here
            inliner.reporter.warning(
                'unable to expand %s extlink with base URL %r, please make '
                'sure the base contains \'%%s\' exactly once'
                % (typ, url_pattern), line=lineno)
            full_url = url_pattern + refspec

        if not has_explicit_title:
            if display_pattern is None:
                title = full_url
            else:
                title = get_display(display_pattern, refspec)
        pnode = nodes.reference(title, title, internal=False, refuri=full_url)
        return [pnode], []
    return role


def setup_link_roles(app):
    for name, (url_pattern, display_pattern) in iteritems(app.config.sphinxrelinks):
        app.add_role(name, make_link_role(url_pattern, display_pattern))


def setup(app):
    app.add_config_value('sphinxrelinks', {}, 'env')
    app.connect('builder-inited', setup_link_roles)
    return {'version': '0.1', 'parallel_read_safe': True}
