import os

import docutils.nodes
import sphinxproblems.parser
import sphinxproblems.problems

def on_doctree_read(app, doctree):
    print('#'*30+' doctree-read '+'#'*10
          +' '+os.path.basename(doctree['source'])
          +' '+'#'*30)
  #  print doctree.pformat()
    # print '.'*80
    for n in doctree.traverse(docutils.nodes.system_message):#docutils.nodes.title):
        # MANAGER.addProblem(Problem(type=n['type'], line=n['line'], source=n['source'], message=n[0][0]))
        print('PROBLEM FOUND')
        #print type(n)
        #print '---'

def on_doctree_resolved(app, doctree,docname):
    if 'source' in doctree:
        s = os.path.basename(doctree['source'])
    else:
        s = 'no source'
    print('#'*30+' doctree-resolved '+'#'*10
          +' '+s+' '+'#'*30)
 #   print doctree.pformat()
    # print app.env.warnings
    print('.'*80)

def on_env_updated(app, env):
    print('#'*30+' env-updated '+'#'*80)
    FILE = '/D2/m2cci/m2cci-pi-groups/m2cci-pi-GPI01/.build/docs/build-errors.txt'
    with open(FILE,'r') as f:
        content = f.read()
    print(content)
    print('.'*80)

def on_missing_reference(app, env, node, contnode):
    print('#'*30+' missing-reference '+'#'*80)
    print(node.pformat())
    print('.'*80)



def on_build_finished(app, exception):
    print('#'*500)
    print('Build finished')
    # problems = sphinxerrorparser.parseErrorFile('.build/docs/sphinx-errors.txt', PROBLEM_MANAGER)
    # print PROBLEM_MANAGER.summary()


def setup(app):
    app.connect('doctree-read',on_doctree_read)
   # app.connect('env-updated',on_env_updated)   #???
   # app.connect('doctree-resolved',on_doctree_resolved)
   # app.connect('missing-reference',on_missing_reference)
    app.connect('build-finished',on_build_finished)
    return {'version': '0.1'}
