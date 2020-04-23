from flask import Flask, request, jsonify

from energycodes import get_random_combination


app = Flask(__name__)


@app.route('/get-energy-type', methods=['GET'])
def projects():
    """
    Query parameters:
        gsrn : str

    Returns JSON body with:
        technologyCode : str
        fuelCode : str
    """
    gsrn = request.args.get('gsrn')

    # TODO Take GSRN into account...

    tech_code, fuel_code = get_random_combination()

    return jsonify({
        'technologyCode': tech_code,
        'fuelCode': fuel_code,
    })


if __name__ == '__main__':
    app.run(port=8765)
