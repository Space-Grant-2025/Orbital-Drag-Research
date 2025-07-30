import os
from csv import reader
from datetime import timedelta, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plot
from matplotlib.ticker import LinearLocator

class satellite_reentry:
    def __init__(self, id, date, name, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time):
        self.id = id
        self.date = date
        self.name = name
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
def get_name(self):
    return self.name
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

def gather_data_from_csv(id):
    # list of data points for one satellite
    satellite_list = []
    with open(f'../data/human_readable/tle_{id}.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)
        for row in csv_reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            name = row[1]
            altitude = row[2]
            velocity = row[3]
            longitude = row[4]
            latitude = row[5]
            jb2008 = row[6]
            nrlmsise = row[7]
            local_time = row[8]

            satellite_instance = satellite_reentry(id, date, name, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time)
            satellite_list.append(satellite_instance)
    return satellite_list

def get_reference_epoch(id):
    reference_epoch = ""
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        # grab reference epoch
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == id:
                if row[1] is not None:
                    reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")
    return reference_epoch

def plot_altitude_time(satellite_list):
    # lists to plot
    altitude_list = []
    date_list = []

    satellite_id = get_id(satellite_list[0])

    reference_epoch = get_reference_epoch(satellite_id)

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days=14)
        # add to relevant dates to list
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                altitude_list.append(float(get_altitude(satellite_instance)))
                date_list.append(get_date(satellite_instance))

    # plot data
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
    plot.title("NORAD CAT ID " + str(satellite_id))
    plot.ylabel("Altitude (km)")
    plot.xlabel("Date")
    plot.savefig('../data/reentry_graphs/altitude_time/' + str(satellite_id) + '_altitude_time.png', format='png')
    plot.close()

def plot_jb2008_time(satellite_list):
    # lists to plot
    jb2008_list = []
    date_list = []

    reference_epoch = ""
    satellite_id = get_id(satellite_list[0])
    # find reference epoch for satellite
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        # grab reference epoch
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == satellite_id:
                if row[1] is not None:
                    reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days=14)
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                jb2008_list.append(float(get_jb2008(satellite_instance)))
                date_list.append(get_date(satellite_instance))

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # y axis (density)
    ax.yaxis.set_major_locator(LinearLocator(10))

    # plot data
    plot.plot(date_list, jb2008_list)
    plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
    plot.ylabel("JB2008 Density (Kg/M^3)")
    plot.xlabel("Date")
    plot.savefig('../data/reentry_graphs/jb2008_time/' + str(satellite_id) + '_jb2008_time.png', format='png')
    plot.close()

def plot_nrlmsise_time(satellite_list):
    # lists to plot
    nrlmsise_list = []
    date_list = []

    reference_epoch = ""
    satellite_id = get_id(satellite_list[0])
    # find reference epoch for satellite
    with open('../data/epochs.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        # grab reference epoch
        for row in csv_reader:
            epoch_id = int(row[0])
            if epoch_id == satellite_id:
                if row[1] is not None:
                    reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

    # gather data to plot
    for satellite_instance in satellite_list:
        date = get_date(satellite_instance)
        interval = timedelta(days=14)
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                nrlmsise_list.append(float(get_nrlmsise(satellite_instance)))
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
    plot.plot(date_list, nrlmsise_list)
    plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
    plot.ylabel("NRLMSISE00 Density (Kg/M^3)")
    plot.xlabel("Date")
    plot.savefig('../data/reentry_graphs/nrlmsise_time/' + str(satellite_id) + '_nrlmsise_time.png', format='png')
    plot.close()

def plot_lifetime(satellite_list):
    # lists to plot
    altitude_list = []
    date_list = []

    satellite_id = get_id(satellite_list[0])

    # gather data to plot
    for satellite_instance in satellite_list:
        altitude = float(get_altitude(satellite_instance))
        date = get_date(satellite_instance)
        altitude_list.append(altitude)
        date_list.append(date)

    # plot data
    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))

    # y axis (density)
    #ax.yaxis.set_major_locator(LinearLocator(10))
    # ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False))

    # plot data
    plot.plot(date_list, altitude_list)
    plot.title("NORAD CAT ID " + str(satellite_id))
    plot.ylabel("Altitude (km)")
    plot.xlabel("Date (YY-MM)")
    plot.savefig('../data/lifetime_profiles/' + str(satellite_id) + '_lifetime_profile.png', format='png')
    plot.close()

def run_altitude_time():
    if not os.path.exists("../data/reentry_graphs/altitude_time/"):
        os.makedirs("../data/reentry_graphs/altitude_time/")

    with open('../data/starlink_reentries_list.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/reentry_graphs/altitude_time/" + str(id) + "_altitude_time.png"):
                continue

            plot_altitude_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1
    print("Finished altitude-time")

def run_jb2008_time():
    if not os.path.exists("../data/reentry_graphs/jb2008_time/"):
        os.makedirs("../data/reentry_graphs/jb2008_time/")

    with open('../data/starlink_reentries_list.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/reentry_graphs/jb2008_time/" + str(id) + "_jb2008_time.png"):
                continue

            plot_jb2008_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1

    print("Finished JB2008-time")

def run_nrlmsise_time():
    if not os.path.exists("../data/reentry_graphs/nrlmsise_time/"):
        os.makedirs("../data/reentry_graphs/nrlmsise_time/")

    with open('../data/starlink_reentries_list.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/reentry_graphs/nrlmsise_time/" + str(id) + "_nrlmsise_time.png"):
                continue

            plot_nrlmsise_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1

    print("Finished NRLMSISE00-time")

def run_lifetime():

    with open('../data/starlink_reentries_list.txt', 'r') as list:

        # pass over headers
        next(list)
        # count of satellites
        count = 1

        # create plot for each id
        for id in list:
            id = id.strip()

            if os.path.exists("../data/lifetime_profiles/" + str(id) + "_lifetime_profile.png"):
                continue

            plot_lifetime(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1
    print("Finished lifetime profiles")


if __name__ == '__main__':
    if not os.path.exists("../data/reentry_graphs/"):
        os.makedirs("../data/reentry_graphs/")
    if not os.path.exists("../data/lifetime_profiles/"):
        os.makedirs("../data/lifetime_profiles/")

    run_altitude_time()
    run_jb2008_time()
    run_nrlmsise_time()
    run_lifetime()
