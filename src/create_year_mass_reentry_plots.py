from csv import reader
from matplotlib import pyplot as plot
import datetime
from f10_data import *
from matplotlib.ticker import ScalarFormatter
from special_tools import *
from matplotlib import dates as mdates


# satellites launched per year
def plot_launches_per_year(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)

    nums_list, year_list = fill_year_dict_launch_nums(satellite_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.bar(year_list, nums_list)
    plot.title("Number of Satellite Launches per Year")
    plot.ylabel("Number of Satellite Launches")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/satellites_launched.png', format='png')



def plot_mass_launched_per_year(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)
    year_nums = get_year_dict(start_year, end_year)

    # fill with satellite masses
    for satellite in satellite_list:
        if satellite.get_launch_date() is not None and satellite.get_launch_date() is not None:
            launch_year = int(satellite.get_launch_date().year)
            year_nums[launch_year] += satellite.get_mass() / 1_000_000

    mass_list = year_nums.values()
    year_list = year_nums.keys()

    fig, ax = plot.subplots(layout='constrained', figsize = (9, 4.8))
    plot.bar(year_list, mass_list)
    plot.title("Mass of Satellite Launches per Year")
    plot.ylabel("Mass (metric tonnes)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/satellite_mass_launched.png', format='png')

def plot_satellites_in_space(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)
    sat_nums, sat_years = fill_year_dict_sat_nums(satellite_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.figure(figsize = (9, 4.8))
    plot.bar(sat_years, sat_nums, color='blue')
    plot.title("Satellites in Space by Year")
    plot.ylabel("Number of Satellites")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/satellites_in_space.png', format='png')

def plot_stacked_satellites_in_space(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    starlink_list = get_starlink_list(start_year, end_year)

    # satellite dict
    other_nums, other_years = fill_year_dict_sat_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_sat_nums(starlink_list, start_year, end_year)


    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.figure(figsize = (9, 4.8))
    plot.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    plot.bar(other_years, other_nums, bottom = starlink_nums, color='grey', label='Other')
    plot.title("Satellites in Space by Year")
    plot.legend()
    plot.ylabel("Number of Satellites")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/stacked_satellites_in_space.png', format='png')

def plot_stacked_satellites_in_space_f10(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    starlink_list = get_starlink_list(start_year, end_year)

    # get plot dict
    other_nums, other_years = fill_year_dict_sat_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_sat_nums(starlink_list, start_year, end_year)
    f10_values, f10_years = get_average_f10(start_year, end_year)

    fig, sat_axis = plot.subplots(layout='constrained', figsize = (9, 4.8))
    f10_axis = sat_axis.twinx()

    plot.title("Satellites in Space by Month and F10 Values")
    sat_axis.set_xlabel("Year")
    sat_axis.set_ylabel("Number of Satellites")

    sat_axis.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    sat_axis.bar(other_years, other_nums, bottom = starlink_nums, color='grey', label='Other')
    sat_axis.legend()

    f10_axis.set_ylabel("F10 Values")
    f10_axis.scatter(f10_years, f10_values, color='black', s = 1)

    plot.savefig('../data/mass_graphs/stacked_satellites_in_space_f10.png', format='png')


if __name__ == '__main__':
    plot_stacked_launches_per_year(1957, 2025)
    plot_stacked_satellites_in_space(1957, 2025)
    plot_stacked_satellites_in_space_f10(1957, 2025)
    plot_stacked_mass_in_space(1957, 2025)
    plot_stacked_mass_in_space_f10(1957, 2025)
    plot_f10_starlink_reentries_time(datetime.date(2020, 1, 1), datetime.date(2025, 5, 31))
    plot_stacked_reentries_time(1957, 2025)
    plot_mass_launched_per_year(1957, 2025)


