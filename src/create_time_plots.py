import os
from csv import reader
from datetime import timedelta, datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plot
from matplotlib.ticker import LinearLocator
from satellite_classes import *

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
                    reference_epoch = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")
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
    plot.savefig('../data/graphs/altitude_time/' + str(satellite_id) + '_altitude_time.png', format='png')
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
                    reference_epoch = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

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
    plot.savefig('../data/graphs/jb2008_time/' + str(satellite_id) + '_jb2008_time.png', format='png')
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
                    reference_epoch = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

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
    plot.savefig('../data/graphs/nrlmsise_time/' + str(satellite_id) + '_nrlmsise_time.png', format='png')
    plot.close()

def run_altitude_time():
    if not os.path.exists("../data/graphs/altitude_time/"):
        os.makedirs("../data/graphs/altitude_time/")

    with open('../data/reentry_ids_masterlist.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/graphs/altitude_time/" + str(id) + "_altitude_time.png"):
                continue

            plot_altitude_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1
    print("Finished altitude-time")

def run_jb2008_time():
    if not os.path.exists("../data/graphs/jb2008_time/"):
        os.makedirs("../data/graphs/jb2008_time/")

    with open('../data/reentry_ids_masterlist.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/graphs/jb2008_time/" + str(id) + "_jb2008_time.png"):
                continue

            plot_jb2008_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1

    print("Finished JB2008-time")

def run_nrlmsise_time():
    if not os.path.exists("../data/graphs/nrlmsise_time/"):
        os.makedirs("../data/graphs/nrlmsise_time/")

    with open('../data/reentry_ids_masterlist.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        # create plot for each id
        for id in masterlist:
            id = int(id.strip())

            if os.path.exists("../data/graphs/nrlmsise_time/" + str(id) + "_nrlmsise_time.png"):
                continue

            plot_nrlmsise_time(gather_data_from_csv(id))
            print(f"{count}: {id}")
            count += 1

    print("Finished NRLMSISE00-time")

if __name__ == '__main__':
    if not os.path.exists("../data/graphs/"):
        os.makedirs("../data/graphs/")

    run_altitude_time()
    run_jb2008_time()
    run_nrlmsise_time()
