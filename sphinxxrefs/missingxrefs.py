import re
import os
import codecs

from sphinx import addnodes
from collections import Counter

import filehelpers

debug=False

XXX='XXX'
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
RES_DIR = os.path.join(THIS_DIR,'res')
TEMPLATE_DIR = 'sphinxxrefstemplates'

def isIdentifier(text):
    return re.match('^[A-Za-z_]\w+$', text) is not None



def _getDefinitionTemplate(app, domain, type):
    """
    Try to get the template for the given domain and type from a file with
    the pattern:  xreftemplates/def-{domain}-{type}.rst where xreftemplates
    is at the same level of conf.py (in the confdirectory)
    For instance xreftemplates/def-sql-table.rst

    The env.xglossary_templates dict serve as as a cache. It can be intialized in
    conf.py with a given content.
    Something like
        xreftemplates = {
            ('se','requirement') :
               "{header}\n"
               ".. requirement:: {label}\n"
            }

    Return none if no such template exist.
    :return: str | None
    """

    def find_template_file(domain, type):
        filename = os.path.join(TEMPLATE_DIR,'def-%s-%s.rst' % (domain,type))
        user_filename = os.path.join(app.confdir,filename)
        if os.path.isfile(user_filename):
            return user_filename
        sys_filename = os.path.join(RES_DIR, filename)
        if os.path.isfile(sys_filename):
            return sys_filename
        else:
            return None


    env = app.env
    if not hasattr(env, 'sphinxxrefs_templates'):
        env.sphinxxrefs_templates = {}

    # search if the file has been read/defined or read it otherwise
    if (domain,type) in env.sphinxxrefs_templates:
        # already here, just return the content
        return env.sphinxxrefs_templates[(domain,type)]
    else:
        # search first in user confir

        filepath = find_template_file(domain, type)
        if filepath is not None:
            # read and register the file for further use
            with codecs.open(filepath, 'r', 'utf-8') as f:
                content = f.read()
            env.sphinxxrefs_templates[(domain,type)]=content
            return content
        else:
            return None




class MissingXRefTable(object):

    def __init__(self):
        #: dict[(str,str,str),MissingXRef]
        self.missingXRefsMap = {}
        # self.missingXRefsByDomainTypeDocname = {}

    def add(self, domain, type, label, docname):
        key = (domain, type, label)

        # add in missingXRefsMap
        if key in self.missingXRefsMap.keys():
            self.missingXRefsMap[key].addOccurrence(docname)
        else:
            xref = MissingXRef(domain, type, label, docname)
            self.missingXRefsMap[key] = xref

    def nbOfReferences(self):
        return len(self.missingXRefsMap)

    def nbOfOccurrences(self):
        return sum(map (lambda xref:xref.nbOccurrences(), self.missingXRefsMap.values()))

    def __unicode__(self):
        return '\n'.join(
            unicode(xref) for xref in self.missingXRefsMap.values()
        )

    def unknownReferencesSummary(self, app):
        pass # TODO
        # for (domain, type, label) in self.missingXRefsMap:

    def unknownReferencesRSTPage(self, app):
        title = '%d unknown references' % self.nbOfReferences()
        summary = (
            '%s unknowns references with %s occurrences' % (
                self.nbOfReferences(),
                self.nbOfOccurrences())
        )
        _ = [
            title,
            '-'*len(title),
            '',
            summary,
            '::',
            '',
            '    .. you can copy and paste the following skeltons in the appropriate place']

        for xref in self.missingXRefsMap.values():
            _ += map(lambda line:'    '+line, xref.getDefinitionStub(app).split('\n'))

        return '\n'.join(_)

