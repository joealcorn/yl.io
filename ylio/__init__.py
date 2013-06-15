from flask import Flask, current_app, g

app = Flask(__name__, static_folder=None)
app.config.from_pyfile('config.py')

if app.config.get('SENTRY_DSN'):
    from raven.contrib.flask import Sentry
    sentry = Sentry(app)


# Route static folder to /static in dev
# and a subdomain in production
app.static_folder = 'static'
static_path = '/<path:filename>'
static_subdomain = 'static'
if app.config.get('SERVER_NAME') is None:
    static_path = '/static/<path:filename>'
    static_subdomain = None

app.add_url_rule(
    static_path,
    endpoint='static',
    subdomain=static_subdomain,
    view_func=app.send_static_file
)


@app.before_request
def set_signal_sender():
    g.sender = current_app._get_current_object


from flask.ext.assets import Environment, Bundle
assets = Environment(app)
js = Bundle(
    'js/colorpicker.js',
    'js/modernizr.js',
    'js/lightordark.js',
    'js/ylio.js',
    filters='jsmin',
    output='scripts.js'
)

css = Bundle(
    'css/colorpicker.css',
    'css/ylio.css',
    filters='cssmin',
    output='styles.css'
)

assets.register('js', js)
assets.register('css', css)

import ylio.views
