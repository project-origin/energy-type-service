import pandas as pd

from exception import EnergyCodeNotFoundException
from settings import ENERGYCODE_FILE
from util import hash_gsrn


def get_tech_fuel_code(gsrn):
    """
    :rtype: (str, str)
    :return: Tuple of (technologyCode, fuelCode)
    """

    hashed_gsrn = hash_gsrn(gsrn)

    with open(ENERGYCODE_FILE, 'rb') as f:
        df = pd.read_parquet(f)

        if hashed_gsrn in df.index:
            row = df.loc[hashed_gsrn]
            return row.tech_code, row.fuel_code
        else:
            raise EnergyCodeNotFoundException()


def add_tech_fuel_code(gsrn, tech, fuel):
    """
    :rtype: (str, str)
    :return: Tuple of (technologyCode, fuelCode)
    """

    with open(ENERGYCODE_FILE, 'rb') as f:
        df = pd.read_parquet(f)

    hashed_gsrn = hash_gsrn(gsrn)
    df.loc[hashed_gsrn] = {'tech_code': tech, 'fuel_code': fuel}

    with open(ENERGYCODE_FILE, 'wb') as f:
        df.to_parquet(ENERGYCODE_FILE)
