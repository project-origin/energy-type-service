import logging
import datetime
from flask import Flask, request, jsonify
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import AlwaysOnSampler

from emissions import get_emission_data, get_residual_mix
from exception import EnergyCodeNotFoundException
from settings import (
    PROJECT_NAME,
    ENERGYCODE_FILE,
    AZURE_APP_INSIGHTS_CONN_STRING,
    ISO_FORMAT,
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

    handler = AzureLogHandler(
        connection_string=AZURE_APP_INSIGHTS_CONN_STRING,
        export_interval=5.0,
    )
    handler.add_telemetry_processor(__telemetry_processor)
    handler.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

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
    Returns technology code and fuel code for a specific GSRN.

    Takes 'gsrn' as query parameter.
    """
    gsrn = request.args.get('gsrn')

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
    except Exception as e:
        app.logger.exception(f'Exception for GSRN: {gsrn}\n\n{e}')
        raise


@app.route('/get-emissions', methods=['GET'])
def get_gsrn_emissions():
    """
    Returns emission data for a specific GSRN.

    Takes 'gsrn' as query parameter.
    """
    gsrn = request.args.get('gsrn')

    emissions = get_emission_data(gsrn)

    return jsonify({
        'success': emissions is not None,
        'emissions': emissions if emissions else {},
    })


@app.route('/residual-mix', methods=['GET'])
def get_mix_emissions():
    """
    Returns emissions data for the residual mix in the grid

    Takes 'sector' as query parameter.
    Takes 'begin_from' as query parameter.
    Takes 'begin_to' as query parameter.
    """

    sectors = request.args.getlist('sector')
    begin_from = datetime.datetime.strptime(request.args.get('begin_from'), ISO_FORMAT)
    begin_to = datetime.datetime.strptime(request.args.get('begin_to'), ISO_FORMAT)

    mix = get_residual_mix(sectors, begin_from, begin_to)

    return jsonify({
        'success': mix is not None,
        'residual-mix': mix if mix else {},
    })

if __name__ == '__main__':
    app.run(port=8765)
