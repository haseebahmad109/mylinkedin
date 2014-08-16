import json
from psycopg2._psycopg import _connect
from sockjs.tornado import SockJSConnection
from LinkedApp.models import User, Notifications
from django.contrib.auth import authenticate


class ChatConnection(SockJSConnection):
    _connected = set()

    def on_open(self, request):
        #print "OPEN"
        #print request.get_cookie('name')
        #self._connected.add(request.user)
        self._connected.add(self)
        self.send("connected")
        print self

    def on_message(self, data):
        data = json.loads(data)
        print data
        try:
            x = Notifications.objects.filter(id=data['notification_id'])[0]
            d = {'des':x.description,
                 'of_whom':x.of_whom.id,
                 'not_id':x.id}
        except Notifications.DoesNotExist:
            d = "not good"

        self.broadcast(self._connected, d)


    def on_close(self):
        #print "CLOSE"
        self.connection_closed = True

    def _package_message(self, m):
        return {'date': m.date.strftime('%H:%M:%S'),
                'message': m.message,
                'name': m.name}
