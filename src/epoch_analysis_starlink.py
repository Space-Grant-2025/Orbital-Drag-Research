import csv
from datetime import datetime
from f10_data import *
from matplotlib import pyplot as plot
from matplotlib.ticker import ScalarFormatter

start_date = datetime.datetime(2023, 1, 1).date()
end_date = datetime.datetime(2024, 1, 1).date()

def get_data():
    delta_list = []
    reference_dates = []
    dst_list = []

    with open(f"../data/epoch_masterlist.csv", 'r') as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            id = row[0]
            reference_epoch = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")

            if start_date < reference_epoch.date() < end_date:

                if row[5] != '' and row[9] != '':
                    prediction_epoch = datetime.datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                    reentry_epoch = datetime.datetime.strptime(row[9], "%Y-%m-%d %H:%M:%S%z")
                    epoch_delta = (prediction_epoch - reentry_epoch).days
                    print(f"{id}: {epoch_delta}")

                    delta_list.append(epoch_delta)
                    reference_dates.append(reference_epoch)
                    dst_list.append(float(row[11]))

    return delta_list, reference_dates, dst_list

def plot_data_horizontal():
    delta_list, reference_dates, dst_list = get_data()


    fig, error_ax = plot.subplots()
    dst_ax = error_ax.twinx()

    plot.title('SPG-4 Prediction Error')
    error_ax.set_xlabel('Reference Epoch (280km)')
    error_ax.set_ylabel('Difference in Estimated and Predicted Reentry (Days)')

    #error_ax.set_yscale('log')
    error_ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    dst_ax.set_ylabel("Minimum DST (14 days)")

    error_ax.scatter(reference_dates, delta_list, s = 5)
    dst_ax.scatter(reference_dates, dst_list, color = 'black', s = 5)

    plot.savefig('../data/epoch_graphs/epoch_analysis_starlink.png', format='png')

def plot_data_vertical():
    delta_list, reference_dates, dst_list = get_data()


    fig, ax = plot.subplots()

    plot.title(f'SPG-4 Prediction Error {start_date} to {end_date}')
    ax.set_xlabel('Difference in Estimated and Predicted Reentry (Days)')
    ax.set_ylabel('Minimum DST (14 days)')

    #error_ax.set_yscale('log')
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))

    ax.scatter(delta_list, dst_list, s = 5)

    plot.savefig('../data/epoch_graphs/epoch_analysis_starlink.png', format='png')

if __name__ == '__main__':
    plot_data_vertical()