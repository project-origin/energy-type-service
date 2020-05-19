from random import choice
from itertools import product


thermal_tech_codes = (
     'T050000', 'T050100', 'T050101', 'T050102', 'T050200', 'T050201', 'T050202', 'T050300',
     'T050600', 'T050601', 'T050602', 'T050700', 'T050701', 'T050702', 'T050800', 'T050801',
)


thermal_fuel_codes = (
    'F02010100', 'F02010200', 'F02010300', 'F02010401', 'F02010400', 'F02010500', 'F02020000',
    'F02030100'
)


thermal_combinations = tuple(product(thermal_tech_codes, thermal_fuel_codes))


combinations = (

    # Solar
    ('T010000', 'F01040100'),
    ('T010100', 'F01040100'),
    ('T010101', 'F01040100'),
    ('T010102', 'F01040100'),

    # Wind
    ('T020000', 'F01050100'),
    ('T020001', 'F01050100'),
    ('T020002', 'F01050100')
)

other_combinations = (
    # Hydro
    ('T030400', 'F01050200'),

    # Marine
    ('T040101', 'F01050200'),

    # Nuclear
    ('T060101', 'F03010101')
)


# Increase the number of combinations which is not T05XXXX
combinations += combinations * 50 

# Add more alternatives
combinations += other_combinations * 10

# Add and add the thermal plants.
combinations += thermal_combinations


def get_random_combination():
    """
    :rtype: (str, str)
    :return: Tuple of (technologyCode, fuelCode)
    """
    return choice(combinations)
