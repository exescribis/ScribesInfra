"""
Code to patch readthedocs html files.
"""

import re
debug = False




DUPLICATED_SCRIPTS=[
    """<script type="text/javascript" src="[./]*_static/translations.js"></script>""",
    """<script type="text/javascript" src="[./]*_static/sphinxcontrib-images/LightBox2/lightbox2/js/jquery-1.11.0.min.js"></script>""",
    """<script type="text/javascript" src="[./]*_static/sphinxcontrib-images/LightBox2/lightbox2/js/lightbox.min.js"></script>""",
    """<script type="text/javascript" src="[./]*_static/sphinxcontrib-images/LightBox2/lightbox2-customize/jquery-noconflict.js"></script>"""
]

def removeDuplicatedScripts(file):
    # FIXME: The scripts below are duplicated for unknown reasons in phase #3. To be investigated
    # This is not the case when using a makefile with explicit call to sphinx-build
    # It might be due to the fact that the sphinx API is called directly ? parameters ? state ?
    # The solution below 'DUPLICATED_SCRIPTS" and 'removeDuplicatedScripts' is a really ugly workaround
    with open(file, 'r') as f:
        content = f.read()
    new_content = content
    for script in DUPLICATED_SCRIPTS:
        total_count = len(re.findall(script, new_content, flags=re.MULTILINE))
        new_content = re.sub(script, '', new_content, flags=re.MULTILINE, count=total_count-1)
    changed = new_content != content
    if changed:
        with open(file, 'w') as f:
            f.write(new_content)
        if debug:
            print('removed duplicated scripts in file %s' % file)
    return changed

# Here is the makefile that makes it work
# GROUPDIR        = .
# INFRADIR        = .infra
# BUILDDIR        = $(GROUPDIR)/.build/docs
# # BUILDDIR        = ../m2cci.github.io/m2cci-pi/root
# SPHINXOPTS      = -c $(INFRADIR)/docs
# # SHINXERRORSOUT  = $(BUILDDIR)/sphinx-problems.txt
# # SPHINXBUILD     = sphinx-build
# SCRIBESINFRA    = ../ScribesInfra
#
#
# ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(SPHINXOPTS) $(GROUPDIR)
#
# clean:
# 	rm -rf $(BUILDDIR)/* $(BUILDDIR)/.[!.]*
# 	mkdir -p $(BUILDDIR)
#
# html:
# 	mkdir -p $(BUILDDIR)
# 	$(SPHINXBUILD) -q -b html $(ALLSPHINXOPTS) $(BUILDDIR) -w $(SHINXERRORSOUT) # 2>/dev/null
#   python $(SCRIBESINFRA)/sphinxproblems problemsToRST $(GROUPDIR) $(BUILDDIR)
#   $(SPHINXBUILD) -Q -t sphinx-problems-rerun -b html $(ALLSPHINXOPTS) $(BUILDDIR)
#   python $(SCRIBESINFRA)/sphinxproblems patchHTMLFiles $(GROUPDIR) $(BUILDDIR)
#   echo "\nOpen $(BUILDDIR)/index.html in a browser to see the documentation"

def includeProblemLineInRTFDTheme(file, levelFromHtmlRoot, problemLine):
    """
    Patch a readthedocs html files to include the problem summary on
    the top of the banner. The method is quite ugly, but in the meantime
    it works. Should find something better.
    :param file: The html file to patch.
    :param levelFromHtmlRoot:
    :param problemLine:
    :return:
    """
    # the path to the defaults must be computed depending on the patched file
    origin = """<div class="wy-side-nav-search">(.*><!--__problems__-->)?"""
    replacement_pattern = """
        <div class="wy-side-nav-search">
            <div style="margin-bottom: 2em;
                        background: yellow;
                        color:black;
                        font-size:larger;
                        font-weight:bold;
                        padding:20px;">
                <a href="{problemIndexPath}">
                {problemLine}
                </a>
            </div><!--__problems__-->
        """
    with open(file, 'r') as f:
        content = f.read()
    replacement = replacement_pattern.format(
        problemLine=problemLine,
        problemIndexPath='../'*levelFromHtmlRoot+'.infra/docs/problems/index.html'
    )
    new_content = re.sub(origin, replacement, content, flags=re.MULTILINE | re.DOTALL)
    # if debug:
    #     print('origin:',origin)
    #     print('replacement:', replacement)
    changed = new_content != content
    if changed:
        with open(file, 'w') as f:
            f.write(new_content)
        # if debug:
        #     print('file %s changed' % file)
    return changed

import os

def processFiles(rootDirectory, problemLine):
    """
    Patch all html files under the given directory.
    :param htmlRootDirectory: The directory containing html files.
    :param problemLine: the summary to include in the bar.
    :return: None
    """
    for (dir, subdirs, files) in os.walk(rootDirectory):
        relpath = os.path.relpath(dir,rootDirectory)
        reldir = '.' if relpath=='.' else './%s' % relpath
        level = len(reldir.split('/'))-1
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(dir, file)
                removeDuplicatedScripts(file_path)
                includeProblemLineInRTFDTheme(file_path,level,problemLine)
