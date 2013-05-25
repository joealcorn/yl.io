from threading import Thread

from blinker import Namespace

from ylio.models import Links
from ylio import app

signals = Namespace()

# Create our signals
link_shortened = signals.signal('link_shortened')
link_refused = signals.signal('link_refused')
link_visited = signals.signal('link_visited')
disabled_link_visited = signals.signal('disabled_link_visited')
not_found = signals.signal('not_found')
server_error = signals.signal('server_error')


def increment_stathat(stat, by=1):
    hat = StatHat(app.config['STATHAT_KEY'])
    if app.config['STATHAT_PREFIX'] is not None:
        stat = app.config['STATHAT_PREFIX'] + stat

    t = Thread(target=hat.count, args=(stat, by))
    t.start()


def increment_clicks(sender, request):
    id36 = request.view_args['id']
    Links.increment_clicks(id36)
    print 'visited signal received'


def stathat_link_shortened(sender):
    increment_stathat('links.shortened')
    print 'shortened signal received'


def stathat_link_refused(sender, error):
    error = error.lower().replace(' ', '_')
    increment_stathat('links.refused')
    increment_stathat('links.refused.' + error)
    print 'link refused signal received'


def stathat_404_errors(sender, request):
    increment_stathat('requests.404')
    print '404 signal received'


def stathat_500_errors(sender, request):
    increment_stathat('requests.500')
    print '500 signal received'

# Connect our handlers
link_visited.connect(increment_clicks)

if app.config.get('ENABLE_METRICS'):
    from stathat import StatHat
    link_shortened.connect(stathat_link_shortened)
    link_refused.connect(stathat_link_refused)
    not_found.connect(stathat_404_errors)
    server_error.connect(stathat_500_errors)
