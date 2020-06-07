from flask import Flask, request, jsonify, abort

from exception import EnergyCodeNotFoundException
from settings import ENERGYCODE_FILE

if ENERGYCODE_FILE:
    from file_energycodes import get_tech_fuel_code
else:
    from random_energycodes import get_tech_fuel_code


app = Flask(__name__)


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

    try:
        tech_code, fuel_code = get_tech_fuel_code(gsrn)

        return jsonify({
            'technologyCode': tech_code,
            'fuelCode': fuel_code,
        })

    except EnergyCodeNotFoundException:
        return f'Could not resolve gsrn {gsrn}', 404

if __name__ == '__main__':
    app.run(port=8765)