class MissingXRef(object):

    def __init__(self, domain, type, label, docname=None, nbocc=1):
        self.domain = domain
        self.type = type
        self.label = label
        self.isIdentifier = isIdentifier(self.label)
        self.docCounter = Counter()
        if docname is not None:
            self.docCounter[docname] = nbocc

    def id(self, fakeChar="`"):
        return (
            self.domain
            + (':%s:' % self.type if self.type else '')
            + '%s%s%s' % (fakeChar,fakeChar,self.label)
        )

    def nbOccurrences(self):
        return sum(self.docCounter.values())

    def nbDocuments(self):
        return len(self.docCounter.keys())

    def addOccurrence(self, docname, nbocc=1):
        self.docCounter[docname] += nbocc

    def usage(self):
        details = ','.join(
                ('%s.rst(%s)'%(docname,count)) if count>1 else docname+'.rst'
                for (docname,count) in self.docCounter.iteritems())
        nb_occs = self.nbOccurrences()
        nb_docs = self.nbDocuments()
        if nb_occs > 1 and nb_docs > 1:
            return '%i occurrences in %i files: %s' % (nb_occs, nb_docs, details)
        else:
            return '1 occurrence in %s' % details

    def getDefinitionStub(self, app):
        template = _getDefinitionTemplate(app, self.domain, self.type)
        # header = '.. '+(' '+self.id()).rjust(80,'.')
        if self.isIdentifier:
            if template is None:
                return '.. TODO:: xref missing:  \n'
            else:
                return template.format(
                        domain=self.domain, type=self.type, label=self.label,
                        nbocc=self.nbOccurrences(), usage='')
        else:
            return ''


    def __unicode__(self):
        return self.domain+':'+self.type+':'+self.label+' '+self.usage()

def missxrefs_file(app):
    file =  os.path.join(app.srcdir,'.infra','docs','problems','missing-xrefs.rst')
    return file



#-----------------------------------------------------------------------------------------
#    Handlers
#-----------------------------------------------------------------------------------------

NO_REFERENCE_PROBLEM = '\n'.join(
    [ 'Unknown references',
      '==================',
      '',
      'All references are defined.'
])


def builder_inited_handler(app):
    if not app.tags.has('sphinx-problems-rerun'):
        file = missxrefs_file(app)
        dir = os.path.dirname(file)
        filehelpers.ensureDirectory(dir)
        with open(file,'w') as f:
            f.write(NO_REFERENCE_PROBLEM)

def source_read_handler(app, docname, sourceSingleton):
    sourceSingleton[0] = re.sub('`?XXX`?','`XXX`', sourceSingleton[0])

def missing_reference_handler(app, env, pendingXRefNode, contnode):
    """
    Collect missing xref and return a node with "undefined" class that can
    be used for styling.
    Xrefs are collected in env.sphinxxrefs_unknowns list with a record
    'refdoc','refdomain','reftype', 'reftarget', 'refexplicit', 'refwarn'.

    """

    #--------------------- add entry to sphinxxrefs_unknowns list
    if not hasattr(env, 'sphinxxrefs_unknowns'):
        env.sphinxxrefs_unknowns = []
    attributes = ('refdoc','refdomain','reftype', 'reftarget', 'refexplicit', 'refwarn')
    unknown_entry = { k : pendingXRefNode[k] for k in attributes }
    env.sphinxxrefs_unknowns.append(unknown_entry)
    env.warn(
            pendingXRefNode['refdoc'],
            'reference not found: %s' % pendingXRefNode['reftarget'],
             lineno=None)

    if debug:
        print 'missing entry',unknown_entry


    #--------------------- change the node with a node with "undefined" calss
    newnode = addnodes.literal_strong()
    newnode['classes'] = contnode['classes']+['undefined']
    content=contnode.children[0]
    newnode.append(content)
    return newnode


def purge_unknowns_entries_handler(app, env, docname):
    """
    Purge the sphinxxrefs_unknowns list for a docname. Remove all records
    for this document.
    """
    # see http://www.sphinx-doc.org/en/stable/extdev/tutorial.html#the-event-handlers
    if not hasattr(env, 'sphinxxrefs_unknowns'):
        return
    print 'purge_unknowns_entries for %s'
    env.sphinxxrefs_unknowns = [
        entry for entry in env.sphinxxrefs_unknowns
        if entry['refdoc'] != docname ]



def build_finished_handler(app, exception):
    """
    Transform the collected list of missing references into MissingXRefTable and save it.
    """
    env = app.env
    if not hasattr(env, 'sphinxxrefs_unknowns'):
        return
    else:
        missing_xrefs = MissingXRefTable()

        for unknown in env.sphinxxrefs_unknowns:
            docname = unknown['refdoc']
            label = unknown['reftarget']
            domain = unknown['refdomain'] if unknown['refdomain'] not in ['','std'] else ''
            type = unknown['reftype'] if unknown['reftype']  not in ['','std','any'] else ''
            missing_xrefs.add(domain, type, label,docname)

        missing_output_file = missxrefs_file(app)
        # print "WRITE ",missing_output_file
        with codecs.open(missing_output_file, "w", "utf-8") as f:
            f.write(missing_xrefs.unknownReferencesRSTPage(app))

