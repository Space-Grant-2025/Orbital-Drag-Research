import time
from csv import reader
from datetime import datetime
import ephem
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import numpy as np
from contourpy.util import data

altitude_list = []
date_list = []

id = 44740

# populates lists based on csv data created by read_tle
def gather_data_from_csv(id):
    with open('../data/human_readable/tle_' + str(id) + '.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)

        for row in csv_reader:
            date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
            altitude = row[1]

            date_list.append(date)
            altitude_list.append(float(altitude))

def create_plot():
    fig, ax = plot.subplots(figsize=(5.4, 5.4), layout='constrained')
    plot.plot(date_list[len(date_list)-150:], altitude_list[len(altitude_list)-150:])
    plot.ylabel("Altitude (km)")
    plot.xlabel("Date")

    ax.set(title="NORAD CAT ID " + str(id))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=14))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

    # plot.show()
    plot.savefig('../data/graphs/' + str(id) + '_altitude_time.png', dpi=300, format='png')


gather_data_from_csv(id)
create_plot()