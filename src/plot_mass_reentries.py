from satellite_classes import *
from matplotlib import pyplot as plot

def plot_starlink_mass_reentry(satellite_list):
    mass_list = []
    for satellite in satellite_list:
        if get_mass(satellite) is not None:
            mass_list.append(get_dry_mass(satellite))

    fig, ax = plot.subplots(layout='constrained')
    plot.hist(mass_list)
    plot.title("Number of Starlink Reentries by Dry Mass")
    plot.ylabel("Number of Reentries")
    plot.xlabel("Mass (kg)")
    plot.savefig('../data/starlink_mass_reentries.png', format='png')

def plot_all_mass_reentry(satellite_list):
    mass_limit = 5000
    mass_list = []
    for satellite in satellite_list:
        if get_dry_mass(satellite) is not None:
            if get_dry_mass(satellite) < mass_limit:
                mass_list.append(get_dry_mass(satellite))

    fig, ax = plot.subplots(layout='constrained')
    plot.hist(mass_list, bins = int(mass_limit / 50))
    plot.title("Number of Reentries by Dry Mass")
    plot.ylabel("Number of Reentries")
    plot.xlabel("Mass (kg)")
    plot.savefig('../data/mass_reentries.png', format='png')

if __name__ == '__main__':
    plot_starlink_mass_reentry(get_satellite_list("starlink"))
    plot_all_mass_reentry(get_satellite_list("all"))