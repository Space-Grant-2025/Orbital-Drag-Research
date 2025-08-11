import os
from curses.ascii import isdigit
from datetime import datetime
from matplotlib.pyplot import pcolormesh
import matplotlib.pyplot as plot
from numpy import zeros
from colormaps import idl39_w
import matplotlib
import os

max_height = 300
bin_height = 10
num_bins = (max_height - 100) // bin_height
num_days = 20

def fill_count_arr(count, lines, reference_epoch):
    for x in range(2, len(lines)):
        row = lines[x].strip().split()
        # date from which is being propagated
        current_date = datetime.strptime(row[0], "%Y-%m-%d").date()
        current_time = datetime.strptime(row[1][:5], "%H:%M").time()
        current_epoch = datetime(current_date.year, current_date.month, current_date.day, current_time.hour, current_time.minute)

        day_delta = (current_epoch - reference_epoch).days

        # altitude before propagation
        altitude = float(row[4])
        altitude_bin = int((altitude - 100) / bin_height)


        if altitude_bin >= num_bins or day_delta >= num_days:
            continue

        count[altitude_bin, day_delta] += 1

    return count

def process_file(id, count):
    with open(f"../data/external_datasets/oliveira_epochs/ephem_{id}.txt", "r") as file:
        lines = file.readlines()
        if len(lines) <= 1:
            return None
        first_row = lines[1].strip().split()
        first_date = datetime.strptime(first_row[0], "%Y-%m-%d").date()
        first_time = datetime.strptime(first_row[1][:5], "%H:%M").time()
        '''last_row = lines[len(lines) - 1].strip()
        last_date = last_row.split('  ')[0]'''

        reference_epoch = datetime(first_date.year, first_date.month, first_date.day, first_time.hour, first_time.minute)
        # reentry_epoch = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S')

        count = fill_count_arr(count, lines, reference_epoch)
    return count

def run_through_ids():
    # initialize count
    count = zeros((num_bins, num_days))

    with open("../data/external_datasets/oliveira_data.txt", "r") as file:
        # pass over headers
        next(file)
        next(file)

        for line in file:
            id = int(line.split('\t')[0])
            count = process_file(id, count)
            print(id)
    return count

def create_graph():
    count = run_through_ids()

    fig, ax = plot.subplots(layout='constrained')
    pcolormesh(count, cmap=idl39_w)
    plot.colorbar(label='Number of Instances')
    plot.xlabel('Days After Reference Epoch')

    y_labels = []
    for y in ax.get_yticklabels():
        y_labels.append(int(float(y.get_text()) * bin_height) + 100)
    plot.yticks(ax.get_yticks(), y_labels)
    plot.ylabel('Altitude (km)')

    plot.title(f"Reentry Propagation Error for Reentered Starlinks")
    # plot.savefig(f"../data/starlink_reentries_2020_2025/epoch_analysis/analysis_{id}.png", format='png')
    plot.show()

if __name__ == "__main__":
    create_graph()