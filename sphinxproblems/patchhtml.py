import re
debug = False

def includeProblemLineInRTFDTheme(file, levelFromHtmlRoot, problemLine):
    # the path to the defaults must be computed depending on the patched filae
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
    changed = new_content != content
    if changed:
        with open(file, 'w') as f:
            f.write(new_content)
        if debug:
            print 'file %s changed' % file
    return changed

import os

def processFiles(rootDirectory, problemLine):
    """

    :param htmlRootDirectory:
    :return:
    """
    for (dir, subdirs, files) in os.walk(rootDirectory):
        relpath = os.path.relpath(dir,rootDirectory)
        reldir = '.' if relpath=='.' else './%s' % relpath
        level = len(reldir.split('/'))-1
        for file in files:
            if file.endswith('.html'):
                includeProblemLineInRTFDTheme(os.path.join(dir, file),level,problemLine)
