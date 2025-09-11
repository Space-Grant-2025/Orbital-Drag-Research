import csv
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from numpy import linspace
from colormaps import idl39_w, plasma_w

max_error = 10
min_error = 0
num_bins = 30
bin_height = (max_error - min_error) / num_bins
num_days = 30

count = np.zeros((num_bins, num_days))

def get_data():
    id = 48384

    with open (f"../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv") as f:
        reader = csv.reader(f)
        # pass over headers
        next(reader)

        # get references
        first_line = next(reader)
        reference_epoch = datetime.strptime(first_line[0], "%Y-%m-%d %H:%M:%S%z")
        reference_reentry = datetime.strptime(first_line[2], "%Y-%m-%d %H:%M:%S%z")

        # current altitude x days after ref epoch x prediction - current propagation

        for row in reader:
            current_epoch = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            current_prediction = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S%z")

            day_delta = (current_epoch - reference_epoch).days
            error = abs((reference_reentry - current_prediction).days)
            error_bin = int((error - min_error) / bin_height)

            if min_error < error_bin <= bin_height:
                if 0 <= day_delta < num_days:
                    count[error_bin, day_delta] += 1
    return count

def plot_data():
    count = get_data()
    plt.pcolormesh(count, cmap = plasma_w, vmin = 0, vmax = 300)
    #plt.yticks(linspace(0, bin_height, 9), linspace(min_error, max_error, 9))

    plt.xlabel('Days After Reference Altitude')
    plt.ylabel('Prediction Error (Days)')
    plt.title(f"Superimposed SGP-4 Prediction Error of Reentered Starlinks")

    plt.colorbar(label='Number of Instances')
    plt.show()

if __name__ == '__main__':
    plot_data()
