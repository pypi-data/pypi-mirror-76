# Flask REST Forms

[![PyPI version](https://badge.fury.io/py/Flask-RestForms.svg)](https://badge.fury.io/py/Flask-RestForms)

Flask REST Forms provides a transparent interface for adding REST-like forms to your Jinja templates.

```html
<form method="DELETE" action="/resource/{{ id }}">
    ...
</form>
```

## Installation

Install the extension with pip:

```sh
$ pip install -U Flask-RestForms
```

## Usage

Once installed, the extension just has to be loaded after the application is created:

```py
import flask
from flask_restforms import FlasRestForms

app = flask.Flask(__name__)
flask_restforms = FlaskRestForms(app)
```
