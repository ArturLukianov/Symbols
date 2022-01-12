from flask import Flask
import os, sys

sys.path.append('.')
sys.path.append('..')
from src.core.worldthread import WorldThread
from src.core import Tile, HumanPeasant


app = Flask(__name__)


if __name__ == "__main__":
    tiles = [Tile()]
    tiles[0].chars.append(HumanPeasant())
    world = WorldThread(tiles=tiles)
    world.start()
    app.run()
