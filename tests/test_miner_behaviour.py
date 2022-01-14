#!/usr/bin/env python3

import os, sys
sys.path.append('.')
sys.path.append('..')

from src.core import *


def test_miner_gathering():
	m = HumanMiner()
	s = Mine(10)
	loc = Location()
	loc.connect(s)
	loc.chars.append(m)

	for i in range(100):
		loc.update(600 + i)
		s.update(600 + i)

	assert len(m.inventory) != 0
	assert s.amount != 10


def test_miner_source_search():
	assert True


def test_miner_work_cycle():
	assert True