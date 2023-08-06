import re

from jinja2.ext import Extension
from jinja2.lexer import count_newlines
from jinja2.lexer import Token


class FlaskRestForms:
    DEFAULT_METHOD_FIELD = '__flask-restforms-method'

    def __init__(self, app):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('REST_FORMS_METHOD_FIELD', self.DEFAULT_METHOD_FIELD)
        method_field = app.config['REST_FORMS_METHOD_FIELD']

        app.jinja_options['extensions'].append(RestFormsJinja)
        app.jinja_env.extend(flask_restforms_field=method_field)

        app.wsgi_app = RestFormsMiddleware(app.wsgi_app, method_field)


form_regex = re.compile(r'<form[^>]*>')
method_regex = re.compile(r'method=[\'\"]*(\w+)[\'\"]*')
class RestFormsJinja(Extension):
    IGNORED_METHODS = ['GET', 'HEAD']

    def filter_stream(self, stream):
        for token in stream:
            if token.type != 'data':
                yield token
                continue

            pos = 0
            lineno = token.lineno

            while 1:
                form_match = form_regex.search(token.value, pos)

                if form_match is None:
                    break

                new_pos = form_match.start()
                if new_pos > pos:
                    preval = token.value[pos:new_pos]
                    yield Token(lineno, 'data', preval)
                    lineno += count_newlines(preval)

                form_str = form_match.group()

                method_match = method_regex.search(form_str)
                method = method_match.group(1) if method_match else None

                if not method or method.upper() in self.IGNORED_METHODS:
                    val = token.value[new_pos:form_match.end()]
                    yield Token(lineno, 'data', val)
                    lineno += count_newlines(val)
                else:
                    method_str = method_match.group()
                    new_method = method_str.replace(method, 'POST')
                    new_form = form_str.replace(method_str, new_method)
                    yield Token(lineno, 'data', new_form)
                    lineno += count_newlines(new_form)

                    input_name = self.environment.flask_restforms_field
                    input_str = f'<input type="hidden" name="{input_name}" value="{method}" />'
                    yield Token(lineno, 'data', input_str)
                    lineno += count_newlines(input_str)

                pos = form_match.end()

            if pos < len(token.value):
                yield Token(lineno, 'data', token.value[pos:])


class RestFormsMiddleware:
    def __init__(self, app, method_field):
        self.app = app
        self.method_field = method_field

    def __call__(self, environ, start_response):
        request = self._get_request(environ)
        method = self._get_method_field_value(request)
        if method:
            environ['REQUEST_METHOD'] = method

        return self.app(environ, start_response)

    def _get_request(self, environ):
        return environ['werkzeug.request']

    def _get_method_field_value(self, request):
        return request.form.get(self.method_field)
