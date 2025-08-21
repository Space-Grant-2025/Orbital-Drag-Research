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
num_days = 16

count = zeros((num_bins, num_days))

def get_data():
    excluded = 0
    with open("../data/epoch_masterlist.csv") as masterlist:
        master_reader = csv.reader(masterlist)
        # pass over headers
        next(master_reader)

        for row in master_reader:
            id = row[0]
            print(id)
            reference_epoch = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

            with open(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv") as epoch_file:
                epoch_reader = csv.reader(epoch_file)
                # pass over headers
                next(epoch_reader)

                for row in epoch_reader:
                    current_epoch = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
                    # make sure current time is after 280km
                    if current_epoch >= reference_epoch:

                        day_delta = (current_epoch - reference_epoch).days
                        altitude = float(row[1])
                        altitude_bin = int((altitude - min_height) / bin_height)

                        if min_height < altitude_bin <= bin_height:
                            if 0 < day_delta < num_days:
                                count[altitude_bin, day_delta] += 1
                            else:
                                excluded += 1
                        else:
                            excluded += 1
    print(f"Excluded {excluded} epochs")
    return count

def plot_data():
    count = get_data()
    plot.pcolormesh(count, cmap = plasma_w, vmin = 0, vmax = 300)
    plot.yticks(linspace(0, bin_height, 9), linspace(min_height, max_height, 9))

    plot.xlabel('Days After Reference Altitude')
    plot.ylabel('Altitude (km)')
    plot.title(f"Reentry Propagation Error for Reentered Starlinks")

    plot.colorbar(label='Number of Instances')
    plot.savefig("../data/epoch_graphs/superimposed_epoch_starlink.png")

if __name__ == '__main__':
    plot_data()