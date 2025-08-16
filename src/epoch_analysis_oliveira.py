import sys
import matplotlib
import matplotlib.pyplot as plot
from special_tools import day2doy
from numpy import zeros, linspace
from colormaps import idl39_w, plasma_w

count = zeros((20, 16))

max_height = 400
min_height = 0
num_bins = 20
bin_height = (max_height - min_height) / num_bins

num_days = 15

def get_data():
    with open('../data/external_datasets/oliveira_data.txt') as data:
        lines = data.readlines()[2:]
        for line in lines:
            sat = line.split()
            id = sat[0]
            print(id)

            # get reference time
            year = int(sat[3][:4])
            month = int(sat[3][5:7])
            day = int(sat[3][8:])
            doy = day2doy(year, month, day)
            # days since 2020/1/1
            reference_time = (year - 2020) * 365 + (doy - 1)

            with open('../data/external_datasets/oliveira_epochs/ephem_' + id + '.txt') as data:
                for line in data:
                    split_line = line.split()

                    # get current date
                    year = int(split_line[0][:4])
                    month = int(split_line[0][5:7])
                    day = int(split_line[0][8:])
                    hour = int(split_line[1][:2])
                    min = int(split_line[1][3:5])
                    sec = int(split_line[1][6:])
                    day_of_year = day2doy(year, month, day)
                    # days since 2020/1/1
                    current_time = (year - 2020) * 365. + (day_of_year - 1) + hour / 24. + min / 1440. + sec / 86400.

                    # make sure current time is after 280km
                    if current_time >= reference_time:

                        day_delta = int(current_time - reference_time)
                        altitude = int((float(split_line[4]) - min_height) / bin_height)

                        if min_height < altitude <= bin_height:
                            if 0 < day_delta < num_days:

                                count[altitude, day_delta] = count[altitude, day_delta] + 1
    return count

def plot_data():
    count = get_data()
    plot.pcolormesh(count, cmap = plasma_w, vmin = 0, vmax = 300, label = 'Number of Instances')
    plot.yticks(linspace(0, bin_height, 9), linspace(min_height, max_height, 9))

    plot.xlabel('Days After Reference Altitude')
    plot.ylabel('Altitude (km)')
    plot.title(f"Reentry Propagation Error for Reentered Starlinks")

    plot.colorbar()
    plot.show()

if __name__ == '__main__':
    plot_data()