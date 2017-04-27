"""
sphinxproblems command line.

usage:

    python sphinxproblems <source_directory> <target_directory> [ clean ]

"""

import sys
import os
THIS_DIR = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    sys.path.append(os.path.join(THIS_DIR,'..'))

    import engine
    import filehelpers
    source_directory = sys.argv[1]
    target_directory = sys.argv[2]
    clean = len(sys.argv)==4 and sys.argv[3]=='clean'
    e = engine.SphinxProblemsEngine(source_directory, target_directory, clean=clean)
    sys.exit(e.build())

#     $(SPHINXBUILD) -q -b html $(ALLSPHINXOPTS) $(BUILDDIR) -w $(SHINXERRORSOUT) 2>/dev/null
# python $(SCRIBESINFRA)/sphinxproblems problemsToRST $(GROUPDIR) $(BUILDDIR)
#     $(SPHINXBUILD) -Q -t sphinx-problems-rerun -b html $(ALLSPHINXOPTS) $(BUILDDIR)
# python $(SCRIBESINFRA)/sphinxproblems patchHTMLFiles $(GROUPDIR) $(BUILDDIR)
# echo "\nOpen $(BUILDDIR)/index.html in a browser to see the documentation"


