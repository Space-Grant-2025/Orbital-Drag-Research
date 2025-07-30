from csv import reader
from matplotlib import pyplot as plot
import datetime
from f10_data import *
from matplotlib.ticker import ScalarFormatter
from special_tools import *
from matplotlib import dates as mdates

class satellite_mass_lifetime:
    def __init__(self, id, name, launch_date, reentry_date, mass, orbit, lifetime):
        self.id = id
        self.name = name
        self.launch_date = launch_date
        self.reentry_date = reentry_date
        self.mass = mass
        self.orbit = orbit
        self.lifetime = lifetime

# TODO: increase lengths of x axes
# TODO: add legends

# getters
def get_id(self):
    return self.id
def get_name(self):
    return self.name
def get_launch_date(self):
    return self.launch_date
def get_reentry_date(self):
    return self.reentry_date
def get_mass(self):
    return self.mass
def get_orbit(self):
    return self.orbit
def get_lifetime(self):
    return self.lifetime

def make_sat_object(row):
    id = int(row[0])
    name = row[1]
    if row[2] != "None":
        launch_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
    else:
        launch_date = None
    if row[3] != "None":
        reentry_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
    else:
        reentry_date = None
    if row[4] != "None":
        mass = float(row[4])
    else:
        mass = None

    if row[5] == "-":
        orbit = None
    elif row[5] == "CLO" or row[5] == "DSO" or row[5] == "EEO" or row[5] == "HEO" or row[5] == "VHEO":
        orbit = "HEO"
    elif "GEO" in row[5]:
        orbit = "MEO"
    elif row[5] == "GTO" or row[5] == "MEO":
        orbit = "MEO"
    elif "LEO" in row[5]:
        orbit = "LEO"
    else:
        orbit = None

    if launch_date is not None and reentry_date is not None:
        lifetime = reentry_date - launch_date
    if launch_date is not None and reentry_date is None:
        lifetime = datetime.date.today() - launch_date
    else:
        lifetime = None

    satellite = satellite_mass_lifetime(id, name, launch_date, reentry_date, mass, orbit, lifetime)
    return satellite

