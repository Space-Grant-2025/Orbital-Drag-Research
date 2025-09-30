from year_mass_reentry_setup import *
from csv import reader
from f10_data import *
import datetime
import os

# doesn't use satellite list methods
def plot_f10_starlink_reentries_time(start_date, end_date):
    # get reentries
    reentry_list = []
    with open('../data/epoch_masterlist.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            if row[5] != '':
                reentry_date = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                reentry_list.append(reentry_date)

    # get f10
    f10_dates, f10_values = get_data_from_f10_csv(start_date, end_date)

    fig, reentry_axis = plot.subplots(layout='constrained', figsize = (9, 4.8))
    f10_axis = reentry_axis.twinx()

    # xaxis and title
    plot.title("Starlink Reentries 01/01/2020 to 05/31/2025 and F10 Values", color = 'black')
    reentry_axis.set_xlabel('Date (MM/YY)', color = 'black')
    reentry_axis.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    reentry_axis.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    reentry_axis.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    # reentry axis
    reentry_axis.set_ylabel('Number of Reentries', color = 'black')
    reentry_axis.hist(reentry_list, bins=53, color = 'grey')

    f10_axis.set_ylabel("F10 Values", color='black')
    f10_axis.plot(f10_dates, f10_values, color='black')

    plot.savefig('../data/mass_graphs/f10_starlink_reentries_time.png', format='png')

def plot_stacked_reentries_time(start_year, end_year):
    other_list = get_not_starlink_list()
    starlink_list = get_starlink_list()

    other_nums, other_years = fill_year_dict_reentry_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_reentry_nums(starlink_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize = (9, 4.8))
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    ax.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    ax.bar(other_years, other_nums, bottom=starlink_nums, color='grey', label='Other')
    plot.title("Number of Satellite Reentries per Year")
    plot.legend()
    ax.set_ylabel("Number of Reentries")
    ax.set_xlabel("Year")
    plot.savefig("../data/mass_graphs/stacked_satellites_reentered.png", format='png')

def plot_stacked_launches_time(start_year, end_year):
    other_list = get_not_starlink_list()
    starlink_list = get_starlink_list()

    # fill dicts with launch data
    other_nums, other_years = fill_year_dict_launch_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_launch_nums(starlink_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    ax.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    ax.bar(other_years, other_nums, bottom=starlink_nums, color='grey', label='Other')
    plot.title("Number of Satellite Launches per Year")
    plot.legend()
    ax.set_ylabel("Number of Launches")
    ax.set_xlabel("Year")
    plot.savefig("../data/mass_graphs/stacked_satellites_launched.png", format='png')

def plot_stacked_satellites_in_space(start_year, end_year):
    other_list = get_not_starlink_list()
    starlink_list = get_starlink_list()

    # satellite dict
    other_nums, other_years = fill_year_dict_sat_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_sat_nums(starlink_list, start_year, end_year)


    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.figure(figsize = (9, 4.8))
    plot.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    plot.bar(other_years, other_nums, bottom = starlink_nums, color='grey', label='Other')
    plot.title("Number of Satellites in Space by Year")
    plot.legend()
    plot.ylabel("Number of Satellites")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/stacked_satellites_in_space.png', format='png')

def plot_stacked_mass_in_space(start_year, end_year):
    other_list = get_not_starlink_list()
    starlink_list = get_starlink_list()

    # satellite dict
    other_nums, other_years = fill_year_dict_mass(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_year_dict_mass(starlink_list, start_year, end_year)


    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.figure(figsize = (9, 4.8))
    plot.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    plot.bar(other_years, other_nums, bottom = starlink_nums, color='grey', label='Other')
    plot.title("Mass of Satellites in Space by Year")
    plot.legend()
    plot.ylabel("Mass (tonnes)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/stacked_mass_in_space.png', format='png')



if __name__ == '__main__':
    if not os.path.exists("../data/mass_graphs"):
        os.makedirs("../data/mass_graphs")

    #plot_f10_starlink_reentries_time(datetime.date(2020, 1, 1), datetime.date(2025, 5, 30))
    #plot_stacked_reentries_time(1957, 2025)
    #plot_stacked_launches_time(1957, 2025)
    #plot_stacked_satellites_in_space(1957, 2025)
    #plot_stacked_mass_in_space(1957, 2025)