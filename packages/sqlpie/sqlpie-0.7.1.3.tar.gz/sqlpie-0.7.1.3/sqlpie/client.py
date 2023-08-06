from sqlpie.model_engine import ModelEngine
from sqlpie.project import Project
from sqlpie.exceptions import BadInputError
import yaml
import dag

class Sqlpie:
	#render single model
	#Sqlpie(model = 'model_1')
	#render single model with payload
	#Sqlpie(model = 'model_1', vars_payload={'key': 'value'}) 
	#render multiple selected models
	#Sqlpie(models = ['model_1', 'model_2']) 
	#render multiple selected models with payload
	#Sqlpie(models = ['model_1', 'model_2'], {'model_1': {'key': 'value'}})
	#render all but model that are passed in the excludes params
	#Sqlpie(excludes = ['model_3', model_4])
	#render all but model that are passed in the excludes params with payloads
	#Sqlpie(excludes = ['model_3', model_4], vars_payload={'model_1': {'key': value}}) 
	#render all models
	#Sqlpie()
	#render all models with payload
	#Sqlpie(vars_payload={'model_1': {'key':'value'}, 'model_2': { 'key': 'value' }})
  #render all models
  #include in client only selected models
	def __init__(self, **kwargs):
		self.models = {}
		self.table_index = {}
		self.sources_conf = self._set_source_conf()
		self.api_data = {'models': {}, 'selected_models': [], 'dag': {} }
		self.args = kwargs
		conf_keys = list(kwargs.keys())
		conf_keys.sort()
		self.dag = dag.DAG()
		self.dag_edges = []
		if not kwargs:
			self.render_all()
		elif conf_keys == ['vars_payload']:
			self.render_all(vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['models']:
			self.render_multiple(models=kwargs['models'])
		elif conf_keys == ['models', 'vars_payload']:
			self.render_multiple(models=kwargs['models'], vars_payload=kwargs['vars_payload'])
		elif conf_keys == ['excludes']:
			self.exclude_and_render(excludes=kwargs['excludes'])
		elif conf_keys.sort() == ['excludes', 'vars_payload']:
			self.exclude_and_render(excludes=kwargs['excludes'], vars_payload=kwargs['vars_payload'])
		else:
			raise BadInputError
		self.api_data['dag'] = self.build_dag_api_data(self.dag)
		self.build_table_index()
		self.build_viz_api_data()
	
	def _set_source_conf(self):
		sources_config_file = open("./config/sources.yml", "r")
		sources_conf = yaml.load(sources_config_file, Loader=yaml.FullLoader)
		sources_config_file.close()
		return sources_conf

	def render_all(self, vars_payload={}):
		all_models = Project.models()
		self.render_multiple(all_models, vars_payload)

	def exclude_and_render(self, excludes, vars_payload={}):
		all_models = Project.models()
		models_after_exclusion = [i for i in all_models if not i in excludes]
		self.render_multiple(models=models_after_exclusion, vars_payload=vars_payload)

	def render_multiple(self, models, vars_payload={}):
		for model in Project.models():
			if model in vars_payload.keys():
				rendered_model =  self.render_single(model, vars_payload[model])
			else:
				rendered_model = self.render_single(model)
			if model in models:
				self.api_data['selected_models'].append(model)
				self.append_to_dag(rendered_model)

	def render_single(self, model, vars_payload={}):
		model = ModelEngine(model, vars_payload)
		self.models[model.model] = model
		self.api_data['models'][model.model] = self.build_model_api_data(model)
		return model

	def build_model_api_data(self, model):
		api_data = self.build_dag_api_data(model.dag)
		api_data['staging_model'] = model.staging_model
		api_data['sources'] =  model.model_sources
		api_data['rendered_model'] = model.rendered_model
		return api_data

	def build_dag_api_data(self, dag):
		return 	{
							'ind_nodes': dag.ind_nodes(),
							'all_leaves': dag.all_leaves(),
							'graph_object': self.parse_graph_object(dag.graph),
							'dag_topological_sort': dag.topological_sort(),
							'dag_itterable_object': self.dag_itterable_object(dag)
						}

	def append_to_dag(self, model):
		for edge in model.edges:
			source_table = edge[0]
			destination_table = edge[1]
			self.dag.add_node_if_not_exists(source_table)
			self.dag.add_node_if_not_exists(destination_table)
			if edge not in self.dag_edges:
				self.dag_edges.append(edge)
				self.dag.add_edge(source_table, destination_table)

	def dag_itterable_object(self, dag):
		obj = {}
		for node in dag.topological_sort():
			obj[node] = {'predecessors': dag.predecessors(node), 'downstreams': dag.downstream(node) }
		return obj

	def parse_graph_object(self, graph):
		dict_graph = dict(graph)
		for key in dict_graph.keys():
			dict_graph[key] = list(dict_graph[key])
		return dict_graph

	def get_table_metadata(self, model_name, table_name):
		if model_name in self.sources_conf.keys():
			source_name = model_name
			return {
								'table_name': table_name,
								'schema': self.sources_conf[source_name]['schema'],
								'update_method': None
							}
			self.sources_conf[source_name]['schema']
		else:
			model = self.api_data['models'][model_name]
			if table_name in model['rendered_model'].keys():
				return {
								'table_name': model['rendered_model'][table_name]['execution_metadata']['destination_table'],
								'schema': model_name,
								'update_method': model['rendered_model'][table_name]['execution_metadata']['update_method']
								}
			else:
				return {
								'table_name': table_name,
								'schema': table_name,
								'update_method': None
								}

	def build_viz_api_data(self):
		for model_name, model in self.models.items():
			self.api_data['models'][model_name]['viz_data'] = self.generate_viz_data_from_dag(model.dag)
		self.api_data['dag']['viz_data'] = self.generate_viz_data_from_dag(self.dag)

	def generate_viz_data_from_dag(self, dag):
		data_for_viz = []
		for table in dag.topological_sort():
			downstream = dag.downstream(table)
			model = self.table_index[table]
			for dep_table in downstream:
				dep_model = self.table_index[dep_table]
				table_metadata = self.get_table_metadata(model, table)
				dep_table_metadata = self.get_table_metadata(dep_model, dep_table)
				data_for_viz.append({
														'from': table,
														'to': dep_table,
														'weight': 1,
														'custom_field':{
																						'source_schema': table_metadata['schema'], 
																						'destination_schema': dep_table_metadata['schema']
																						}
													})
		return data_for_viz

	def build_table_index(self):
		for model_name, model in self.models.items():
			for table in self.api_data['models'][model_name]['dag_topological_sort']:
				if table in model.model_sources.keys():
					self.table_index[table] = model.model_sources[table]['source_name']
				else:
					self.table_index[table] = model_name

