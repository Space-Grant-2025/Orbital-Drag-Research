from collections import Counter

from masses import *
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
    plot.savefig('../data/starlink_mass_lifetimes.png', format='png')

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
    plot.savefig('../data/mass_lifetimes.png', format='png')

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
    plot.savefig('../data/recent_mass_lifetimes.png', format='png')

# ask about reentry issue
def plot_all_launch_masses(satellite_list):
    start_year = 1957
    end_year = 2025

    # generate list of years to add masses to
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)

    # initialize dictionary
    year_masses = dict()
    for year in year_list:
        year_masses[year] = 0

    # fill with masses (just launch dates for now)
    for satellite in satellite_list:
        if get_dry_mass(satellite) is not None and get_launch_date(satellite) is not None:
            mass = get_dry_mass(satellite)
            launch_year = int(get_launch_date(satellite).year)
            #reentry_year = int(get_reentry_date(satellite).year)

            year_masses[launch_year] += mass

    mass_list = year_masses.values()

    fig, ax = plot.subplots(layout='constrained')
    plot.bar(year_list, mass_list)
    plot.title("Mass Launched by Year")
    plot.ylabel("Mass (kg)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_launched.png', format='png')

def get_mass_years(satellite_list, start_year, end_year):
    # generate list of years to add masses to
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)

    # initialize dictionary
    year_masses = dict()
    for year in year_list:
        year_masses[year] = 0

    # fill with masses
    for satellite in satellite_list:
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

    mass_list = year_masses.values()
    return mass_list, year_list

def get_mass_years_no_starlink(satellite_list, start_year, end_year):
    # generate list of years to add masses to
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)

    # initialize dictionary
    year_masses = dict()
    for year in year_list:
        year_masses[year] = 0

    # fill with masses
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

    mass_list = year_masses.values()
    return mass_list, year_list

def plot_all_existing_masses():
    mass_list, year_list = get_mass_years(get_satellite_list("all"), 1957, 2025)

    fig, ax = plot.subplots(layout='constrained')
    plot.bar(year_list, mass_list)
    plot.title("Mass in Space by Year")
    plot.ylabel("Mass (kg)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_in_space.png', format='png')

def plot_stacked_existing_masses_f10():
    all_mass_list, all_year_list = get_mass_years_no_starlink(get_satellite_list("all"), 1957, 2025)
    starlink_mass_list, starlink_year_list = get_mass_years(get_satellite_list("starlink"), 1957, 2025)

    fig, ax = plot.subplots(layout='constrained')
    plot.bar(starlink_year_list, starlink_mass_list, color='red')
    plot.bar(all_year_list, all_mass_list, bottom=starlink_mass_list, color='grey')
    plot.title("Mass in Space by Year")
    plot.ylabel("Mass (kg)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_in_space_stacked.png', format='png')

if __name__ == '__main__':
    plot_starlink_mass_lifetime(get_satellite_list("starlink"))
    plot_all_mass_lifetime(get_satellite_list("all"))
    plot_all_recent_mass_lifetime(get_satellite_list("all"))
    plot_all_launch_masses(get_satellite_list("all"))
    plot_all_existing_masses()
    plot_stacked_existing_masses()