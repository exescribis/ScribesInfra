SPHINXOPTS    = -c . -q -w buildErrors.txt
# SPHINXBUILD   = /usr/share/PyVEnvs27/ScribesEnv/bin/sphinx-build
SPHINXBUILD   = sphinx-build

PAPER         =
BUILDDIR      = .build

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .
# the i18n builder cannot share the environment and doctrees with the others
I18NSPHINXOPTS  = $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

clean:
	rm -rf $(BUILDDIR)/*
	mkdir -p $(BUILDDIR)

html:
	mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR) -w $(BUILDDIR)/build-errors.txt
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

pseudoxml:
	$(SPHINXBUILD) -b pseudoxml $(ALLSPHINXOPTS) $(BUILDDIR)/pseudoxml
	@echo
	@echo "Build finished. The pseudo-XML files are in $(BUILDDIR)/pseudoxml."

viewdoc:    html
	firefox .build/index.html &