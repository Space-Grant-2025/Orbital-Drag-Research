import os
import sys
import sgp4
from sgp4.api import SGP4_ERRORS
from sgp4 import conveniences
from collections import deque
import datetime

# given a NORAD ID, reads in processed csv data and return the time when satellite altitude is closest to 280km
def estimate_280km(id):
    with open(f'./data/human_readable/tle_{id}.csv', 'r') as csvfile:
        # pass over header
        csvfile.readline()
        # tuple holding closest altitude and corresponding date, initialized at massive number and date placeholder
        closest_alt = float(sys.maxsize), "0000-00-00 00:00:00"

        # loop over csv data and hold altitude nearest to 280 and corresponding altitude
        for row in csvfile:
            split_row = row.split(',')
            # current values
            current_alt = float(split_row[1]), split_row[0]
            # distances of minimum and current values from 280
            curr_distance_from_280 = abs(current_alt[0] - 280)
            min_distance_from_280 = abs(closest_alt[0] - 280)
            if curr_distance_from_280 < min_distance_from_280:
                closest_alt = current_alt
    return closest_alt

def propagate_100km(id):
    # get julian day of last tle data point
    with open(f'./data/human_readable/tle_{id}.csv', 'r') as file:
        # pass over headers
        file.readline()

        last_line = deque(file, maxlen=1).pop().strip()
        last_date = datetime.datetime.strptime(last_line.split()[0], '%Y/%m/%d %H:%M:%S%Z')
        julian_day, fraction = conveniences.jday_datetime(last_date)

def write_epochs_to_csv(id):
    prediction_epoch = estimate_280km(id)[0]
    height_280km = estimate_280km(id)[1]

    with open(f'../data/epochs.csv', 'w') as epochs:
        epochs.write(f'{id},{prediction_epoch},{height_280km}\n')

def main():
    # delete epochs.csv every time this program runs to get a fresh set of data
    if os.path.exists(f'../data/epochs.csv'):
        os.remove(f'../data/epochs.csv')

    # write headers
    with open(f'../data/epochs.csv', 'w') as epochs:
        epochs.write("NORAD ID,PREDICTION EPOCH (space-track.org),REFERENCE ALTITUDE EPOCH (100km),ESTIMATED REENTRY EPOCH,HEIGHT CLOSEST TO 280KM,HEIGHT CLOSEST TO 100KM,MIN DST")
        epochs.close()

    with open(f'../data/reentry_ids_masterlist.txt.txt', 'r') as masterlist:
        # pass over headers
        masterlist.readline()

        for id in masterlist:
            id = id.strip()
            write_epochs_to_csv(id)


print(estimate_280km(48384))