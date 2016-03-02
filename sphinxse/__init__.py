

import sphinxse.sedomain
import sphinxse.xglossary

def setup(app):

    app.add_domain(sphinxse.sedomain.se_custom_domain)

    # wrong app.add_config_value('xglossary_unknowns',{},'html') # TODO: check if {} and 'html' are necessary
    app.add_directive('xglossary',sphinxse.xglossary.XGlossary)
    return {'version': '0.1'}
