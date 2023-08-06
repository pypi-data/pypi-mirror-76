__author__ = 'Gabriel Salgado and Moises Mendes'
__version__ = '0.9.2'

import typing as tp

from take_resolution.utils import CONTEXT
from take_resolution.utils import load_params
from take_resolution.utils import build_dataframe
from take_resolution.utils import filter_rows
from take_resolution.utils import filter_range_rows
from take_resolution.utils import select_columns
from take_resolution.utils import spark_to_pandas
from take_resolution.bot_flow import get_element
from take_resolution.bot_flow import load_json
from take_resolution.bot_flow import map_states
from take_resolution.bot_flow import build_graph


def run(sql_context: CONTEXT, bot_identity: str, min_date: str, max_date: str) -> tp.Dict[str, tp.Any]:
    """Run TakeResolution.
    
    :param sql_context: Spark SQL context.
    :type sql_context: ``pyspark.SQLContext``
    :param bot_identity: Bot identity on database.
    :type bot_identity: ``str``
    :param min_date: Beginning date to filter ("yyyy-mm-dd").
    :type min_date: ``str``
    :param max_date: Ending date to filter ("yyyy-mm-dd").
    :type max_date: ``str``
    :return: Parameters and results for MLFlow register.
    :rtype: ``dict`` from ``str`` to ``any``
    """
    params = load_params()
    
    bot_flow_database = params['bot_flow_database']
    bot_flow_table = params['bot_flow_table']
    sp_df = build_dataframe(sql_context, bot_flow_database, bot_flow_table)
    
    bot_flow_bot_column = params['bot_flow_bot_column']
    bot_flow_application_column = params['bot_flow_application_column']
    bot_flow_application_value = params['bot_flow_application_value']
    sp_df_selected = filter_rows(sp_df, (bot_flow_bot_column, bot_identity),
                                 (bot_flow_application_column, bot_flow_application_value))
    
    bot_flow_flow_column = params['bot_flow_flow_column']
    sp_df_flow = select_columns(sp_df_selected, bot_flow_flow_column)
    
    df_flow_raw = spark_to_pandas(sp_df_flow)
    
    str_flow_raw = get_element(df_flow_raw)
    dct_flow_raw = load_json(str_flow_raw)
    dct_flow_states = map_states(dct_flow_raw)
    dgr_flow_proc = build_graph(dct_flow_states)
    
    bot_events_database = params['bot_events_database']
    bot_events_table = params['bot_events_table']
    sp_df_events = build_dataframe(sql_context, bot_events_database, bot_events_table)
    
    bot_events_date_column = params['bot_events_date_column']
    sp_df_events_date = filter_range_rows(sp_df_events, bot_events_date_column, min_date, max_date)
    
    bot_events_bot_column = params['bot_events_bot_column']
    sp_df_events_filtered = filter_rows(sp_df_events_date, (bot_events_bot_column, bot_identity))
    
    bot_events_columns = params['bot_events_columns']
    sp_df_events_selected = select_columns(sp_df_events_filtered, bot_events_columns)
    
    df_events_raw = spark_to_pandas(sp_df_events_selected)
    
    return {
        'params': params,
        'result': {
            'raw': {
                'flow': df_flow_raw,
                'events': df_events_raw
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
