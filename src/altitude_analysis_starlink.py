from numpy import zeros
import csv
import datetime
import matplotlib.pyplot as plot
from numpy import zeros, linspace
from colormaps import idl39_w, plasma_w

max_height = 200
min_height = -max_height
num_bins = 20
bin_height = int((max_height * 2) / num_bins)
num_days = 21    # past reference epoch

min_dst = -100

count = zeros((num_bins + 1, num_days + 1))

def get_data():
    id_list = []
    with open ('../data/epoch_masterlist.csv', 'r') as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for line in csv_reader:
            id = int(line[0])
            dst = float(line[11])
            if dst <= min_dst:
                id_list.append(id)
            else:
                print(dst)

        for id in id_list:

            with open(f'../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv', 'r') as file:
                csv_reader = csv.reader(file)
                # pass over headers
                next(csv_reader)
                try:
                    first_row = next(csv_reader)
                except StopIteration:
                        print(f"{id} empty")
                        continue
                reference_day = datetime.datetime.strptime(first_row[0], "%Y-%m-%d %H:%M:%S%z")

                for row in csv_reader:
                    if row[3] != 'None':
                        current_day = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
                        alt_delta = float(row[3])
                        alt_bin = int((alt_delta - min_height) / bin_height)
                        day_bin = (current_day - reference_day).days

                        if 0 <= alt_bin <= bin_height:
                            if 0 <= day_bin < num_days:
                                count[alt_bin][day_bin] += 1
    return count

def plot_data():
    count = get_data()
    plot.pcolormesh(count, cmap = plasma_w, vmin = 0, vmax = 300)
    plot.yticks(linspace(0, bin_height, 9), linspace(-max_height, max_height, 9))

    plot.xlabel('Days After Reference Altitude')
    plot.ylabel('Prediction-Estimated Altitude Difference')
    plot.title(f"Reentry Propagation Error for Reentered Starlinks")

    plot.colorbar(label = 'Number of Instances')
    plot.savefig('../data/epoch_graphs/altitude_analysis_starlink.png', format ='png')

if __name__ == '__main__':
    plot_data()
