import pandas as pd

from exception import EnergyCodeNotFoundException
from settings import E18_EMISSION_FILE, MIX_FILE
from util import hash_gsrn


HEADERS = ['timestamp_utc','sector', 'technology','share', 'amount']


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
    Returns a json list of emissions for the given sector between the dates.

    All values are returned in g/Wh

    :param list[str] sectors: List of the sectors (price-zone) to filter on.
    :param datetime.datetime begin_from: timestamp inclusive
    :param datetime.datetime begin_to: timestamp exclusive

    """
    
    with open(MIX_FILE, 'rb') as f:
        df_read = pd.read_parquet(f)

        df_loc = df_read.loc[(df_read['sector'].isin(sectors) & (df_read['timestamp_utc'] >= begin_from) & (df_read['timestamp_utc'] < begin_to))]
        df_loc = df_loc.sort_values(['timestamp_utc', 'sector'])

        df_loc = df_loc.sort_values(['timestamp_utc', 'sector'])

        json_str =  df_loc.to_json(orient='records', date_format='iso')

        return json_str
