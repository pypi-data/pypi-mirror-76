class BadInputError(Exception):
	pass

class UnknownSourceError(Exception):
	@classmethod
	def message(cls, source):
		return f"The source {source} is used but not declared in the sources configuration"	