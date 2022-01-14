from .gatherer import *

class HumanMiner(HumanGatherer):
	profession = 'miner'
	resource_type = None
	resource_source = None

	def __init__(self, name=None):
		super().__init__(name)

	def work(self, tile, time):
		if self.sub_status == None:
			self.change_sub_status('mining')

		if self.sub_status == 'mining':
			work_status = self.gather_resource()
			if work_status != 'success':
				if work_status == 'no source' or work_status == 'source empty':
					self.change_sub_status('going to unchecked mines')

		if self.sub_status == 'going to unchecked mines':
			unchecked = self.short_memory.get('unchecked mines', [])
			if len(unchecked) > 0:
				self.short_memory['checking mine'] = unchecked[0]
				unchecked = unchecked[1:]
				self.short_memory['unchecked mines'] = unchecked
				self.change_sub_status('checking mine')
			else:
				mines = []
				for i in tile.items:
					if i.is_mine:
						mines.append(i)
				self.short_memory['unchecked mines'] = mines

		if self.sub_status == 'checking mine':
			mine = self.short_memory.get('checking mine', None)
			if mine != None:
				if mine.amount > 0:
					self.resource_source = mine
				self.short_memory['checking mine'] = None
				self.change_sub_status('mining')