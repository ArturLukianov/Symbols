import os, sys
import logging

sys.path.append('.')
sys.path.append('..')
from src.core.worldthread import WorldThread
from src.core import Location, HumanPeasant, Cucumber, Well, Field


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


@sio.event
def connect(sid, environ):
    print('connect', sid)

@sio.event
def get_locs(sid, environ):
    sio.emit('locs', [])


if __name__ == "__main__":
    locs = [Location(), Well(), Field()]
    locs[0].add_char(HumanPeasant())
    locs[0].connect(locs[1])
    locs[0].chars[0].inventory.append(Cucumber())
    locs[0].connect(locs[2])
    world = WorldThread(locs=locs)
    world.start()


    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
