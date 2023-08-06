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
  	self.assertEqual(example_model.dag.ind_nodes(),  ['example_source_schema.table_1', 'example_source_schema.table_2', 'example_source_schema.table_3'])
  
  def test_all_leaves(self):
  	self.assertEqual(example_model.dag.all_leaves(),  ['example_model.example_3', 'example_model.example_2'])
  
  def test_model_key_names(self):
  	self.assertEqual(list(example_model.rendered_model.keys()), ['example_model_staging.example_1', 'example_model.example_3', 'example_model.example_2'])

  def test_custom_staging_schema(self):
  	self.assertEqual(model_with_custom_staging_schema.staging_model, 'custom_staging_schema')

  def test_snippets_rendering(self):
  	rendered_query = example_model.rendered_model['example_model_staging.example_1']['rendered_query']
  	query = "\nselect *, date_trunc('month', CONVERT_TIMEZONE ('UTC', 'America/New_York', getdate()))::date\nfrom  example_source_schema_public.table_1 table_1\njoin  example_source_schema_public.table_2 table_2\non table_1.id = table_2.id\njoin  example_source_schema_public.table_3 table_3\non table_2.table_3_id = table_3.id"
  	self.assertEqual(rendered_query, query)

  def test_vars_rendering_single_model(self):
    rendered_query = example_model.rendered_model['example_model.example_2']['rendered_query']
    query = "\nselect *, 'some_value'\nfrom  example_model_staging.example_1"
    self.assertEqual(rendered_query, query)

  def test_vars_rendering_all_models(self):
    rendered_query = all_models_with_payload.models['example_model'].rendered_model['example_model.example_2']['rendered_query']
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
    itterable_object =  {'example_source_schema.table_1': {'predecessors': [], 'downstreams': ['example_model_staging.example_1']}, 'example_source_schema.table_2': {'predecessors': [], 'downstreams': ['example_model_staging.example_1']}, 'example_source_schema.table_3': {'predecessors': [], 'downstreams': ['example_model_staging.example_1']}, 'example_model_staging.example_1': {'predecessors': ['example_source_schema.table_1', 'example_source_schema.table_2', 'example_source_schema.table_3'], 'downstreams': ['example_model.example_3', 'example_model.example_2']}, 'example_model.example_3': {'predecessors': ['example_model_staging.example_1'], 'downstreams': []}, 'example_model.example_2': {'predecessors': ['example_model_staging.example_1'], 'downstreams': []}}
    self.assertEqual(sorted(all_models.api_data['models']['example_model']['dag_itterable_object'].items()), sorted(itterable_object.items()))
  
  def test_all_models_edges(self):
    output_edges = sorted(all_models.dag_edges)
    edges = sorted([['example_source_schema.table_3', 'custom_staging_schema.example_1'], ['example_model_staging.example_1', 'custom_staging_schema.example_1'], ['example_model.example_3', 'model_with_custom_staging_schema.example_1'], ['custom_staging_schema.example_1', 'model_with_custom_staging_schema.example_1'], ['example_source_schema.table_1', 'example_model_staging.example_1'], ['example_source_schema.table_2', 'example_model_staging.example_1'], ['example_source_schema.table_3', 'example_model_staging.example_1'], ['example_model_staging.example_1', 'example_model.example_3'], ['example_model_staging.example_1', 'example_model.example_2']])
    self.assertEqual(output_edges, edges)

  def test_single_model_edges(self):
    output_edges = sorted(example_model_client.dag_edges)
    edges = sorted([['example_source_schema.table_1', 'example_model_staging.example_1'], ['example_source_schema.table_2', 'example_model_staging.example_1'], ['example_model_staging.example_1', 'example_model.example_3'], ['example_model_staging.example_1', 'example_model.example_2']])

  def test_api_data_structure(self):
    api_data_keys_output = list(all_models.api_data.keys())
    api_data_keys = ['models', 'selected_models', 'dag', 'table_index']
    self.assertEqual(api_data_keys_output, api_data_keys)

  def test_dag_api_data(self):
    dag_api_data_keys_output = list(all_models.api_data['dag'].keys())
    dag_api_data_keys = ['ind_nodes', 'all_leaves', 'graph_object', 'dag_topological_sort', 'dag_itterable_object', 'viz_data']
    self.assertEqual(dag_api_data_keys_output, dag_api_data_keys)
  
  def test_table_index_output(self):
    table_index = {'custom_staging_schema.example_1': {'source_name': 'model_with_custom_staging_schema', 'schema': 'custom_staging_schema', 'table_name': 'custom_staging_schema.example_1', 'update_method': 'append', 'included_in': ['model_with_custom_staging_schema']}, 'model_with_custom_staging_schema.example_1': {'source_name': 'model_with_custom_staging_schema', 'schema': 'model_with_custom_staging_schema', 'table_name': 'model_with_custom_staging_schema.example_1', 'update_method': 'append', 'included_in': []}, 'example_model_staging.example_1': {'source_name': 'example_model', 'schema': 'example_model_staging', 'table_name': 'example_model_staging.example_1', 'update_method': 'append', 'included_in': ['example_model']}, 'example_model.example_3': {'source_name': 'example_model', 'schema': 'example_model', 'table_name': 'example_model.example_3', 'update_method': 'append', 'included_in': ['model_with_custom_staging_schema']}, 'example_model.example_2': {'source_name': 'example_model', 'schema': 'example_model', 'table_name': 'example_model.example_2', 'update_method': 'append', 'included_in': []}, 'example_source_schema.table_3': {'source_type': 'source', 'source_name': 'example_source_schema', 'schema': 'example_source_schema_public', 'table_name': 'table_3', 'destination_table': 'custom_staging_schema.example_1', 'included_in': ['model_with_custom_staging_schema', 'example_model']}, 'example_source_schema.table_1': {'source_type': 'source', 'source_name': 'example_source_schema', 'schema': 'example_source_schema_public', 'table_name': 'table_1', 'destination_table': 'example_model_staging.example_1', 'included_in': ['example_model']}, 'example_source_schema.table_2': {'source_type': 'source', 'source_name': 'example_source_schema', 'schema': 'example_source_schema_public', 'table_name': 'table_2', 'destination_table': 'example_model_staging.example_1', 'included_in': ['example_model']}}
    table_index_output = all_models.api_data['table_index']
    self.assertEqual(table_index, table_index_output)

  def test_table_index_included_in(self):
    table_3_included_in_output  = all_models.api_data['table_index']['example_source_schema.table_3']['included_in']
    table_3_included_in = ['model_with_custom_staging_schema', 'example_model']
    self.assertEqual(table_3_included_in, table_3_included_in_output)

if __name__ == '__main__':
  unittest.main()
