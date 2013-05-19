from blinker import Namespace

from ylio.models import Links

signals = Namespace()

# Create our signals
link_shortened = signals.signal('link_shortened')
link_refused = signals.signal('link_refused')
link_visited = signals.signal('link_visited')
disabled_link_visited = signals.signal('disabled_link_visited')
not_found = signals.signal('not_found')
server_error = signals.signal('server_error')


def increment_clicks(sender, request):
    id36 = request.view_args['id']
    Links.increment_clicks(id36)
    print 'visited signal received'


# Connect our handlers
link_visited.connect(increment_clicks)
