from .gatherer import *

class HumanWoodcutter(HumanGatherer):
	profession = 'woodcutter'
	resource_type = None
	resource_source = None

	def __init__(self, name=None):
		super().__init__(name)

	def work(self, location, time):
		if self.sub_status == None:
			self.change_sub_status('chopping')

		if self.sub_status == 'chopping':
			work_status = self.gather_resource()
			if work_status != 'success':
				if work_status == 'no source' or work_status == 'source empty':
					self.change_sub_status('going to unchecked forests')

		if self.sub_status == 'going to unchecked forests':
			unchecked = self.short_memory.get('unchecked forests', [])
			if len(unchecked) > 0:
				self.short_memory['checking forest'] = unchecked[0]
				unchecked = unchecked[1:]
				self.short_memory['unchecked forests'] = unchecked
				self.change_sub_status('checking forest')
			else:
				forests = []
				for i in location.locs:
					if i.is_forest:
						forests.append(i)
				self.short_memory['unchecked forests'] = forests

		if self.sub_status == 'checking forest':
			forest = self.short_memory.get('checking forest', None)
			if forest != None:
				if forest.amount > 0:
					self.resource_source = forest
				self.short_memory['checking forest'] = None
				self.change_sub_status('chopping')