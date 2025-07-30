import datetime
import re
import csv
import matplotlib.pyplot as plot
from special_tools import smooth, day2doy
from create_mass_reentry_plots import *

class f10_data:
    def __init__(self, date, value):
        self.date = date
        self.value = value

# getters
def get_date(self):
    return self.date
def get_value(self):
    return self.value

def get_day_dict(start_date, end_date):
    day_list = []

    current_date = start_date
    one_day = datetime.timedelta(days=1)

    # fill list
    while current_date <= end_date:
        day_list.append(current_date)
        current_date += one_day

    # fill dict with none
    day_nums = dict()
    for day in day_list:
        day_nums[str(day)] = 0
    return day_nums

def get_average_f10(start_year, end_year):
    f10_dates, f10_values = get_data_from_f10_csv(datetime.date(start_year, 1, 1), datetime.date(end_year, 5, 31))
    # to fill with values
    f10_dict = get_year_dict(start_year, end_year)

    f10_time_floats = []
    for x in range(len(f10_values)):
        year = f10_dates[x].year
        day = day2doy(year, f10_dates[x].month, f10_dates[x].day)
        f10_time_floats.append(year + day / 365)

    f10_values = smooth(f10_values, 30)
    return f10_values, f10_time_floats

def get_data_from_SOLFSMY():
    f10_list = []

    with open('../data/external_datasets/SOLFSMY.TXT', 'r') as file:
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

            # create object and add to list
            f10_object = f10_data(date, f10_value)
            f10_list.append(f10_object)

    return f10_list

def get_data_from_olivera_csv():
    f10_list = []

    with open('../data/external_datasets/oliveira_solar_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
            value = float(row[4])

            # create object and add to list
            f10_object = f10_data(date, value)
            f10_list.append(f10_object)

    return f10_list

def get_f10_masterlist():
    solfsmy_list = get_data_from_SOLFSMY()
    oliveira_list = get_data_from_olivera_csv()

    start_date = oliveira_list[0]
    end_date = solfsmy_list[len(solfsmy_list) - 1]

    day_vals = get_day_dict(start_date, end_date)

    for f10 in oliveira_list:
        # make sure within date range
        day_vals[str(get_date(f10))] = get_value(f10)

    # add solfsmy data
    for f10 in solfsmy_list:
        f10_date = str(get_date(f10))
        f10_value = get_value(f10)

        # make sure within date range
        # if value is unset, add solfsmy data and move on
        if day_vals[f10_date] == 0:
            day_vals[f10_date] = f10_value
            continue

        # if values do not match, average them
        if day_vals[f10_date] != f10_value:
            day_vals[f10_date] = (day_vals[f10_date] + f10_value) / 2

    return day_vals

def write_f10_to_file():
    f10_dict = get_f10_masterlist()

    with open('../data/f10_data.csv', 'w') as file:
        file.write("DATE (YY-MM-DD), VALUE\n")

        for date, value in f10_dict.items():
            file.write(f"{date}, {value}\n")

def get_data_from_f10_csv(start_date, end_date):
    f10_dates = []
    f10_values = []
    with open ('../data/f10_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            f10_date = datetime.datetime.strptime(row[0], "%Y-%m-%d").date()
            f10_value = float(row[1])
            if start_date <= f10_date <= end_date:
                f10_dates.append(f10_date)
                f10_values.append(f10_value)
    return f10_dates, f10_values

def plot_f10_time(start_date, end_date):
    f10_dates, f10_values = get_data_from_f10_csv(start_date, end_date)


    fig, ax = plot.subplots(layout='constrained')
    # x axis (dates)
    '''ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%y'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=1))'''

    plot.scatter(f10_dates, f10_values, s = 1)
    plot.title("F10 Values by Time")
    plot.ylabel("F10")
    plot.xlabel("Date (YYYY)")
    plot.savefig("../data/mass_graphs/f10_time.png", format="png")

if __name__ == '__main__':
    start_date = datetime.date(1957, 1, 1)
    end_date = datetime.date(2025, 5, 31)
    plot_f10_time(start_date, end_date)