__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.7.0'

import typing as tp
import warnings as wn
from take_resolution.utils import load_params
from take_resolution.utils import build_dataframe
from take_resolution.utils import filter_rows
from take_resolution.utils import select_columns
from take_resolution.utils import spark_to_pandas
from take_resolution.bot_flow import get_element
from take_resolution.bot_flow import load_json
from take_resolution.bot_flow import map_states
from take_resolution.bot_flow import build_graph
with wn.catch_warnings():
	wn.simplefilter('ignore')
	import pyspark as ps


CONTEXT = ps.SQLContext


def run(sql_context: CONTEXT, bot_identity: str) -> tp.Dict[str, tp.Any]:
	"""Run TakeResolution.
	
	:param sql_context: Spark SQL context.
	:type sql_context: ``pyspark.SQLContext``
	:param bot_identity: Bot identity on database.
	:type bot_identity: ``str``
	:return: Parameters and results for MLFlow register.
	:rtype: ``dict`` from ``str`` to ``any``
	"""
	params = load_params()
	
	bot_flow_database = params['bot_flow_database']
	bot_flow_table = params['bot_flow_table']
	sp_df = build_dataframe(sql_context, bot_flow_database, bot_flow_table)
	
	bot_column = params['bot_column']
	application_column = params['application_column']
	application_value = params['application_value']
	sp_df_selected = filter_rows(sp_df, (bot_column, bot_identity), (application_column, application_value))
	
	flow_column = params['flow_column']
	sp_df_flow = select_columns(sp_df_selected, flow_column)
	
	df_flow_raw = spark_to_pandas(sp_df_flow)
	
	str_flow_raw = get_element(df_flow_raw)
	dct_flow_raw = load_json(str_flow_raw)
	dct_flow_states = map_states(dct_flow_raw)
	dgr_flow_proc = build_graph(dct_flow_states)
	
	return {
		'params': params,
		'result': {
			'raw': {
				'flow': df_flow_raw
			},
			'intermediate': {
				'flow': dct_flow_raw
			},
			'primary': {
				'flow': dgr_flow_proc
			},
			'features': {
			
			},
			'model_input': {
			
			},
			'models': {
			
			},
			'model_output': {
			
			},
			'reporting': {
			
			}
		}
	}