def get_satellite_list(start_year, end_year):
    satellite_list = []
    with open("../data/satellite_masses_list.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = make_sat_object(row)
            # make sure within year specification
            if get_launch_date(satellite) is not None:
                if start_year <= get_launch_date(satellite).year <= end_year:
                    satellite_list.append(satellite)

    return satellite_list

def get_starlink_list(start_year, end_year):
    satellite_list = []
    with open("../data/satellite_masses_list.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = make_sat_object(row)
            # make sure within year specification
            if get_launch_date(satellite) is not None:
                if start_year <= get_launch_date(satellite).year <= end_year:
                    # check satellite is starlink
                    if "STARLINK" in get_name(satellite):
                        satellite_list.append(satellite)
    return satellite_list

def get_not_starlink_list(start_year, end_year):
    satellite_list = []
    with open("../data/satellite_masses_list.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = make_sat_object(row)
            # make sure within year specification
            if get_launch_date(satellite) is not None:
                if start_year <= get_launch_date(satellite).year <= end_year:
                    # check satellite is not starlink
                    if "STARLINK" not in get_name(satellite):
                        satellite_list.append(satellite)
    return satellite_list

def get_year_dict(start_year, end_year):
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)
    year_nums = dict()
    for year in year_list:
        year_nums[year] = 0
    return year_nums

# fills with lifetime
def fill_dict_sat_nums(satellite_list, start_year, end_year):
    year_nums = get_year_dict(start_year, end_year)

    for satellite in satellite_list:
        if get_launch_date(satellite) is not None:
            launch_year = int(get_launch_date(satellite).year)
            # if no reentry, assume satellite is still orbiting
            if get_reentry_date(satellite) is None or get_reentry_date(satellite).year > end_year:
                reentry_year = end_year
            else:
                reentry_year = int(get_reentry_date(satellite).year)

            for x in range(reentry_year - launch_year + 1):
                year_nums[launch_year + x] += 1

    sat_nums = year_nums.values()
    sat_years = year_nums.keys()
    return sat_nums, sat_years

def fill_dict_launch_nums(satellite_list, start_year, end_year):
    year_nums = get_year_dict(start_year, end_year)

    # fill with num satellites
    for satellite in satellite_list:
        if get_launch_date(satellite) is not None:
            launch_year = int(get_launch_date(satellite).year)
            year_nums[launch_year] += 1

    nums_list = year_nums.values()
    year_list = year_nums.keys()

    return nums_list, year_list

# fills with lifetime
def fill_dict_mass_nums(satellite_list, start_year, end_year):
    year_masses = get_year_dict(start_year, end_year)

    # fill with mass
    for satellite in satellite_list:
        if get_mass(satellite) is not None and get_launch_date(satellite) is not None:
            mass = get_mass(satellite) / 1_000_000
            launch_year = int(get_launch_date(satellite).year)
            # if no reentry, assume satellite is still orbiting
            if get_reentry_date(satellite) is None or get_reentry_date(satellite).year > end_year:
                reentry_year = end_year
            else:
                reentry_year = int(get_reentry_date(satellite).year)

            for x in range(reentry_year - launch_year + 1):
                year_masses[launch_year + x] += mass

    mass_list = year_masses.values()
    year_list = year_masses.keys()
    return mass_list, year_list

def plot_reentries_time():
    reentry_list = []
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            if row[5] != '':
                reentry_date = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                reentry_list.append(reentry_date)

    fig, ax = plot.subplots(layout='constrained', figsize = (9, 4.8))
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    # 53 months in 4 years and 5 months
    plot.hist(reentry_list, bins=53)
    plot.title("Starlink Reentries 01/01/2020 to 05/31/2025")
    plot.ylabel("Number of Reentries")
    plot.xlabel("Date (MM/YY)")
    plot.savefig("../data/reentry_graphs/reentries_time.png")

def plot_f10_starlink_reentries_time(start_date, end_date):
    # get reentries
    reentry_list = []
    with open('../data/epochs.csv', 'r') as file:
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

    f10_axis.set_ylabel("F10 Values", color = 'black')
    f10_axis.plot(f10_dates, f10_values, color = 'black')

    plot.savefig('../data/reentered_starlinks/reentry_graphs/f10_starlink_reentries_time.png', format='png')

# satellites launched per year
def plot_launches_per_year(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)

    nums_list, year_list = fill_dict_launch_nums(satellite_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.bar(year_list, nums_list)
    plot.title("Number of Satellite Launches per Year")
    plot.ylabel("Number of Satellite Launches")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/satellites_launched.png', format='png')

def plot_stacked_launches_per_year(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    starlink_list = get_starlink_list(start_year, end_year)

    # fill dicts with kaunch data
    other_nums, other_years = fill_dict_launch_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_dict_launch_nums(starlink_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    ax.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    ax.bar(other_years, other_nums, bottom=starlink_nums, color='grey', label='Other')
    plot.title("Number of Satellite Launches per Year")
    plot.legend()
    ax.set_ylabel("Number of Launches")
    ax.set_xlabel("Year")
    plot.savefig("../data/mass_graphs/stacked_satellites_launched.png", format='png')

def plot_mass_launched_per_year(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)
    year_nums = get_year_dict(start_year, end_year)

    # fill with satellite masses
    for satellite in satellite_list:
        if get_launch_date(satellite) is not None and get_mass(satellite) is not None:
            launch_year = int(get_launch_date(satellite).year)
            year_nums[launch_year] += get_mass(satellite) / 1_000_000

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
    sat_nums, sat_years = fill_dict_sat_nums(satellite_list, start_year, end_year)

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
    other_nums, other_years = fill_dict_sat_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_dict_sat_nums(starlink_list, start_year, end_year)


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
    other_nums, other_years = fill_dict_sat_nums(other_list, start_year, end_year)
    starlink_nums, starlink_years = fill_dict_sat_nums(starlink_list, start_year, end_year)
    f10_values, f10_years = get_average_f10(start_year, end_year)

    fig, sat_axis = plot.subplots(layout='constrained', figsize = (9, 4.8))
    f10_axis = sat_axis.twinx()

    plot.title("Satellites in Space by Year and F10 Values")
    sat_axis.set_xlabel("Year")
    sat_axis.set_ylabel("Number of Satellites")

    sat_axis.bar(starlink_years, starlink_nums, color='blue', label='Starlinks')
    sat_axis.bar(other_years, other_nums, bottom = starlink_nums, color='grey', label='Other')
    sat_axis.legend()

    f10_axis.set_ylabel("F10 Values")
    f10_axis.scatter(f10_years, f10_values, color='black', s = 1)

    plot.savefig('../data/mass_graphs/stacked_satellites_in_space_f10.png', format='png')

# mass in space by year
def plot_mass_in_space(start_year, end_year):
    satellite_list = get_satellite_list(start_year, end_year)

    mass_list, year_list = fill_dict_mass_nums(satellite_list, start_year, end_year)

    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.bar(year_list, mass_list)
    plot.title("Mass in Space by Year")
    plot.ylabel("Mass (metric tonnes)")
    plot.xlabel("Year")
    plot.savefig('../data/mass_graphs/mass_in_space.png', format='png')

def plot_stacked_mass_in_space(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    starlink_list = get_starlink_list(start_year, end_year)

    other_mass, other_years = fill_dict_mass_nums(other_list, start_year, end_year)
    starlink_mass, starlink_years = fill_dict_mass_nums(starlink_list, start_year, end_year)


    fig, ax = plot.subplots(layout='constrained', figsize=(9, 4.8))
    plot.bar(starlink_years, starlink_mass, color='blue', label='Starlinks')
    plot.bar(other_years, other_mass, bottom=starlink_mass, color='grey', label='Other')
    plot.title("Mass in Space by Year")
    plot.legend()
    ax.set_ylabel("Mass (metric tonnes)")
    ax.set_xlabel("Year")
    plot.savefig('../data/mass_graphs/stacked_mass_in_space.png', format='png')

def plot_stacked_mass_in_space_f10(start_year, end_year):
    other_list = get_not_starlink_list(start_year, end_year)
    starlink_list = get_starlink_list(start_year, end_year)

    other_mass, other_years = fill_dict_mass_nums(other_list, start_year, end_year)
    starlink_mass, starlink_years = fill_dict_mass_nums(starlink_list, start_year, end_year)

    f10_values, f10_years = get_average_f10(start_year, end_year)


    fig, mass_axis = plot.subplots(layout='constrained', figsize=(9, 4.8))
    f10_axis = mass_axis.twinx()

    plot.title("Mass in Space by Year")
    mass_axis.set_ylabel("Mass (metric tonnes)")
    mass_axis.set_xlabel("Year")

    mass_axis.bar(starlink_years, starlink_mass, color='blue', label='Starlinks')
    mass_axis.bar(other_years, other_mass, bottom=starlink_mass, color='grey', label='Other')
    mass_axis.legend()

    f10_axis.set_ylabel("F10 Values")
    f10_axis.scatter(f10_years, f10_values, color='black', s = 1)

    plot.savefig('../data/mass_graphs/stacked_mass_in_space_f10.png', format='png')

if __name__ == '__main__':
    plot_f10_starlink_reentries_time(datetime.date(2020, 1, 1), datetime.date(2025, 5, 31))
    plot_stacked_launches_per_year(1957, 2025)
    plot_stacked_satellites_in_space_f10(1957, 2025)
    plot_stacked_mass_in_space_f10(1957, 2025)

