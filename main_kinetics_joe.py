#!/usr/bin/env python3

"""
main.py
Authors: Caner and Joe

Main file for the Reaction Kinetics Simulator.

Caner mainly worked on:
- reaction_caner.py
- simulator_caner.py

Joe mainly worked on:
- plotter_joe.py
- data_export_joe.py
- user interface in this file

This program allows the user to simulate zero-order, first-order and
second-order chemical reactions and plot concentration against time.
"""

from Caner.Chemical_Reaction_Kinetics.reaction_caner import Reaction, calculate_arrhenius_rate_constant
from Caner.Chemical_Reaction_Kinetics.simulator_caner import Simulator
from Joe.Chemical_Reaction_Kinetics.plotter_joe import Plotter
from Joe.Chemical_Reaction_Kinetics.data_export_joe import *


def get_float_input(message):
    """
    Gets a number from the user.
    Keeps asking until the user enters a valid number.
    """

    while True:
        try:
            value = float(input(message))
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_int_input(message):
    """
    Gets an integer from the user.
    Used for menu choices and reaction order.
    """

    while True:
        try:
            value = int(input(message))
            return value
        except ValueError:
            print("Please enter a whole number.")


def create_reaction_from_user():
    """
    Asks the user for information and creates a Reaction object.
    """

    name = input("Enter a name for the reaction: ")

    print("\nChoose reaction order:")
    print("0 - Zero order")
    print("1 - First order")
    print("2 - Second order")

    order = get_int_input("Enter reaction order: ")

    print("\nHow do you want to enter the rate constant?")
    print("1 - Enter k directly")
    print("2 - Calculate k using the Arrhenius equation")

    k_choice = get_int_input("Enter choice: ")

    if k_choice == 1:
        rate_constant = get_float_input("Enter rate constant k: ")

    elif k_choice == 2:
        activation_energy = get_float_input("Enter activation energy Ea in J mol^-1: ")
        temperature = get_float_input("Enter temperature in K: ")
        pre_exponential = get_float_input("Enter pre-exponential factor A: ")

        rate_constant = calculate_arrhenius_rate_constant(
            activation_energy,
            temperature,
            pre_exponential
        )

        print(f"Calculated rate constant k = {rate_constant:.5g}")

    else:
        print("Invalid choice, using direct input for k.")
        rate_constant = get_float_input("Enter rate constant k: ")

    initial_concentration = get_float_input(
        "Enter initial concentration in mol dm^-3: "
    )

    reaction = Reaction(name, order, rate_constant, initial_concentration)

    return reaction


def print_summary(reaction, simulator, times, concentrations, rates):
    """
    Prints a useful summary of the simulation.
    """

    summary = simulator.get_summary(times, concentrations, rates)

    print("\nSimulation complete.")
    print(reaction.get_description())

    if summary["simulated_half_life"] is not None:
        print(f"Estimated half-life from simulation = {summary['simulated_half_life']} s")
    else:
        print("Half-life was not reached during this simulation.")

    print(f"Theoretical half-life = {summary['theoretical_half_life']:.3f} s")
    print(f"Final concentration = {summary['final_concentration']:.5f} mol dm^-3")
    print(f"Final rate = {summary['final_rate']:.5f}")
    print(f"Percentage reacted = {summary['percentage_reacted']:.2f}%")
    print(f"Average rate = {summary['average_rate']:.5f}")

    if summary["time_for_90_percent"] is not None:
        print(f"Time for 90% reacted = {summary['time_for_90_percent']} s")
    else:
        print("90% reacted was not reached during this simulation.")


