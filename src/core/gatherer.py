from .human import *

class HumanGatherer(Human):
	profession = 'gatherer'
	resource_type = None
	resource_source = None

	def gather_resource(self):
		if self.resource_source == None:
			return 'no source'
		self.go_to(self.resource_source)
		if self.resource_source.amount <= 0:
			return 'source empty'
		resource = self.resource_source.take_resource()
		self.inventory.append(resource)
		return 'success'