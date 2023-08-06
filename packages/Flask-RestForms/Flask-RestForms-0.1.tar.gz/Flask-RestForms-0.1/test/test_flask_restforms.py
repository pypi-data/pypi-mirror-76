from unittest.mock import MagicMock

import pytest
from jinja2 import Environment

from flask_restforms.main import FlaskRestForms, RestFormsJinja, RestFormsMiddleware


class AppMock(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.wsgi_app = MagicMock()
        self.jinja_options = {'extensions': []}
        self.jinja_env = MagicMock()


@pytest.mark.parametrize('request_method, field_value, expected_method', (
    ('POST', 'DELETE', 'DELETE'),
    ('POST', None, 'POST'),
    ('GET', '', 'GET'),
    ('POST', 'OTHER', 'OTHER'),
))
def test_middleware_updates_request_method(request_method, field_value, expected_method):
    method_field = 'method-field'
    app = AppMock()
    start_response = MagicMock()
    request = MagicMock()
    request.form = {method_field: field_value}
    environ = {
        'werkzeug.request': request,
        'REQUEST_METHOD': request_method,
    }
    middleware = RestFormsMiddleware(app.wsgi_app, method_field)

    response = middleware(environ, start_response)

    app.wsgi_app.assert_called_once_with(environ, start_response)
    assert response == app.wsgi_app.return_value
    assert environ['REQUEST_METHOD'] == expected_method


def test_flask_restforms_set_up():
    app = AppMock()

    FlaskRestForms(app)

    app.jinja_env.extend.assert_called_once_with(
        flask_restforms_field=app.config['REST_FORMS_METHOD_FIELD']
    )
    assert RestFormsJinja in app.jinja_options['extensions']
    assert isinstance(app.wsgi_app, RestFormsMiddleware)


def test_jinja_appends_hidden_input_to_forms():
    env = Environment()
    env.add_extension(RestFormsJinja)
    env.extend(flask_restforms_field='method_input')

    t = env.from_string('''
        <h1>Title</h1>
        <!-- <form>
            <button type="submit">Go</button>
        </form> -->
        <form action="/other/url/or/so">
            <button type="submit">Go</button>
        </form>
        <form method="GET">
            <button type="submit">Go</button>
        </form>
        <form method="DELETE">
            <button type="submit">Delete</button>
        </form>
        <form method="PATCH">
            <button type="submit">Edit</button>
        </form>
    ''')

    assert t.render() == '''
        <h1>Title</h1>
        <!-- <form>
            <button type="submit">Go</button>
        </form> -->
        <form action="/other/url/or/so">
            <button type="submit">Go</button>
        </form>
        <form method="GET">
            <button type="submit">Go</button>
        </form>
        <form method="POST"><input type="hidden" name="method_input" value="DELETE" />
            <button type="submit">Delete</button>
        </form>
        <form method="POST"><input type="hidden" name="method_input" value="PATCH" />
            <button type="submit">Edit</button>
        </form>
    '''
