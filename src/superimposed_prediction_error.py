from csv import reader

from dateutil.relativedelta import relativedelta

from modular_methods import day2doy
from numpy import array, zeros
from colormaps import idl39_w, plasma_w
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

max_height = 310
min_height = 200
num_alt_bins = 20
bin_height = (max_height - min_height) / num_alt_bins
bins_per_day = 2
num_days = 10

count = zeros((num_alt_bins, num_days * bins_per_day))

'''Get estimated re-entry epoch and altitude from sl_predictions.txt
This was already propagated from the last tle in my previous work
This will be appended later'''

# returns estimated reentry date, estimated reentry alt, reference date
def get_reentry_and_reference(target_id):
    with open('../data/epoch_masterlist.csv', 'r') as epoch_masterlist:
        masterlist = reader(epoch_masterlist)
        # pass over headers
        next(masterlist)

        for row in masterlist:
            id = int(row[0])
            if id == target_id:
                if row[9] != "":
                    est_reentry_date = datetime.strptime(row[9], '%Y-%m-%d %H:%M:%S%z')
                    est_reentry_alt = float(row[10])
                    reference_epoch = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S%z')
                    return est_reentry_date, est_reentry_alt, reference_epoch
    return None, None, None

'''
Read the new propagation file with SGP-4 estimated re-entries as a function of time
The first epoch is the zero-epoch time (reference altitude)
The error will be the absolute value of the difference between the estimated-re-entry
and prediction re-entry
'''

# returns 2d array of error values
def get_error_data():
    with open("../data/starlink_reentries_list.txt", "r") as file:
        # pass over headers
        next(file)

        for line in file:
            id = int(line.strip())

            estimated_reentry_date, estimated_reentry_alt, reference_epoch = get_reentry_and_reference(id)
            if estimated_reentry_alt is None or estimated_reentry_date is None or reference_epoch is None:
                continue

            with open(f'../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv', 'r') as file:
                csv_reader = reader(file)
                # pass over headers
                next(csv_reader)

                for row in csv_reader:
                    if row[2] != "None":
                        current_epoch = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S%z')

                        predict_reentry_date = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S%z')

                        error = abs((predict_reentry_date - estimated_reentry_date).days)

                        day_delta = current_epoch - reference_epoch
                        hour_delta = int(day_delta.total_seconds() / 3600)
                        day_bin = int((day_delta.days * bins_per_day) + (hour_delta % (24 // bins_per_day)))
                        current_alt = float(row[1])
                        altitude_bin = int((current_alt - min_height) / bin_height)

                        if min_height < current_alt < max_height:
                            if 0 <= day_bin < num_days * bins_per_day:
                                count[altitude_bin, day_bin] += error
            print(id)
    return count

def plot_data():
    count = get_error_data()

    # plot it
    plt.pcolormesh(count, cmap=plasma_w)
    plt.xticks(np.linspace(0, num_days * bins_per_day, 5), np.linspace(0, num_days, 5))
    plt.yticks(np.linspace(0, num_alt_bins, 11), np.linspace(min_height, max_height, 11))

    plt.xlabel('Hours after Reference Epoch (280km)')
    plt.ylabel('Altitude (km)')

    plt.title('SPG-4 Prediction Error on Starlink Reentries')

    cb = plt.colorbar()
    cb.set_label('Prediction Error (Days)')

    plt.show()

plot_data()
