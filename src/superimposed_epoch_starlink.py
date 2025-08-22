import sys
import csv
import matplotlib
import matplotlib.pyplot as plot
from special_tools import day2doy
from numpy import zeros, linspace
from colormaps import idl39_w, plasma_w
from datetime import datetime

max_height = 400
min_height = 0
num_bins = 20
bin_height = (max_height - min_height) / num_bins
num_days = 20

count = zeros((num_bins, num_days))

def get_data():
    with open("../data/starlink_reentries_list.txt", "r") as file:
        # pass over headers
        next(file)

        for line in file:
            id = int(line)

            with open(f"../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv") as epoch_file:
                epoch_reader = csv.reader(epoch_file)
                # pass over headers
                next(epoch_reader)

                # get references
                first_line = next(epoch_reader)
                reference_epoch = datetime.strptime(first_line[0], "%Y-%m-%d %H:%M:%S")

                for row in epoch_reader:
                    current_epoch = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")

                    day_delta = (current_epoch - reference_epoch).days
                    altitude = float(row[1])
                    altitude_bin = int((altitude - min_height) / bin_height)

                    if min_height < altitude_bin <= bin_height:
                        if 0 <= day_delta < num_days:
                            count[altitude_bin, day_delta] += 1
    return count

def plot_data():
    count = get_data()
    plot.pcolormesh(count, cmap = plasma_w, vmin = 0, vmax = 300)
    plot.yticks(linspace(0, bin_height, 9), linspace(min_height, max_height, 9))

    plot.xlabel('Days After Reference Altitude')
    plot.ylabel('Altitude (km)')
    plot.title(f"Superimposed Trajectory of Reentered Starlinks")

    plot.colorbar(label='Number of Instances')
    plot.savefig("../data/epoch_graphs/superimposed_epoch_starlink.png")

if __name__ == '__main__':
    plot_data()