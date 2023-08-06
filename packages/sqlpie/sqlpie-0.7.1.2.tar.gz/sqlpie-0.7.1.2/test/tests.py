from sqlpie.client import Sqlpie
import unittest
from unittest.mock import MagicMock

example_model_client = Sqlpie(models=['example_model'], vars_payload={"example_model": {"test_var": "some_value"}})
example_model = example_model_client.models['example_model']
model_with_custom_staging_schema = Sqlpie(models=['model_with_custom_staging_schema']).models['model_with_custom_staging_schema']
all_models = Sqlpie()
all_models_with_payload = Sqlpie(vars_payload={"example_model": {"test_var": "some_value"}})
excludes = Sqlpie(excludes=['model_with_custom_staging_schema'])

class TestClient(unittest.TestCase):

  def test_dag_validity_for_single_model(self):
    self.assertEqual(example_model.dag.validate()[0], True)

  def test_ind_nodes(self):
  	self.assertEqual(example_model.dag.ind_nodes(),  ['example_source_schema.table_1', 'example_source_schema.table_2'])
  
  def test_all_leaves(self):
  	self.assertEqual(example_model.dag.all_leaves(),  ['example_model.example_3', 'example_model.example_2'])
  
  def test_model_key_names(self):
  	self.assertEqual(list(example_model.rendered_model.keys()), ['example_model_staging.example_1', 'example_model.example_3', 'example_model.example_2'])

  def test_custom_staging_schema(self):
  	self.assertEqual(model_with_custom_staging_schema.staging_model, 'testing_custom_staging_schema')

  def test_snippets_rendering(self):
  	rendered_query = example_model.rendered_model['example_model_staging.example_1']['rendered_query']
  	query = "\nselect *, date_trunc('month', CONVERT_TIMEZONE ('UTC', 'America/New_York', getdate()))::date\nfrom  example_source_schema_public.table_1\njoin  example_source_schema_public.table_2"
  	self.assertEqual(rendered_query, query)

  def test_vars_rendering_single_model(self):
    rendered_query = example_model.rendered_model['example_model.example_2']['rendered_query']
    query = "\nselect *, 'some_value'\nfrom  example_model_staging.example_1"
    self.assertEqual(rendered_query, query)

  def test_vars_rendering_all_models(self):
    rendered_query = all_models_with_payload.models['example_model'].rendered_model['example_model.example_2']['rendered_query']
    print(rendered_query)
    query = "\nselect *, 'some_value'\nfrom  example_model_staging.example_1"
    self.assertEqual(rendered_query, query)

  def test_model_names_extraction(self):
    self.assertEqual(example_model.all_models, ['model_with_custom_staging_schema', 'example_model'])

  def test_dag_validity_for_all_models_1(self):
    self.assertEqual(all_models.models['example_model'].dag.validate()[0], True)

  def test_dag_validity_for_all_models_2(self):
    self.assertEqual(all_models.models['model_with_custom_staging_schema'].dag.validate()[0], True)

  def test_excluding(self):
    self.assertEqual(excludes.api_data['selected_models'], ['example_model'])

  def test_model_api_data_keys(self):
    keys = [
            'ind_nodes',
            'all_leaves',
            'graph_object',
            'dag_topological_sort',
            'dag_itterable_object',
            'staging_model',
            'sources',
            'rendered_model',
            'viz_data'
            ]
    self.assertEqual( list(all_models.api_data['models']['example_model'].keys()) , keys)

  def test_dag_itterable_object_structure(self):
    itterable_object =  {'example_source_schema.table_1': {'predecessors': [], 'downstreams': ['example_model_staging.example_1']}, 'example_source_schema.table_2': {'predecessors': [], 'downstreams': ['example_model_staging.example_1']}, 'example_model_staging.example_1': {'predecessors': ['example_source_schema.table_1', 'example_source_schema.table_2'], 'downstreams': ['example_model.example_3', 'example_model.example_2']}, 'example_model.example_3': {'predecessors': ['example_model_staging.example_1'], 'downstreams': []}, 'example_model.example_2': {'predecessors': ['example_model_staging.example_1'], 'downstreams': []}}
    self.assertEqual(sorted(all_models.api_data['models']['example_model']['dag_itterable_object'].items()), sorted(itterable_object.items()))
  
  def test_all_models_edges(self):
    output_edges = sorted(all_models.dag_edges)
    edges = sorted([['example_model.example_1', 'testing_custom_staging_schema.example_1'], ['example_model.example_6', 'model_with_custom_staging_schema.example_1'], ['example_model_staging.example_1', 'example_model.example_2'], ['example_model_staging.example_1', 'example_model.example_3'], ['example_source_schema.table_1', 'example_model_staging.example_1'], ['example_source_schema.table_2', 'example_model_staging.example_1'], ['example_source_schema.table_3', 'testing_custom_staging_schema.example_1'], ['testing_custom_staging_schema.example_1', 'model_with_custom_staging_schema.example_1']])
    self.assertEqual(output_edges, edges)

  def test_single_model_edges(self):
    output_edges = sorted(example_model_client.dag_edges)
    edges = sorted([['example_source_schema.table_1', 'example_model_staging.example_1'], ['example_source_schema.table_2', 'example_model_staging.example_1'], ['example_model_staging.example_1', 'example_model.example_3'], ['example_model_staging.example_1', 'example_model.example_2']])

  def test_api_data_structure(self):
    api_data_keys_output = list(all_models.api_data.keys())
    api_data_keys = ['models', 'selected_models', 'dag']
    self.assertEqual(api_data_keys_output, api_data_keys)

  def test_dag_api_data(self):
    dag_api_data_keys_output = list(all_models.api_data['dag'].keys())
    dag_api_data_keys = ['ind_nodes', 'all_leaves', 'graph_object', 'dag_topological_sort', 'dag_itterable_object', 'viz_data']
    self.assertEqual(dag_api_data_keys_output, dag_api_data_keys)

if __name__ == '__main__':
  unittest.main()
