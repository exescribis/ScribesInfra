import sphinxgithub.dir


def build_finished_handler(app, exception):
    if app.builder.format == 'html':
        dir.addNoJekyll(app)

def setup(app):
    app.connect('build-finished',build_finished_handler)
    return {'version': '0.1'}