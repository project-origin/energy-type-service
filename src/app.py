import logging
from flask import Flask, request, jsonify
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import AlwaysOnSampler

from exception import EnergyCodeNotFoundException
from settings import (
    PROJECT_NAME,
    ENERGYCODE_FILE,
    AZURE_APP_INSIGHTS_CONN_STRING,
)


if ENERGYCODE_FILE:
    from file_energycodes import get_tech_fuel_code
else:
    from random_energycodes import get_tech_fuel_code


app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


# Setup logging using OpenCensus / Azure
if AZURE_APP_INSIGHTS_CONN_STRING:
    print('Exporting logs to Azure Application Insight', flush=True)

    def __telemetry_processor(envelope):
        envelope.data.baseData.cloud_roleName = PROJECT_NAME
        envelope.tags['ai.cloud.role'] = PROJECT_NAME

    exporter = AzureExporter(connection_string=AZURE_APP_INSIGHTS_CONN_STRING)
    exporter.add_telemetry_processor(__telemetry_processor)

    FlaskMiddleware(
        app=app,
        sampler=AlwaysOnSampler(),
        exporter=exporter,
    )


@app.route('/get-energy-type', methods=['GET'])
def get_energy_type():
    """
    Query parameters:
        gsrn : str

    Returns JSON body with:
        technologyCode : str
        fuelCode : str
    """
    gsrn = request.args.get('gsrn')

    0/0

    try:
        tech_code, fuel_code = get_tech_fuel_code(gsrn)

        return jsonify({
            'success': True,
            'technologyCode': tech_code,
            'fuelCode': fuel_code,
        })
    except EnergyCodeNotFoundException:
        return jsonify({
            'success': False,
            'message': f'Could not resolve energy type for GSRN {gsrn}',
        })


if __name__ == '__main__':
    app.run(port=8765)
