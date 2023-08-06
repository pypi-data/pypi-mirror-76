# run pip install -r requirements.txt
import glob
import sys
from os import listdir

class Project:
	
	@staticmethod
	def models():
		all_paths = Project._all_model_paths()
		return list(map(lambda x: x.split('/')[-1].split('.')[0] , all_paths))

	@staticmethod
	def model_paths():
		all_paths = Project._all_model_paths()
		models_and_paths = list(map(lambda x: {x.split('/')[-1].split('.')[0]: x} , all_paths))
		models_and_paths_list = {}
		for item in models_and_paths:
			model_name = list(item)[0]
			models_and_paths_list[model_name] = item[model_name]
		return models_and_paths_list

	@staticmethod
	def _all_model_paths():
		return glob.glob('./models/*')