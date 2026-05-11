# converter_ui.py - interface for the unit converter by Mo

from . import converter_engine as eng
#from mohammed.quiz import run_quiz

def print_table(results):
    """
    Printing the conversion results as a table
    """
    print(f"\n{'Unit':<28} {'Value':>16}")
    print("-" * 46)
    for unit, val in results.items():
        name = eng.UNIT_NAMES[unit]
        print(f"{name+' ('+unit+')':<28} {val:<16.4g}")
    print("-" * 46)

# Asking the user to pick a unit by number or symbol, grouped by category
def pick_unit(prompt):
    units_flat = []
    print()
    i = 1
    for category, symbols in eng.CATEGORIES.items():
        print(f"  [{category}]")
        for symbol in symbols:
            print(f"  {i:>2}. {symbol:<10} {eng.UNIT_NAMES[symbol]}")
            units_flat.append(symbol)
            i += 1
        print()
    while True:
        raw = input(f"{prompt} (number or symbol): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(units_flat):
            return units_flat[int(raw) - 1]
        if raw in eng.ALL_UNITS:
            return raw
        print("  Not recognised, try again.")


# Prompting the user for a number and continuing till one is input
def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("  Please enter a valid number.")

# Print EM region (name and wavelength range only)
def print_em_region(joules):
    region = eng.get_em_region(joules)
    print(f"  EM Region   : {region['name']}  ({region['wavelength_range']})")

# Warnings for units that are not straightforward energy units
UNIT_WARNINGS = {
    "K":    "  Note: Kelvin here is converted to thermal energy using E = kB x T.",
    "Hz":   "  Note: Hz is converted to energy using E = h x freq.",
    "nm":   "  Note: nm is converted to energy using E = hc / wavelength.",
    "cm-1": "  Note: cm-1 (wavenumber) is converted to energy using E = hc x wavenumber.",
}


# Main unit conversion
def run_conversion():
    print("\n--- UNIT CONVERSION ---")
    from_unit = pick_unit("Select input unit")
    if from_unit in UNIT_WARNINGS:
        print(UNIT_WARNINGS[from_unit])
    value = get_float(f"  Enter value in {from_unit}: ")

    results = eng.convert_all(value, from_unit)
    joules  = eng.to_joules(value, from_unit)
    level   = eng.classify_energy(joules)

    print_table(results)
    print(f"\n  Energy level: {level}")
    print(f"  Energy in J : {joules:.4e} J")
    print_em_region(joules)
    print()

# Physics mode
def run_physics():
    print("\n--- PHYSICS CALCULATIONS ---")
    print("  Use this when you have a frequency, wavelength, mass,")
    print("  temperature, or voltage and want to find the energy.\n")
    print("  1. Planck  E = h*freq  (frequency)")
    print("  2. Planck  E = hc/wavelength  (wavelength)")
    print("  3. Einstein  E = mc^2")
    print("  4. Boltzmann  E = kB*T")
    print("  5. Voltage  E = qV")
    print("  6. Molar  per-molecule to per-mole")
    print("  7. Molar  per-mole to per-molecule")

    choice = input("\n  Select mode: ").strip()
    joules = None

    if choice == "1":
        freq = get_float("  Enter frequency (Hz): ")
        joules = eng.planck_frequency(freq)
    elif choice == "2":
        wl = get_float("  Enter wavelength (nm): ")
        joules = eng.planck_wavelength(wl)
    elif choice == "3":
        mass = get_float("  Enter mass (kg): ")
        joules = eng.einstein_mass_energy(mass)
    elif choice == "4":
        temp = get_float("  Enter temperature (K): ")
        joules = eng.boltzmann_thermal(temp)
    elif choice == "5":
        volts = get_float("  Enter voltage (V): ")
        n = get_float("  Enter number of electrons: ")
        joules = eng.voltage_energy(volts, n)
    elif choice == "6":
        j = get_float("  Enter energy per molecule (J): ")
        result = eng.to_molar(j)
        print(f"\n  Result: {result:.4e} J/mol\n")
        return
    elif choice == "7":
        j = get_float("  Enter energy per mole (J/mol): ")
        result = eng.from_molar(j)
        print(f"\n  Result: {result:.4e} J per molecule\n")
        return
    else:
        print("  Invalid choice.")
        return

    if joules is not None:
        results = {u: eng.from_joules(joules, u) for u in eng.ALL_UNITS}
        level = eng.classify_energy(joules)
        print_table(results)
        print(f"\n  Energy level: {level}")
        print(f"  Energy in J : {joules:.4e} J")
        print_em_region(joules)
        print()

# Checking if the units are compatible
def run_compatibility_check():
    print("\n--- DIMENSION COMPATIBILITY CHECK ---")
    print("  Use this to check if two units measure the same physical quantity.")
    unit1 = pick_unit("Select first unit")
    unit2 = pick_unit("Select second unit")
    if eng.check_compatible(unit1, unit2):
        print(f"\n  {unit1} and {unit2} are compatible.\n")
    else:
        print(f"\n  {unit1} and {unit2} are NOT compatible.\n")

# Printing conversion history
def show_history():
    print("\n--- CONVERSION HISTORY ---")
    record = eng.get_history()
    if not record:
        print("  No conversions yet.\n")
        return
    print(f"\n  {'#':<4} {'Input':<20} {'Joules':>16}")
    print("  " + "-" * 42)
    for i, entry in enumerate(record, 1):
        input_str = f"{entry['value']:.4g} {entry['unit']}"
        print(f"  {i:<4} {input_str:<20} {entry['joules']:<16.4e}")
    print()

    clear = input("  Clear history? [y/N]: ").strip().lower()
    if clear == "y":
        eng.clear_history()
        print("  History cleared.\n")

# How to use guide
def show_help():
    print("""
--- HOW TO USE ---

  1. Convert a unit
     Enter a value in any energy unit and get it
     converted to all other units instantly.

  2. Physics Mode
     Use this when you have a frequency, wavelength,
     mass, temperature or voltage but not an energy value.
     It calculates the energy using the relevant formula
     then converts it to all units.

  3. Compatibility Check
     Checks if two units measure the same physical
     quantity. For example J and kJ are compatible,
     but J and nm are not.

  4. Conversion History
     Shows the last 10 conversions performed.
     You can also clear the history from here.

  5. Quiz
     Test your knowledge on energy units.
""")


def main():
    print("\n========================================")
    print("      ENERGY UNIT CONVERTER v1.0")
    print("========================================")

    while True:
        print("\n  1. Convert a unit")
        print("  2. Physics Mode")
        print("  3. Compatibility check")
        print("  4. Conversion history")
        print("  5. Quiz")
        print("  h. How to use")
        print("  q. Quit")
        choice = input("\n  Select: ").strip().lower()

        if choice == "1":
            run_conversion()
        elif choice == "2":
            run_physics()
        elif choice == "3":
            run_compatibility_check()
        elif choice == "4":
            show_history()
        elif choice == "5":
            run_quiz()
        elif choice == "h":
            show_help()
        elif choice == "q":
            print("\n  Goodbye!\n")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
