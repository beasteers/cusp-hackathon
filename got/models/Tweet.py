class Tweet:
	
	def __init__(self, **kw):
		self.__dict__.update(kw)

	def attrs(self):
		return self.__dict__