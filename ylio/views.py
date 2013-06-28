import re

from flask import (
    abort,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from ylio import app, signals
from ylio.models import Links

# This re is taken from django and slightly modified
# http://git.io/A19tSw
url_re = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten():
    url = request.form.get('url')

    if url is None:
        error = 'missing required param'
        signals.link_refused.send(g.sender(), error=error)
        return jsonify(error=error), 400
    elif len(url) >= 2000:
        error = 'url too long'
        signals.link_refused.send(g.sender(), error=error)
        return jsonify(error=error), 400

    elif not re.match(url_re, url):
        error = 'invalid url'
        signals.link_refused.send(g.sender(), error=error)
        return jsonify(error=error), 400

    elif canonical_url(url) in app.config['DOMAIN_BLACKLIST']:
        error = 'blacklisted domain'
        signals.link_refused.send(g.sender(), error=error)
        return jsonify(error=error), 403

    id36 = Links.new(url, request.remote_addr)
    if id36 is None:
        return jsonify(error='server error'), 500

    short_url = url_for('shortened', id=id36, _external=True)
    return jsonify(url=short_url)


@app.route('/<id>')
def shortened(id):
    link = Links.get(id)

    if link is None:
        abort(404)
    elif not link['active']:
        signals.disabled_link_visited.send(g.sender(), request=request)
        return render_template('disabled.html'), 410

    signals.link_visited.send(g.sender(), request=request)
    return redirect(link['target']), 301


def canonical_url(url):
    url = url.lower()

    if url.startswith('http://'):
        url = url[7:]
    if url.startswith('https://'):
        url = url[8:]
    if url.startswith('www.'):
        url = url[4:]
    if url.endswith('/'):
        url = url[:-1]
    if url.endswith('.'):
        url = url[:-1]

    url = url.split('/', 1)[0]
    return url


@app.errorhandler(404)
def not_found(error):
    signals.not_found.send(g.sender(), request=request)
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(error):
    signals.server_error.send(g.sender(), request=request)
    return render_template('500.html'), 500
