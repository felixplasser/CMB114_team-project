# converter_engine.py  by Mo- Conversion happens here
# Constants from NIST CODATA 2018: https://physics.nist.gov/cuu/Constants/

import json

class constants:
    """"
    Collection of physical constants.
    """
    H  = 6.62607015e-34   # Planck constant (J·s)
    C  = 2.99792458e8     # Speed of light (m/s)
    KB = 1.380649e-23     # Boltzmann constant (J/K)
    E  = 1.602176634e-19  # Elementary charge (C)
    ME = 9.1093837015e-31 # Electron mass (kg)

constants.H

# Load database
with open("mohammed/Database.json", "r") as f:
    DB = json.load(f)

# Build lookup dicts from the database
UNITS = {u["symbol"]: u for u in DB["units"]}
UNIT_NAMES = {u["symbol"]: u["name"] for u in DB["units"]}
ALL_UNITS = [u["symbol"] for u in DB["units"]]
EM_REGIONS = DB["em_regions"]
ENERGY_LEVELS = DB["energy_levels"]

# Build category grouping
CATEGORIES = {}
for u in DB["units"]:
    cat = u["category"]
    if cat not in CATEGORIES:
        CATEGORIES[cat] = []
    CATEGORIES[cat].append(u["symbol"])

# Conversion history for the last 10 conversions
history = []

# Converting the value in unit given to Joules
def to_joules(value, unit):
    u = UNITS[unit]
    if u["type"] == "linear":
        return value * u["factor_to_J"]
    elif u["type"] == "photon_wavelength":
        return (H * C) / (value * u["scale_to_metres"])
    elif u["type"] == "photon_frequency":
        return H * (value * u["scale_to_Hz"])
    elif u["type"] == "wavenumber":
        return H * C * (value * u["scale_to_per_metre"])
    else:
        raise Exception("Type not supported.")

# Converting Joules to the given unit
def from_joules(joules, unit):
    u = UNITS[unit]
    if u["type"] == "linear":
        return joules / u["factor_to_J"]
    elif u["type"] == "photon_wavelength":
        return (H * C) / joules / u["scale_to_metres"]
    elif u["type"] == "photon_frequency":
        return joules / H / u["scale_to_Hz"]
    elif u["type"] == "wavenumber":
        return joules / (H * C * u["scale_to_per_metre"])

# Converting values to all units in the database, to return a dict
def convert_all(value, from_unit):
    joules = to_joules(value, from_unit)
    results = {u: from_joules(joules, u) for u in ALL_UNITS}
    save_to_history(value, from_unit, joules)
    return results
    
# Classifying energy as low, medium or high
def classify_energy(joules):
    if joules <= ENERGY_LEVELS["low_threshold_J"]:
        return ENERGY_LEVELS["labels"]["low"]
    elif joules >= ENERGY_LEVELS["high_threshold_J"]:
        return ENERGY_LEVELS["labels"]["high"]
    else:
        return ENERGY_LEVELS["labels"]["medium"]

# Return the EM region for a given energy in Joules
def get_em_region(joules):
    for region in EM_REGIONS:
        if joules <= region["max_energy_J"]:
            return region
    return EM_REGIONS[-1]

# Compatibility check
def check_compatible(unit1, unit2):
    dims1 = UNITS[unit1].get("dimensions", {})
    dims2 = UNITS[unit2].get("dimensions", {})
    return dims1 == dims2

# Saving last 10 conversions to make conversion history
def save_to_history(value, unit, joules):
    entry = {
        "value": value,
        "unit": unit,
        "joules": joules
    }
    history.append(entry)
    if len(history) > 10:
        history.pop(0)

# Return the conversion history 
def get_history():
    return history

# Clear the conversion history
def clear_history():
    history.clear()

# Physics Mode functions

# Planck law: E = h * frequency
def planck_frequency(freq_hz):
    return H * freq_hz
    
# Planck law: E = h * c / wavelength
def planck_wavelength(wavelength_nm):
    return (H * C) / (wavelength_nm * 1e-9)

# Einstein mass-energy: E = m * c²
def einstein_mass_energy(mass_kg):
    return mass_kg * C ** 2

# Boltzmann thermal energy: E = kB * T
def boltzmann_thermal(temp_k):
    return KB * temp_k
    
# Voltage energy: E = charge * voltage
def voltage_energy(voltage_v, num_electrons):
    return num_electrons * E * voltage_v

# Molar scaling: convert a per-molecule energy to per-mole
def to_molar(joules_per_molecule):
    na = 6.02214076e23
    return joules_per_molecule * na

# Molar scaling: convert a per-mole energy to per-molecule
def from_molar(joules_per_mole):
    na = 6.02214076e23
    return joules_per_mole / na
