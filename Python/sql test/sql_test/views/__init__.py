"""All html pages should subclass View."""

from pyramid.decorator import reify

from pyramid_mod_huisstijl import BaseView


@reify
def menu(self):
    """Return menu dict.

    Menu can be made dynamic, e.g. depending on user view permissions
    """
    menu = list()
    
    
    menu.extend([
        {
            'title': 'Bootstrap Demo',
            'href': self.request.route_url('bootstrap_demo'),
            'icon': "fa fa-twitter-square"
        },
        {
            'title': 'Jade Demo',
            'href': self.request.route_url('jade_demo'),
            'icon': "fa fa-indent"
        },
    ])
    if self.user:
        menu.extend([
            {
                'title': 'Entities',
                'icon': "fa fa-bar-chart",
                'dropdown': [
                    {
                        'title': 'All entities',
                        'href': self.request.route_url(
                            'entities',
                            ext='html',
                            _query={
                                'renderer': 'datatable',
                                'options': 'serverside-columnsearch'
                            }
                        ),
                        'icon': "fa fa-bar-chart"},
                    {
                        'title': 'CPTs',
                        'href': self.request.route_url(
                            'cpts',
                            ext='html',
                            _query={
                                'renderer': 'datatable',
                                'options': 'columnsearch'
                            }
                        ),
                    }
                ]
            }
        ]),
        if self.user.has_admin:
            menu.append(
                {
                    'title': "User Management",
                    'icon': "fa fa-users",
                    'dropdown': [
                        {
                            'title': 'User Overview',
                            'href': self.request.route_url(
                                'users',
                                ext='html',
                                _query={
                                    'renderer': 'datatable',
                                    'options': 'serverside-columnsearch'
                                }
                            ),
                            'icon': 'fa fa-users',
                        },
                        {
                            'title': 'Add User',
                            'href': self.request.route_url('user_create'),
                            'icon': 'fa fa-user-plus',
                        }
                    ]
                }
            )

    return menu


BaseView.project_name = 'sql test'
BaseView.include_security = True
BaseView.menu = menu


class View(BaseView):
    """All html pages should subclass View."""

    pass
