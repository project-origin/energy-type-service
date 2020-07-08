import pandas as pd

from exception import EnergyCodeNotFoundException
from settings import E18_EMISSION_FILE, MIX_FILE
from util import hash_gsrn


HEADERS = ['timestamp_utc','sector', 'technology','share']


def get_emission_data(gsrn):
    """
    Returns emissions data as dict, or None if no data exists for the GSRN.
    
    All values are returned in g/Wh

    :param str gsrn:
    """
    
    hashed_gsrn = hash_gsrn(gsrn)

    with open(E18_EMISSION_FILE, 'rb') as f:
        df = pd.read_parquet(f)
            
        if hashed_gsrn in df.index:
            result = {}
            row = df.loc[df.index == hashed_gsrn]

            for key in row:
                value = row[key].values[0]
                if value != 0:
                    result[key] = value

            return result

        else:
            None


def get_residual_mix(sectors, begin_from, begin_to):
    """
    Returns a list of emissions for the given sector between the dates.

    All values are returned in g/Wh

    :param list[str] sectors: List of the sectors (price-zone) to filter on.
    :param datetime.datetime begin_from: timestamp inclusive
    :param datetime.datetime begin_to: timestamp exclusive

    """
    
    with open(MIX_FILE, 'rb') as f:
        df_read = pd.read_parquet(f)

        res = {}

        df_loc = df_read.loc[(df_read['sector'].isin(sectors)) & (df_read['timestamp_utc'] >= begin_from) & (df_read['timestamp_utc'] < begin_to)]

        for index, row in df_loc.iterrows():
            
            ts = row['timestamp_utc'].isoformat()
            
            if ts not in res:
                res[ts] = {
                    'timestamp_utc': ts, 
                    'sector': row['sector'],
                    'parts': []
                    }
                
            ts_obj = res[ts]
            
            emission = {}
            part = {
                'share': row['share'],
                'technology': row['technology'],   
                'emissions': emission
            }
            
            ts_obj['parts'].append(part)
            
            for key in df_loc:
                if key not in HEADERS:
                    if row[key] != 0:
                        emission[key] = row[key]
                
        result_list = [b for b in res.values()]


        for obj in result_list:
            
            mix = {}
            
            for part in obj['parts']:
                share = part['share']
                
                for key in part['emissions']:
                    if key in mix:
                        mix[key] += part['emissions'][key] * share
                    else:
                        mix[key] = part['emissions'][key] * share
            
            obj['mix_emissions'] = mix

        return result_list
