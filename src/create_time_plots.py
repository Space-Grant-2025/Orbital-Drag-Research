import os
from csv import reader
from datetime import timedelta, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plot
from matplotlib.ticker import LinearLocator
import pandas as pd

class satellite_reentry:
    def __init__(self, id, row):
        self.id = id
        self.date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
        self.name = row[1]
        self.altitude = row[2]
        self.velocity = row[3]
        self.longitude = row[4]
        self.latitude = row[5]
        self.jb2008 = row[6]
        self.nrlmsise = row[7]
        self.local_time = row[8]



def gather_data_from_csv(id):
    # list of data points for one satellite
    satellite_list = []
    with open(f'../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)

        for row in csv_reader:
            satellite_instance = satellite_reentry(id, row)
            satellite_list.append(satellite_instance)

    return satellite_list

def get_reference_epoch(id):
    epoch_df = pd.read_csv('../data/epoch_masterlist.csv')
    target_row = epoch_df[epoch_df['NORAD ID'] == id]
    ref_alt = target_row["REFERENCE ALTITUDE EPOCH"].iloc[0]
    return datetime.strptime(ref_alt, "%Y-%m-%d %H:%M:%S%z")

def plot_altitude_time(satellite_list):
    # lists to plot
    altitude_list = []
    date_list = []

    satellite_id = satellite_list[0].id
    reference_epoch = get_reference_epoch(satellite_id)

    # gather data to plot
    for satellite_instance in satellite_list:
        date = satellite_instance.date
        interval = timedelta(days=14)
        # add to relevant dates to list
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                altitude_list.append(float(satellite_instance.altitude))
                date_list.append(satellite_instance.date)

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
    plot.savefig('../data/starlink_reentries_2020_2025/reentry_graphs/altitude_time/' + str(satellite_id) + '_altitude_time.png', format='png')
    plot.close()

def plot_jb2008_time(satellite_list):
    # lists to plot
    jb2008_list = []
    date_list = []

    reference_epoch = get_reference_epoch(satellite_list[0].id)

    # gather data to plot
    for satellite_instance in satellite_list:
        date = satellite_instance.date
        interval = timedelta(days=14)
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                jb2008_list.append(float(satellite_instance.jb2008))
                date_list.append(satellite_instance.date)

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%D'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # y axis (density)
    ax.yaxis.set_major_locator(LinearLocator(10))

    # plot data
    plot.plot(date_list, jb2008_list)
    plot.title("NORAD CAT ID " + str(satellite_list[0].id))
    plot.ylabel("JB2008 Density (Kg/M^3)")
    plot.xlabel("Date")
    plot.savefig('../data/starlink_reentries_2020_2025/reentry_graphs/jb2008_time/' + str(satellite_id) + '_jb2008_time.png', format='png')
    plot.close()

def plot_nrlmsise_time(satellite_list):
    # lists to plot
    nrlmsise_list = []
    date_list = []

    reference_epoch = get_reference_epoch(satellite_list[0].id)

    # gather data to plot
    for satellite_instance in satellite_list:
        date = satellite_instance.date
        interval = timedelta(days=14)
        if reference_epoch != "":
            if (reference_epoch - interval) <= date <= (reference_epoch + interval):
                nrlmsise_list.append(float(satellite_instance.nrlmsise))
                date_list.append(satellite_instance.date)

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
    plot.title("NORAD CAT ID " + str(satellite_list[0].id))
    plot.ylabel("NRLMSISE00 Density (Kg/M^3)")
    plot.xlabel("Date")
    plot.savefig('../data/starlink_reentries_2020_2025/reentry_graphs/nrlmsise_time/' + str(satellite_id) + '_nrlmsise_time.png', format='png')
    plot.close()

def plot_lifetime(satellite_list):
    # lists to plot
    altitude_list = []
    date_list = []

    satellite_id = satellite_list[0].id

    # gather data to plot
    for satellite_instance in satellite_list:
        altitude = float(satellite_instance.altitude)
        date = satellite_instance.date
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
    plot.savefig('../data/starlink_reentries_2020_2025/lifetime_profiles/' + str(satellite_id) + '_lifetime_profile.png', format='png')
    plot.close()

def run_altitude_time():
    if not os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/altitude_time/"):
        os.makedirs("../data/starlink_reentries_2020_2025/reentry_graphs/altitude_time/")

    with open('../data/starlink_reentries_list.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/altitude_time/" + str(id) + "_altitude_time.png"):
                continue

            print(f"{count}: {id}")
            plot_altitude_time(gather_data_from_csv(id))
            count += 1
    print("Finished altitude-time")

def run_jb2008_time():
    if not os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/jb2008_time/"):
        os.makedirs("../data/starlink_reentries_2020_2025/reentry_graphs/jb2008_time/")

    reentries_list = pd.read_csv("../data/starlink_reentries_list.txt")
    id_list = reentries_list["STARLINK REENTRIES 2020-01-01 to 2025-05-31"]

    # create plot for each id
    count = 1
    for id in id_list:
        id = int(id.strip())

        if os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/jb2008_time/" + str(id) + "_jb2008_time.png"):
            continue

        plot_jb2008_time(gather_data_from_csv(id))
        print(f"{count}: {id}")
        count += 1

    print("Finished JB2008-time")

def run_nrlmsise_time():
    if not os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/nrlmsise_time/"):
        os.makedirs("../data/starlink_reentries_2020_2025/reentry_graphs/nrlmsise_time/")


    reentries_list = pd.read_csv("../data/starlink_reentries_list.txt")
    id_list = reentries_list["STARLINK REENTRIES 2020-01-01 to 2025-05-31"]

    # create plot for each id
    count = 1
    for id in id_list:
        id = int(id.strip())

        if os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs/nrlmsise_time/" + str(id) + "_nrlmsise_time.png"):
            continue

        plot_nrlmsise_time(gather_data_from_csv(id))
        print(f"{count}: {id}")
        count += 1

    print("Finished NRLMSISE00-time")

def run_lifetime():
    if not os.path.exists("../data/starlink_reentries_2020_2025/lifetime_profiles/"):
        os.makedirs("../data/starlink_reentries_2020_2025/lifetime_profiles/")


    reentries_list = pd.read_csv("../data/starlink_reentries_list.txt")
    id_list = reentries_list["STARLINK REENTRIES 2020-01-01 to 2025-05-31"]

    # create plot for each id
    count = 1
    for id in id_list:
        id = id.strip()

        if os.path.exists("../data/starlink_reentries_2020_2025/lifetime_profiles/" + str(id) + "_lifetime_profile.png"):
            continue

        plot_lifetime(gather_data_from_csv(id))
        print(f"{count}: {id}")
        count += 1
    print("Finished lifetime profiles")


if __name__ == '__main__':
    if not os.path.exists("../data/starlink_reentries_2020_2025/reentry_graphs"):
        os.makedirs("../data/starlink_reentries_2020_2025/reentry_graphs")

    run_altitude_time()
    run_jb2008_time()
    run_nrlmsise_time()
    run_lifetime()
