sphinxrelinks
=============


Installation
------------

Add the extension in your configuration file (if not already done). ``conf.py`` should look like::

    extensions = [
        ...                # some extensions
        'sphinxrelinks',
        ...                # other extensions
        something else
    ]



Usage
-----

This extension is directly derived from `sphinx.ext.extlinks`_ standard
sphinx extension. Changed (a bit) by Jean-Marie Favre in order to support
multiple arguments like::

    :gh_issue:`m2cci/m2cci-pi-GPI01/23`

..  _`sphinx.ext.extlinks`:
        http://www.sphinx-doc.org/en/stable/ext/extlinks.html


This extension should be improved for refspec parsing (e.g. use a regexp).

Currently / is used as a separator so roles should looks like::

    :gh_issue:`m2cci/m2cci-pi-GPI01/23`

See ``test/sphinxrelinks/conf.py`` for interesting examples of url definitions.
The definitions are provided for:

* github links
* scribesquality links

this should be externalized somehow.
