import os
import logging

PROJECT_NAME = 'EnergyTypeService'
ENERGYCODE_FILE = os.environ.get('ENERGYCODE_FILE')
E18_EMISSION_FILE = os.environ.get('E18_EMISSION_FILE')
MIX_FILE = os.environ.get('MIX_FILE')

AZURE_APP_INSIGHTS_CONN_STRING = os.environ.get(
    'AZURE_APP_INSIGHTS_CONN_STRING')

_LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

if hasattr(logging, _LOG_LEVEL):
    LOG_LEVEL = getattr(logging, _LOG_LEVEL)
else:
    raise ValueError('Invalid LOG_LEVEL: %s' % _LOG_LEVEL)
