import missingxrefs


def setup(app):
    app.connect('builder-inited',missingxrefs.builder_inited_handler)
    app.connect('env-purge-doc', missingxrefs.purge_unknowns_entries_handler)
    app.connect('source-read',missingxrefs.source_read_handler)
    app.connect('missing-reference', missingxrefs.missing_reference_handler)
    app.connect('build-finished',missingxrefs.build_finished_handler)
    return {'version': '0.1'}