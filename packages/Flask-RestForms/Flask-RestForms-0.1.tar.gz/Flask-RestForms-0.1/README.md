# Flask REST Forms

Badges

Flask REST Forms provides a transparent interface for adding REST-like forms to your Jinja templates.

```html
<form method="DELETE" action="/resource/{{ id }}">
    ...
</form>
```

## Installation

Install the extension with pip:

```sh
$ pip install -U flask-restforms
```

## Usage

Once installed, the extension just has to be loaded after the application is created:

```py
import flask
from flask_restforms import FlasRestForms

app = flask.Flask(__name__)
flask_restforms = FlaskRestForms(app)
```
