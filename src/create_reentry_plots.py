from datetime import datetime
import datetime
import matplotlib.pyplot as plot
from matplotlib import dates as mdates
from satellite_classes import *
import re
import os

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
    start_date = datetime.date(2020, 1, 1)
    end_date = datetime.date(2025, 5, 31)

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
            date = datetime.datetime.strptime(f"{year}-{day}", "%Y-%j").date()

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
                reentry_date = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
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

if __name__ == '__main__':
    if not os.path.exists("../data/graphs/"):
        os.makedirs("../data/graphs/")

    plot_f10_reentries_time(gather_f10_data())