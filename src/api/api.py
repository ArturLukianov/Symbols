import os, sys
import logging

sys.path.append('.')
sys.path.append('..')
from src.core.worldthread import WorldThread
from src.core import Location, HumanPeasant, Cucumber, Well, Field, Mine


import eventlet
eventlet.monkey_patch()


import socketio


sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
app = socketio.WSGIApp(sio)


class SocketIOHandler(logging.Handler):
    def __init__(self, socket, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.socket = socket

    def emit(self, record):
        self.socket.emit('log', {'text': record.msg}, broadcast=True)


logger = logging.getLogger('symbols')

ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

sh = SocketIOHandler(socket=sio)

logger.addHandler(ch)
logger.addHandler(sh)


locs = [Location(), Well(), Field(), Mine(10)]
locs[0].add_char(HumanPeasant())
locs[0].connect(locs[1])
locs[0].chars[0].inventory.append(Cucumber())
locs[0].connect(locs[2])
locs[1].connect(locs[2])
locs[0].connect(locs[3])
world = WorldThread(locs=locs)

@sio.event
def connect(sid, environ):
    print('connect', sid)

    locs = {
        'nodes': [loc.to_d3() for loc in world.locs],
        'links': []
    }

    for loc in world.locs:
        for link in loc.locs:
            locs['links'].append({
                'source': id(loc),
                'target': id(link)
            })

    sio.emit('locs', locs)


if __name__ == "__main__":
    world.start()


    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
