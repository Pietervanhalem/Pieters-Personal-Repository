"""Route configuration."""


def includeme(config):
    """Include in the config if this module is loaded."""
    config.add_static_view("static_deform", "deform:static")
    config.add_static_view(name='static', path='sql_test:static', cache_max_age=3600)
    config.add_route("home", "/")
    
    config.add_route('jade_demo', '/jade_demo')
    config.add_route('bootstrap_demo', '/bootstrap_demo')
    config.add_route('entities', '/entities.{ext}')
    config.add_route('cpts', '/cpts.{ext}')
    config.add_route('entity', '/entity/{name}')
    config.add_route('cpt_plot', 'cpt_plot/{name}')
    