def run_one_simulation():
    """
    Runs one reaction simulation and gives the user options to plot and save.
    """

    try:
        reaction = create_reaction_from_user()

        total_time = get_float_input("Enter total simulation time in seconds: ")
        time_step = get_float_input("Enter time step in seconds: ")

        simulator = Simulator(reaction, total_time, time_step)

        times, concentrations, rates = simulator.run_simulation()

        print_summary(reaction, simulator, times, concentrations, rates)

        print("\nFirst few results:")
        simulator.print_table(times, concentrations, rates)

        plotter = Plotter()

        plot_choice = input("\nDo you want to show the concentration graph? (y/n): ")

        if plot_choice.lower() == "y":
            plotter.plot_single_reaction(
                times,
                concentrations,
                reaction.reaction_name
            )

        rate_choice = input("Do you want to show the rate graph? (y/n): ")

        if rate_choice.lower() == "y":
            plotter.plot_rate_time(
                times,
                rates,
                reaction.reaction_name
            )

        save_choice = input("\nDo you want to save the data as a CSV file? (y/n): ")

        if save_choice.lower() == "y":
            filename = input("Enter filename: ")
            export_to_csv(filename, times, concentrations)

    except ValueError as error:
        print(f"Error: {error}")


def compare_two_reactions():
    """
    Allows the user to simulate and compare two reactions on one graph.
    """

    results = []

    try:
        for number in range(1, 3):
            print(f"\n--- Reaction {number} ---")

            reaction = create_reaction_from_user()

            total_time = get_float_input("Enter total simulation time in seconds: ")
            time_step = get_float_input("Enter time step in seconds: ")

            simulator = Simulator(reaction, total_time, time_step)
            times, concentrations, rates = simulator.run_simulation()

            results.append({
                "name": reaction.reaction_name,
                "times": times,
                "concentrations": concentrations
            })

        plotter = Plotter()
        plotter.plot_comparison(results)

    except ValueError as error:
        print(f"Error: {error}")


def compare_reaction_orders():
    """
    Shows what the concentration-time graph would look like for
    zero-order, first-order and second-order reactions.

    The same numerical value of k is used so that the graph shapes can be
    compared easily. In real chemistry, the units of k are different for
    different reaction orders, but this comparison is still useful visually.
    """

    try:
        print("\nReaction order graph comparison")
        print("-------------------------------")
        print("This compares 0th, 1st and 2nd order graphs using the same starting values.")

        rate_constant = get_float_input("Enter a numerical value for k: ")
        initial_concentration = get_float_input(
            "Enter initial concentration in mol dm^-3: "
        )
        total_time = get_float_input("Enter total simulation time in seconds: ")
        time_step = get_float_input("Enter time step in seconds: ")

        results = []

        for order in [0, 1, 2]:
            reaction_name = f"Order {order}"

            reaction = Reaction(
                reaction_name,
                order,
                rate_constant,
                initial_concentration
            )

            simulator = Simulator(reaction, total_time, time_step)
            times, concentrations, rates = simulator.run_simulation()

            results.append({
                "name": reaction_name,
                "times": times,
                "concentrations": concentrations
            })

        plotter = Plotter()
        plotter.plot_order_comparison(results)

    except ValueError as error:
        print(f"Error: {error}")


def print_about_project():
    """
    Prints a short explanation of the chemistry behind the program.
    """

    print("\nAbout this project")
    print("------------------")
    print("This program simulates simple chemical reaction kinetics.")
    print("For a zero-order reaction, the rate is constant and does not depend on [A].")
    print("For a first-order reaction, the rate depends on [A].")
    print("For a second-order reaction, the rate depends on [A]^2.")
    print("Euler's method is used to estimate how concentration changes over time.")
    print("The Arrhenius equation can also be used to estimate k from temperature.")


def main_menu():
    """
    Main menu loop.
    """

    while True:
        print("\nReaction Kinetics Simulator")
        print("---------------------------")
        print("1 - Run one reaction simulation")
        print("2 - Compare two reactions")
        print("3 - Compare 0th, 1st and 2nd order graph shapes")
        print("4 - About this project")
        print("5 - Exit")

        choice = get_int_input("Enter choice: ")

        if choice == 1:
            run_one_simulation()

        elif choice == 2:
            compare_two_reactions()

        elif choice == 3:
            compare_reaction_orders()

        elif choice == 4:
            print_about_project()

        elif choice == 5:
            print("Goodbye.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
