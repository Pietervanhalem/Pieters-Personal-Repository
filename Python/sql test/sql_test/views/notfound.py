"""The not found page view."""

from pyramid.view import notfound_view_config


@notfound_view_config(renderer='../templates/404.jade')
def notfound_view(request):
    """Show when the requested page could not be found."""
    request.response.status = 404
    return {}
