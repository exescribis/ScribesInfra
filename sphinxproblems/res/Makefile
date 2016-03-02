GROUPDIR        = .
INFRADIR        = .infra
BUILDDIR        = $(GROUPDIR)/.build/docs
SPHINXOPTS      = -c $(INFRADIR)/docs
SHINXERRORSOUT  = $(BUILDDIR)/sphinx-problems.txt
SPHINXBUILD     = sphinx-build
SCRIBESINFRA     = ../ScribesInfra


ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) $(GROUPDIR)

clean:
	rm -rf $(BUILDDIR)/*
	mkdir -p $(BUILDDIR)

html:
	mkdir -p $(BUILDDIR)
	$(SPHINXBUILD) -q -b html $(ALLSPHINXOPTS) $(BUILDDIR) -w $(SHINXERRORSOUT) 2>/dev/null
	python $(SCRIBESINFRA)/sphinxproblems problemsToRST $(GROUPDIR) $(BUILDDIR)
	$(SPHINXBUILD) -Q -t sphinx-problems-rerun -b html $(ALLSPHINXOPTS) $(BUILDDIR)
	python $(SCRIBESINFRA)/sphinxproblems patchHTMLFiles $(GROUPDIR) $(BUILDDIR)
	echo "\nOpen $(BUILDDIR)/index.html in a browser to see the documentation"





