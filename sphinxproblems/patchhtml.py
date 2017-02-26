"""
Code to patch readthedocs html files.
"""

import re
debug = True

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
                includeProblemLineInRTFDTheme(os.path.join(dir, file),level,problemLine)
