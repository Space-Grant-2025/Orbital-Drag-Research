import os
from collections import Counter

from satellite_classes import *
from matplotlib import pyplot as plot
from datetime import date

recent_launch_date = date(2000, 1, 1)

def plot_starlink_mass_lifetime(satellite_list):
    mass_list = []
    lifetime_list = []
    for satellite in satellite_list:
        mass = get_mass(satellite)
        lifetime = get_lifetime(satellite)
        if lifetime is not None and mass is not None:
            if mass > 0:
                mass_list.append(mass)
                lifetime_list.append(lifetime.days)

    fig, ax = plot.subplots(layout='constrained')
    plot.scatter(mass_list, lifetime_list, s = 1)
    plot.title("Starlink Satellite Lifetime by Dry Mass")
    plot.ylabel("Days in Orbit")
    plot.xlabel("Mass (kg)")
    plot.savefig('../data/mass_graphs/starlink_mass_lifetimes.png', format='png')

def plot_all_mass_lifetime(satellite_list):
    mass_list = []
    lifetime_list = []
    for satellite in satellite_list:
        mass = get_mass(satellite)
        lifetime = get_lifetime(satellite)
        if lifetime is not None and mass is not None:
            if mass > 0:
                mass_list.append(mass)
                lifetime_list.append(lifetime.days)

    fig, ax = plot.subplots(layout='constrained')
    plot.scatter(mass_list, lifetime_list, s = 1)
    plot.title("Satellite Lifetime by Dry Mass")
    plot.ylabel("Days in Orbit")
    plot.xlabel("Mass (kg)")
    plot.savefig('../data/mass_graphs/mass_lifetimes.png', format='png')

def plot_all_recent_mass_lifetime(satellite_list):
    mass_list = []
    lifetime_list = []
    for satellite in satellite_list:
        mass = get_mass(satellite)
        lifetime = get_lifetime(satellite)
        if lifetime is not None and mass is not None:
            if mass > 0:
                if get_launch_date(satellite) > recent_launch_date:
                    mass_list.append(mass)
                    lifetime_list.append(lifetime.days)

    fig, ax = plot.subplots(layout='constrained')
    plot.scatter(mass_list, lifetime_list, s = 1)
    plot.title("Satellite Lifetime by Dry Mass")
    plot.ylabel("Days in Orbit")
    plot.xlabel("Mass (kg)")
    plot.savefig('../data/mass_graphs/recent_mass_lifetimes.png', format='png')


def get_mass_years(satellite_list, start_year, end_year):
    # generate list of years to add mass_graphs to
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)

    # initialize dictionary
    year_masses = dict()
    for year in year_list:
        year_masses[year] = 0

    # fill with mass_graphs
    for satellite in satellite_list:
        if get_dry_mass(satellite) is not None and get_launch_date(satellite) is not None:
            mass = get_dry_mass(satellite)
            launch_year = int(get_launch_date(satellite).year)
            if get_reentry_date(satellite) is None:
                reentry_year = end_year
            else:
                reentry_year = int(get_reentry_date(satellite).year)

            for x in range(reentry_year - launch_year + 1):
                year_masses[launch_year + x] += mass

    mass_list = year_masses.values()
    return mass_list, year_list

def get_mass_years_no_starlink(satellite_list, start_year, end_year):
    # generate list of years to add mass_graphs to
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)

    # initialize dictionary
    year_masses = dict()
    for year in year_list:
        year_masses[year] = 0

    # fill with mass_graphs
    count = 0
    for satellite in satellite_list:
        if not "Starlink" in get_name(satellite):
            if get_dry_mass(satellite) is not None and get_launch_date(satellite) is not None:
                mass = get_dry_mass(satellite)
                launch_year = int(get_launch_date(satellite).year)
                if get_reentry_date(satellite) is None:
                    reentry_year = end_year
                    print(launch_year)
                else:
                    reentry_year = int(get_reentry_date(satellite).year)

                for x in range(reentry_year - launch_year + 1):
                    year_masses[launch_year + x] += mass
        else:
            count += 1

    mass_list = year_masses.values()
    print(count)
    return mass_list, year_list

def plot_all_existing_masses():
    mass_list, year_list = get_mass_years(get_satellite_list("all"), 1957, 2025)

    fig, ax = plot.subplots(layout='constrained')
    plot.bar(year_list, mass_list)
    plot.title("Mass in Space by Year")
    plot.ylabel("Mass (kg)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/mass_in_space.png', format='png')

def plot_stacked_existing_masses_f10(f10_list):
    all_mass_list, all_year_list = get_mass_years_no_starlink(get_satellite_list("all"), 1957, 2025)
    starlink_mass_list, starlink_year_list = get_mass_years(get_satellite_list("starlink"), 1957, 2025)

    # get f10
    dates_list = []
    values_list = []
    for f10 in f10_list:
        dates_list.append(f10.get_date())
        values_list.append(f10.get_value())

    fig, mass_axis = plot.subplots(layout='constrained')
    f10_axis = mass_axis.twinx()

    # plot title and mass axis
    mass_axis.bar(starlink_year_list, starlink_mass_list, color='red')
    mass_axis.bar(all_year_list, all_mass_list, bottom=starlink_mass_list, color='grey')
    plot.title("Mass in Space by Year")
    mass_axis.set_ylabel("Mass (kg)")
    mass_axis.set_xlabel("Year")

    # f10 axis
    f10_axis.set_ylabel("F10 Values", color='black')
    f10_axis.plot(dates_list, values_list, color='black')

    plot.show()

if __name__ == '__main__':
    if not os.path.exists("../data/mass_graphs"):
        os.makedirs("../data/mass_graphs")

    '''plot_starlink_mass_lifetime(get_satellite_list("starlink"))
    plot_all_mass_lifetime(get_satellite_list("all"))
    plot_all_recent_mass_lifetime(get_satellite_list("all"))
    plot_all_launch_masses(get_satellite_list("all"))
    plot_all_existing_masses()'''

    #plot_stacked_existing_masses_f10(gather_f10_data(datetime.date(1957, 1, 1), datetime.date(2025, 5, 31)))