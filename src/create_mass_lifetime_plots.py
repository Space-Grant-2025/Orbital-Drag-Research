import os
import matplotlib
from create_mass_reentry_plots import *
from get_satellite_masses_file import *
from csv import reader
from colormaps import *

# TODO: all satellite reentry lifetime altitude color bar starlink squares, other circles
def plot_altitude_mass_lifetime(start_year, end_year):
    with open("../data/all_satellite_info.csv", 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        starlink_mass_list = []
        starlink_lifetime_list = []
        starlink_altitude_list = []

        other_mass_list = []
        other_lifetime_list = []
        other_altitude_list = []

        for row in csv_reader:
            # check mean alt to make sure satellite is leo
            if row[5] != 'None' and float(row[5]) <= 1000:
                launch_date = datetime.datetime.strptime(row[2], "%Y-%m-%d")
                reentry_date = datetime.datetime.strptime(row[3], "%Y-%m-%d")

                lifetime = (reentry_date - launch_date).days / 365
                mass = float(row[4])
                altitude = float(row[5])
                # check if starlink
                if "STARLINK" in row[1]:
                    starlink_mass_list.append(mass)
                    starlink_lifetime_list.append(lifetime)
                    starlink_altitude_list.append(altitude)
                else:
                    other_mass_list.append(mass)
                    other_lifetime_list.append(lifetime)
                    other_altitude_list.append(altitude)


    fig, ax = plot.subplots(figsize = (9, 4.8), layout='constrained')

    norm = matplotlib.colors.Normalize(vmin=100, vmax=800)
    cmap = idl39
    fig.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical', label='Altitude (km)')

    plot.scatter(other_mass_list, other_lifetime_list, s = 20, c = other_altitude_list, cmap = cmap, norm = norm, marker = '.')
    plot.scatter(starlink_mass_list, starlink_lifetime_list, s = 20, c = starlink_altitude_list, cmap = cmap, norm = norm, marker = 'x')

    plot.title("Reentered LEO Satellite Lifetime by Dry Mass and Altitude")
    plot.ylabel("Years in Orbit")
    plot.xlabel("Mass (kg)")
    plot.xscale('log')
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    plot.savefig('../data/lifetime_graphs/altitude_mass_lifetime.png', format='png')

# outdated
'''# lifetime of satellites by mass
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
    plot.savefig('../data/lifetime_graphs/prelim_altitude_mass_lifetime.png', format='png')'''

if __name__ == '__main__':
    if not os.path.exists("../data/lifetime_graphs/"):
        os.makedirs("../data/lifetime_graphs/")

    #plot_prelim_altitude_mass_lifetime(1957, 2025)
    plot_altitude_mass_lifetime(1957, 2025)