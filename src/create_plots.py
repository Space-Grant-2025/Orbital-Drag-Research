import re
from csv import reader
from datetime import timedelta, datetime

import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plot
from matplotlib.ticker import LinearLocator, ScalarFormatter

class satellite_data:
    def __init__(self, id, date, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time):
        self.id = id
        self.date = date
        self.altitude = altitude
        self.velocity = velocity
        self.longitude = longitude
        self.latitude = latitude
        self.jb2008 = jb2008
        self.nrlmsise = nrlmsise
        self.local_time = local_time

# getters
def get_id(self):
    return self.id
def get_date(self):
    return self.date
def get_altitude(self):
    return self.altitude
def get_velocity(self):
    return self.velocity
def get_longitude(self):
    return self.longitude
def get_latitude(self):
    return self.latitude
def get_jb2008(self):
    return self.jb2008
def get_nrlmsise(self):
    return self.nrlmsise
def get_local_time(self):
    return self.local_time

class f10:
    def __init__(self, date, value):
        self.date = date
        self.value = value

# getters
    def get_date(self):
        return self.date
    def get_value(self):
        return self.value

def gather_data_from_csv(id):
    # list of data points for one satellite
    satellite_list = []
    with open('../data/human_readable/tle_' + str(id) + '.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)
        for row in csv_reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            altitude = row[1]
            velocity = row[2]
            longitude = row[3]
            latitude = row[4]
            jb2008 = row[5]
            nrlmsise = row[6]
            local_time = row[7]

            satellite_instance = satellite_data(id, date, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time)
            satellite_list.append(satellite_instance)
    return satellite_list

def gather_f10_data():
    f10_list = []
    start_date = datetime(2000, 1, 1)
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

def plot_altitude_time(satellite_list):
    # lists to plot
    altitude_list = []
    date_list = []

    satellite_id = get_id(satellite_list[0])
    # find reference epoch for satellite
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == satellite_id:
                reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days=14)
        if (reference_epoch - interval) <= date <= (reference_epoch + interval):
            altitude_list.append(get_altitude(satellite_instance))
            date_list.append(get_date(satellite_instance))

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # y axis (density)
    ax.yaxis.set_major_locator(LinearLocator(10))
    # ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # plot data
    plot.plot(date_list, altitude_list)
    plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
    plot.ylabel("Altitude (km)")
    plot.xlabel("Date")
    plot.show()

'''def plot_nrlmsise_time(satellite_list):
    # lists to plot
    nrlmsise00_list = []
    date_list = []

    satellite_id = get_id(satellite_list[0])
    # find reference epoch for satellite
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == satellite_id:
                reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days=14)
        if (reference_epoch - interval) <= date <= (reference_epoch + interval):
            nrlmsise00_list.append(get_nrlmsise(satellite_instance))
            date_list.append(get_date(satellite_instance))

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # y axis (density)
    ax.yaxis.set_major_locator(LinearLocator(10))
    # ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # plot data
    plot.plot(date_list, nrlmsise00_list)
    plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
    plot.ylabel("NRLMSISE00 Density (Kg/M^3")
    plot.xlabel("Date")
    plot.show()'''

def plot_jb2008_time(satellite_list):
    # lists to plot
    jb2008_list = []
    date_list = []

    satellite_id = get_id(satellite_list[0])
    # find reference epoch for satellite
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == satellite_id:
                reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days = 14)
        if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                jb2008_list.append(get_jb2008(satellite_instance))
                date_list.append(get_date(satellite_instance))

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # y axis (density)
    ax.yaxis.set_major_locator(LinearLocator(10))
    #ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # plot data
    plot.plot(date_list, jb2008_list)
    plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
    plot.ylabel("JB2008 Density (Kg/M^3)")
    plot.xlabel("Date")
    plot.show()

if __name__ == '__main__':
    '''with open('../data/reentry_ids_masterlist.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        for id in masterlist:
            id = id.strip()
            plot_density_altitude(gather_data_from_csv(id))'''
    #plot_altitude_time(gather_data_from_csv(44235))
    plot_reentries_time()
    #plot_f10_time(gather_f10_data())