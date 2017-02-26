DOCDIR          = .
INFRADIR        = .infra
BUILDDIR        = $(DOCDIR)/.build/docs
SPHINXOPTS      = -c $(INFRADIR)/docs
SPHINXERRORSOUT = $(BUILDDIR)/sphinx-problems.txt
SPHINXBUILD     = sphinx-build
SCRIBESINFRA    = ../../../../ScribesInfra

# SPHINXOPTS    = -c . -q -w buildErrors.txt
# SPHINXBUILD   = /usr/share/PyVEnvs27/ScribesEnv/bin/sphinx-build
PAPER         =
#BUILDDIR      = .build

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) $(DOCDIR)

clean:
	rm -rf $(BUILDDIR)/*
	mkdir -p $(BUILDDIR)

html:
	mkdir -p $(BUILDDIR)
	@echo $(SCRIBESINFRA)
	$(SPHINXBUILD) -q -b html $(ALLSPHINXOPTS) $(BUILDDIR) -w $(SPHINXERRORSOUT)
	python $(SCRIBESINFRA)/sphinxproblems problemsToRST $(DOCDIR) $(BUILDDIR)
	$(SPHINXBUILD) -Q -t sphinx-problems-rerun -b html $(ALLSPHINXOPTS) $(BUILDDIR)
	python $(SCRIBESINFRA)/sphinxproblems patchHTMLFiles $(DOCDIR) $(BUILDDIR)
	echo "\nOpen $(BUILDDIR)/index.html in a browser to see the documentation"

pseudoxml:
	$(SPHINXBUILD) -b pseudoxml $(ALLSPHINXOPTS) $(BUILDDIR)/pseudoxml
	@echo
	@echo "Build finished. The pseudo-XML files are in $(BUILDDIR)/pseudoxml."

viewdoc:    html
	firefox $(BUILDDIR)/index.html &


