#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_miner_gathering():
	m = HumanMiner()
	s = Mine('iron')
	s.amount = 10
	tile = Tile()

	tile.chars.append(m)
	tile.items.append(s)

	for _ in range(100):
		tile.update(600)

	assert len(m.inventory) != 0
	assert s.amount != 10


def test_miner_source_search():
	pass


def test_miner_work_cycle():
	pass


def test_miner_can_keep_alive():
	pass