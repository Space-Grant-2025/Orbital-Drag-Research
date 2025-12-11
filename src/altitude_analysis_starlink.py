from numpy import zeros
import csv
import datetime
import matplotlib.pyplot as plot
from numpy import zeros, linspace
from colormaps import idl39_w, plasma_w
import pandas as pd

max_height = 200
min_height = -max_height
num_bins = 20
bin_height = int((max_height * 2) / num_bins)
num_days = 21    # past reference epoch

min_dst = -100

count = zeros((num_bins + 1, num_days + 1))

def get_data():
    id_list = []
    epoch_masterlist = pd.read_csv('../data/epoch_masterlist.csv')
    id_list = epoch_masterlist['NORAD ID'].tolist()
    dst_list = epoch_masterlist['MIN DST'].tolist()

    for id in id_list:
        epoch_df = pd.read_csv(f'../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv').dropna()

        try:
            first_row = epoch_df.iloc[0]
        except IndexError:
            print(f"{id} empty")
            continue

        reference_day = datetime.datetime.strptime(first_row["TLE INSTANCE EPOCH"], "%Y-%m-%d %H:%M:%S%z")
        epoch_df = epoch_df.iloc[1:]

        current_day = pd.to_datetime(epoch_df["TLE INSTANCE EPOCH"], format="%Y-%m-%d %H:%M:%S%z")
        alt_delta = epoch_df[("PREDICTION DELTA (KM)")]

        for day_index in range(len(current_day)):
            alt_bin = int((alt_delta.iloc[day_index] - min_height) / bin_height)
            day_bin = (current_day.iloc[day_index] - reference_day).days

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
