import os
import sys
from datetime import timedelta, datetime

import ephem
from collections import deque
from read_tle_by_id import get_date_from_tle


# prediction epoch (space-track.org)
# take reference altitude tle and create array hour by hour and create new objects for pyephem to read
# initial tle data stay the same
# return epoch when elevation is < 100km
#
# reference altitude epoch
# find tle data point where satellite altitude is closest to 280km
#
# estimated reentry epoch
# last available tle and create array hour by hour and create new objects for pyephem to read
# initial tle data stays the same
# return epoch when elevation is < 100km
# save elevation to h100 [km]
#
# h280 [km]
# save reference altitude
#
# h100 [km]
# save estimated reentry epoch
#
# min dst
# download monthly data
# epoch of reference altitude and read data hourly for 14 days and take min dst of all epochs

# given a NORAD ID, reads in processed csv data
# returns altitude closest to 280km and corresponding epoch
def get_reference_alt(id):
    with open(f'../data/human_readable/tle_{id}.csv', 'r') as csvfile:
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

# given NORAD, takes in last tle data point
# returns propagated altitude less than 100km and corresponding epoch
def get_estimated_reentry(id):
    # get julian day of last tle data point
    with (open(f'../data/tles/tle_{id}.txt', 'r') as file):
        # pass over headers
        file.readline()

        # gather last tle data point
        file_queue = deque(file.readlines())
        tle2 = file_queue.pop().strip()
        tle1 = file_queue.pop().strip()

        # ephem object reads in given tle data
        ephem_satellite = ephem.readtle('NORAD' + str(id), tle1, tle2)

        # initalize date
        date = get_date_from_tle(tle1)
        one_hr = timedelta(hours=1)

        # increase date by one hour until elevation is less than 100km
        altitude = 9999
        while altitude >= 100:
            # increment date and make readable to pyephem
            date = date + one_hr
            str_date = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
            ephem_date = ephem.date(str_date)

            # compute satellite
            ephem_satellite.compute(ephem_date)
            altitude = ephem_satellite.elevation / 1000

        return altitude, str(date)


def write_epochs_to_csv(id):
    with open(f'../data/epochs.csv', 'w') as epochs:
        epochs.write(f'{id},{get_reference_alt(id)[1]},{get_reference_alt(id)[0]},{get_estimated_reentry(id)[1]},{get_estimated_reentry(id)[0]}\n')

def main():
    # delete epochs.csv every time this program runs to get a fresh set of data
    if os.path.exists(f'../data/epochs.csv'):
        os.remove(f'../data/epochs.csv')

    # write headers
    with open(f'../data/epochs.csv', 'w') as epochs:
        epochs.write("NORAD ID, REFERENCE ALTITUDE EPOCH, REFERENCE ALTITUDE (KM), ESTIMATED REENTRY EPOCH, ESTIMATED REENTRY ALTITUDE (KM), PREDICTION EPOCH, PREDICTION ALTITUDE, MIN DST")
        epochs.close()

    with open(f'../data/reentry_ids_masterlist.txt.txt', 'r') as masterlist:
        # pass over headers
        masterlist.readline()

        for id in masterlist:
            id = id.strip()
            write_epochs_to_csv(id)

write_epochs_to_csv(44235)