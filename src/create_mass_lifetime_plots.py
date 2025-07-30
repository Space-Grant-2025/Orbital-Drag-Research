import os
from create_mass_reentry_plots import *
from get_satellite_masses_file import *
from csv import reader

# TODO: all satellite reentry lifetime altitude color bar starlink squares, other circles

# lifetime of satellites by mass
def plot_prelim_altitude_mass_lifetime(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    none_mass_list = []
    none_lifetime_list = []
    leo_mass_list = []
    leo_lifetime_list = []
    meo_mass_list = []
    meo_lifetime_list = []
    heo_mass_list = []
    heo_lifetime_list = []

    starlink_list = get_starlink_list(start_year, end_year)
    starlink_mass_list = []
    starlink_lifetime_list = []

    # starlink satellites
    for starlink in starlink_list:
        mass = get_mass(starlink)
        lifetime = get_lifetime(starlink)
        if lifetime is not None and mass is not None:
            starlink_mass_list.append(mass)
            starlink_lifetime_list.append(lifetime.days / 365)

    fig, ax = plot.subplots(layout='constrained')
    plot.figure(figsize = (9, 4.8))

    for other_sat in other_list:
        if get_mass(other_sat) is not None and get_lifetime(other_sat) is not None:

            mass = get_mass(other_sat)
            lifetime = get_lifetime(other_sat).days / 365
            orbit = get_orbit(other_sat)

            if orbit is None:
                none_mass_list.append(mass)
                none_lifetime_list.append(lifetime)
            elif orbit == "LEO":
                leo_mass_list.append(mass)
                leo_lifetime_list.append(lifetime)
            elif orbit == "MEO":
                meo_mass_list.append(mass)
                meo_lifetime_list.append(lifetime)
            elif orbit == "HEO":
                heo_mass_list.append(mass)
                heo_lifetime_list.append(lifetime)

    plot.scatter(starlink_mass_list, starlink_lifetime_list, s = 1, color='blue', label='Starlink')
    plot.scatter(leo_mass_list, leo_lifetime_list, s = 1, color='grey', label = "LEO")
    plot.scatter(meo_mass_list, meo_lifetime_list, s = 1, color='purple', label = "MEO")
    plot.scatter(heo_mass_list, heo_lifetime_list, s = 1, color='red', label = "HEO")
    plot.scatter(none_mass_list, none_lifetime_list, s = 1, color='black', label = "No Data")

    plot.legend()
    plot.title("Satellite Lifetime by Dry Mass")
    plot.ylabel("Years in Orbit")
    plot.xlabel("Mass (kg)")
    plot.xscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    plot.savefig('../data/lifetime_graphs/prelim_altitude_mass_lifetime.png', format='png')

# def plot_reentry_mass_lifetime(start_year, end_year):


if __name__ == '__main__':
    if not os.path.exists("../data/lifetime_graphs/"):
        os.makedirs("../data/lifetime_graphs/")

    plot_prelim_altitude_mass_lifetime(1957, 2025)