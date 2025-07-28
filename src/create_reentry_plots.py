from datetime import datetime
import datetime
import matplotlib.pyplot as plot
from matplotlib import dates as mdates
from satellite_classes import *
import re
import os

class f10_data:
    def __init__(self, date, value):
        self.date = date
        self.value = value

# getters
    def get_date(self):
        return self.date
    def get_value(self):
        return self.value

def gather_f10_data(start_date, end_date):
    f10_list = []

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
                f10_object = f10_data(date, f10_value)
                f10_list.append(f10_object)
    dates_list = []
    values_list = []

    for f10 in f10_list:
        dates_list.append(f10.get_date())
        values_list.append(f10.get_value())

    return dates_list, values_list

def plot_f10_time(start_date, end_date):
    dates_list, values_list = gather_f10_data(start_date, end_date)

    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    '''ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))'''

    plot.scatter(dates_list, values_list, s = 1)
    plot.title("F10 Values by Time")
    plot.ylabel("F10")
    plot.xlabel("Date (MM/YY)")
    plot.savefig("../data/graphs/f10_time.png", format="png")

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
    plot.savefig("../data/graphs/reentries_time.png")

def plot_f10_reentries_time(start_date, end_date):
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
    f10_dates, f10_values = gather_f10_data(start_date, end_date)

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
    reentry_axis.hist(reentry_list, bins=53, color = 'grey')

    f10_axis.set_ylabel("F10 Values", color = 'black')
    f10_axis.plot(f10_dates, f10_values, color = 'black')

    plot.savefig('../data/graphs/f10_reentries_time.png', format='png')
    print("Plotted F10-reentries-time")

if __name__ == '__main__':
    if not os.path.exists("../data/graphs/"):
        os.makedirs("../data/graphs/")

    plot_f10_time(datetime.date(1957, 1, 1), datetime.date(2025, 12, 31))
    '''plot_reentries_time()
    plot_f10_reentries_time(datetime.date(2020, 1, 1), datetime.date(2025, 1, 1))'''