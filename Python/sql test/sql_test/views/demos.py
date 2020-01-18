"""Views for demo purposes."""
import pandas as pd
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config

from sql_test.models.models import Entity
from sql_test.models.models_cpt import Cpt
from pyramid_mod_dataframe import ColumnDT, QueryView, DataFrameView

from . import View


class Demos(View):
    """Contains all demo views.

    All web HTML/jade rendered web pages should be part of this class.
    """

    @view_config(route_name='bootstrap_demo',
                 permission=NO_PERMISSION_REQUIRED,
                 renderer='../templates/bootstrap_demo.jade')
    def bootstrap_demo(self):
        """View."""
        return {}

    @view_config(route_name='jade_demo',
                 permission=NO_PERMISSION_REQUIRED,
                 renderer='../templates/jade_demo.jade')
    def jade_demo(self):
        """View."""
        class FauxUser(object):
            name = 'abc'
            email = 'abc@def.com'
            city = 'NY'

        return {'user': FauxUser()}

    @view_config(route_name='entities',
                 permission='authenticated',
                 renderer='dataframe')  # noqa
    def entities(self):
        """Overview of all entities.
        As it is a lot of data and not a complicated query, the QueryView
        class is used.
        """
        name = 'Entities overview'
        request = self.request
        session = request.session

        columns = [
            ColumnDT(Entity.id),
            ColumnDT(Entity.name),
            ColumnDT(Entity._date),
            ColumnDT(Entity.longitude),
            ColumnDT(Entity.latitude),
            ColumnDT(Entity.entity_type)
        ]

        query = session.query()\
            .select_from(Entity)

        datatable_opts = """
        "columnDefs": [ {
          "render": function ( data, type, row ) {
      return '<a href="%s">NAME</a>'.replace('NAME',data).replace('NAME',data);
          },
          "targets": 1
          } ]
        """ % self.request.route_url('entity', name='NAME')

        return QueryView(request, query=query, datatable_opts=datatable_opts,
                         columns=columns, name=name, view=self)

    @view_config(route_name='cpts',
                 permission='authenticated',
                 renderer='dataframe')
    def cpts(self):
        """Overview of the CPTs.
        This is not a large ammount of data. Here the DataFrameView
        is applied.
        """
        query = self.request.session.query(
            Cpt.id.label('id'),
            Cpt.name.label('Name'),
            Cpt._date.label('Date'),
            Cpt.longitude.label('Longitude'),
            Cpt.latitude.label('Latitude'),
            Cpt.entity_type.label('Type')
        )

        df = pd.read_sql(query.statement, query.session.bind)

        datatable_opts = """
        "columnDefs": [ {
          "render": function ( data, type, row ) {
      return '<a href="%s">NAME</a>'.replace('NAME',data).replace('NAME',data);
          },
          "targets": 1
          } ]
        """ % self.request.route_url('entity', name='NAME')

        return DataFrameView(
            self.request, df, view=self,
            name='Overview of entities', datatable_opts=datatable_opts)

    @view_config(route_name='entity',
                 permission='authenticated',
                 renderer='../templates/entity.jade')
    def entity(self):
        """Detailed view of entity data.
        This view shows the main attributes of the entities.

        In this case, the whole entity is passed to the template.
        In the template, the interesting information is gotten from it.
        """
        self.page_title = 'Entity'

        self.js_requirements_specific = [
            {'name': 'Plot.ly',
             'priority': 200,
             'url': 'https://cdn.plot.ly/plotly-latest.min.js'},
             {'name': 'lodash',
             'priority': 250,
             'url': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.8.2/lodash.min.js'},  # noqa
             {'name': 'cpt_plot',
             'priority': 1200,
             'url': 'sql_test:static/js/plot.js'}]  # noqa

        name = self.request.matchdict['name']
        entity = self.request.session.query(Entity)\
            .filter(Entity.name == name).one()

        return{'entity': entity}


@view_config(route_name='cpt_plot',
             permission='authenticated',
             renderer='json')
def cpt_plot(request):
    """Show basic Plotly CPT-plot.

    Always return a dictionary for a Plotly plot:
        {'data': xxx,
         'layout': yyy}
    """
    name = request.matchdict['name']
    cpt = request.session.query(Cpt)\
        .filter(Cpt.name == name).one()

    # df = cpt.data_as_dataframe()
    df = pd.DataFrame.from_dict(cpt.data)
    df_dic = df.to_dict('records')
    depth = []
    friction = []
    resistance = []

    for val in df_dic:
        depth.append(-val['depth'])
        friction.append(val['fs'])
        resistance.append(val['qc'])

    friction_plot = {
        'x': friction, 'y': depth, 'mode': 'lines',
        'type': 'scatter',
        'name': 'Sleeve friction', 'hoverinfo': 'x+y',
        'line': {'color': '#a52a2a'}}

    resistance_plot = {
        'x': resistance, 'y': depth, 'mode': 'lines',
        'type': 'scatter',
        'name': 'Cone resistance', 'hoverinfo': 'x+y',
        'xaxis': 'x2', 'line': {'color': '#2aa52a'}}

    lines = [friction_plot, resistance_plot]
    layout = {
        'yaxis': {
            'title': 'Depth [m]'
        },
        'xaxis1': {
            'title': 'Sleeve friction [MPa]',
            'titlefont': {'color': '#a52a2a'},
            'tickfont': {'color': '#a52a2a'},
        },
        'xaxis2': {
            'overlaying': 'x',
            'side': 'top',
            'title': 'Cone resistance [MPa]',
            'titlefont': {'color': '#2aa52a'},
            'tickfont': {'color': '#2aa52a'},
        },
        'hovermode': 'y',
        'width':	500,
        'height':	800,

    }

    return {
        'data': lines,
        'layout': layout}
