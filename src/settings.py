import os

PROJECT_NAME = 'EnergyTypeService'
ENERGYCODE_FILE = os.environ.get('ENERGYCODE_FILE')
E18_EMISSION_FILE = os.environ.get('E18_EMISSION_FILE')
MIX_FILE = os.environ.get('MIX_FILE')

ISO_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

AZURE_APP_INSIGHTS_CONN_STRING = os.environ.get(
    'AZURE_APP_INSIGHTS_CONN_STRING')
