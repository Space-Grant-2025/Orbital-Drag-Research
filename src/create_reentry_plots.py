import datetime
import sys
from csv import reader
from datetime import datetime
import matplotlib.pyplot as plot
from matplotlib import dates as mdates
from satellite_data import *
import re
import os

class satellite_mass:
    def __init__(self, id, name, version, mass, dry_mass):
        self.id = id
        self.name = name
        self.version = version
        self.mass = mass
        self.dry_mass = dry_mass

        # to be set by set_lifetimes()
        self.first_date = None
        self.last_date = None
        self.lifetime = None

# getters
def get_id(self):
    return self.id
def get_name(self):
    return self.name
def get_version(self):
    return self.version
def get_mass(self):
    return self.mass
def get_dry_mass(self):
    return self.dry_mass
def get_first_date(self):
    return self.first_date
def get_last_date(self):
    return self.last_date
def get_lifetime(self):
    return self.lifetime

# setters
def set_first_date(self, first_date):
    self.first_date = first_date
def set_last_date(self, last_date):
    self.last_date = last_date
def set_lifetime(self, lifetime):
    self.lifetime = lifetime

class f10:
    def __init__(self, date, value):
        self.date = date
        self.value = value

# getters
    def get_date(self):
        return self.date
    def get_value(self):
        return self.value

def gather_f10_data():
    f10_list = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 5, 31)

    with open('../data/SOLFSMY.TXT', 'r') as file:
        # pass over headers 4x
        for x in range (0, 4):
            next(file)

        for row in file:
            # get values
            whitespace = re.compile('\\s+')
            data = whitespace.split(row)
            year = data[1]
            day = data[2]

            f10_value = float(data[4])
            date = datetime.strptime(f"{year}-{day}", "%Y-%j")

            if start_date < date < end_date:
                # create object and add to list
                f10_object = f10(date, f10_value)
                f10_list.append(f10_object)
    return f10_list

def plot_f10_time(f10_list):
    dates_list = []
    values_list = []

    for f10 in f10_list:
        dates_list.append(f10.get_date())
        values_list.append(f10.get_value())

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    plot.plot(dates_list, values_list)
    plot.title("F10 Values by Time")
    plot.ylabel("F10")
    plot.xlabel("Date (MM/YY)")
    plot.show()

def plot_reentries_time():
    reentry_list = []
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            if row[5] != '':
                reentry_date = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                reentry_list.append(reentry_date)

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    # 53 months in 4 years and 5 months
    plot.hist(reentry_list, bins=53)
    plot.title("Starlink Reentries 01/01/2020 to 05/31/2025")
    plot.ylabel("Number of Reentries")
    plot.xlabel("Date (MM/YY)")
    plot.show()

def plot_f10_reentries_time(f10_list):
    # get reentries
    reentry_list = []
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            if row[5] != '':
                reentry_date = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                reentry_list.append(reentry_date)

    # get f10
    dates_list = []
    values_list = []
    for f10 in f10_list:
        dates_list.append(f10.get_date())
        values_list.append(f10.get_value())

    fig, reentry_axis = plot.subplots(layout='constrained')
    f10_axis = reentry_axis.twinx()

    # xaxis and title
    plot.title("Starlink Reentries 01/01/2020 to 05/31/2025 and F10 Values", color = 'black')
    reentry_axis.set_xlabel('Date (MM/YY)', color = 'black')
    reentry_axis.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    reentry_axis.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    reentry_axis.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

    # reentry axis
    reentry_axis.set_ylabel('Number of Reentries', color = 'black')
    reentry_axis.hist(reentry_list, bins=53, color = 'gray')

    f10_axis.set_ylabel("F10 Values", color = 'black')
    f10_axis.plot(dates_list, values_list, color = 'black')

    plot.savefig('../data/graphs/f10_reentries_time.png', format='png')
    print("Plotted F10-reentries-time")

# returns first_date, last_date, lifetime
def find_lifetime(id):
    with open(f'../data/human_readable/tle_{id}.csv', 'r') as file:
        # pass over headers
        file.readline()

        # get first line
        first_line = file.readline()
        first_date = datetime.strptime(first_line.split(",")[0], "%Y-%m-%d %H:%M:%S%z")

        # get last line
        last_line = file.readlines()[-1]
        last_date = datetime.strptime(last_line.split(",")[0], "%Y-%m-%d %H:%M:%S%z")

    lifetime = last_date - first_date
    return first_date, last_date, lifetime

def set_lifetimes(satellite_list):
    new_list = []
    for satellite in satellite_list:
        satellite_id = int(get_id(satellite))
        first_date, last_date, lifetime = find_lifetime(satellite_id)
        set_first_date(satellite, first_date)
        set_last_date(satellite, last_date)
        set_lifetime(satellite, lifetime)
        new_list.append(satellite)
    return new_list

def get_mass_data():
    satellite_list = []
    with open('../data/starlink_masses.csv', 'r') as mass_file:
        csv_reader = reader(mass_file)
        # pass over headers
        next(csv_reader)

        # create satellite object for every row in starlink_masses
        for row in csv_reader:
            id = row[0]
            name = row[1]
            version = row[2]
            mass = row[3]
            dry_mass = row[4]
            satellite = satellite_mass(id, name, version, mass, dry_mass)

            # check if satellite appears in masterlist
            with open('../data/reentry_ids_masterlist.txt', 'r') as masterlist:
                for line in masterlist:
                    id = line.strip()
                    if get_id(satellite) == id:
                        # add satellite to list
                        satellite_list.append(satellite)
    return satellite_list

def plot_mass_reentry(satellite_list):
    mass_list = []
    for satellite in satellite_list:
        mass_list.append(get_dry_mass(satellite))

    mass_list.sort()
    fig, ax = plot.subplots(layout='constrained')
    plot.hist(mass_list)
    plot.title("Number of Reentries by Dry Mass")
    plot.ylabel("Number of Reentries")
    plot.xlabel("Mass (kg)")
    plot.show()

def plot_mass_lifetime(satellite_list):
    mass_data_list = []
    for satellite in satellite_list:
        mass = get_mass(satellite)
        lifetime = get_lifetime(satellite)
        data_point = (mass, lifetime)
        mass_data_list.append(data_point)

    mass_list = []
    lifetime_list = []
    for mass_data in mass_data_list:
        mass = int(mass_data[0])
        lifetime = mass_data[1]
        mass_list.append(mass)
        lifetime_list.append(int(lifetime.days))

    fig, ax = plot.subplots(layout='constrained')
    plot.scatter(mass_list, lifetime_list, s =1)
    plot.title("Satellite Lifetime by Dry Mass")
    plot.ylabel("Days in Orbit (From First TLE to Last TLE)")
    plot.xlabel("Mass (kg)")
    plot.show()


if __name__ == '__main__':
    if not os.path.exists("../data/graphs/"):
        os.makedirs("../data/graphs/")

    # plot_f10_reentries_time(gather_f10_data())

    satellite_list = set_lifetimes(get_mass_data())
    #plot_mass_reentry(satellite_list)
    plot_mass_lifetime(satellite_list)