class BadInputError(Exception):
	@classmethod
	def message(cls, args):
		return f"The combination of the given args {argss} is invalid \n check our documentation at sqlpie.io/docs/sqlpie-lib"	

class UnknownSourceError(Exception):
	@classmethod
	def message(cls, source):
		return f"The source {source} is used but not declared in the sources configuration or in any one of the models"	