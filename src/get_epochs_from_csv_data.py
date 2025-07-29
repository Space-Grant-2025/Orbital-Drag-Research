import glob
import os
import sys
from datetime import timedelta, datetime
import ephem
import queue
from read_tle_by_id import get_date_from_tle
from special_tools import day2doy

class satellite_epochs:
    def __init__(self, id):
        self.id = id
        self.reference_epoch = get_reference(id)[1]
        self.reference_alt = get_reference(id)[0]
        self.estimated_reentry_epoch = get_estimated_reentry(id)[1]
        self.estimated_reentry_alt = get_estimated_reentry(id)[0]
        self.prediction_epoch = get_prediction(id)[1]
        self.prediction_alt = get_prediction(id)[0]
        self.min_dst = get_dst(id)

# getters
def get_id(self):
    return self.id
def get_reference_epoch(self):
    return self.reference_epoch
def get_reference_alt(self):
    return self.reference_alt
def get_estimated_reentry_epoch(self):
    return self.estimated_reentry_epoch
def get_estimated_reentry_alt(self):
    return self.estimated_reentry_alt
def get_prediction_epoch(self):
    return self.prediction_epoch
def get_prediction_alt(self):
    return self.prediction_alt
def get_min_dst(self):
    return self.min_dst

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
def get_reference(id):
    with open(f'../data/human_readable/tle_{id}.csv', 'r') as csvfile:
        # pass over header
        csvfile.readline()
        # tuple holding closest altitude and corresponding date, initialized at massive number and date placeholder
        closest_alt = float(sys.maxsize), None

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
    with (open(f'../data/starlink_tles/tle_{id}.txt', 'r') as file):
        # pass over headers
        file.readline()

        # gather last tle data point
        tles = file.readlines()
    file_queue = queue.LifoQueue(len(tles))
    for tle in tles:
        file_queue.put(tle)

    tle2 = file_queue.get().strip()
    tle1 = file_queue.get().strip()

    return get_100km(id, tle1, tle2)

def get_prediction(id):
    reference_date = get_reference(id)[1]

    with (open(f'../data/starlink_tles/tle_{id}.txt', 'r') as file):
        lines = file.readlines()[:]
    file.close()

    for x in range(0, len(lines), 2):
        # create tle object and add to list
        tle1 = lines[x].strip("\n")
        tle2 = lines[x + 1].strip("\n")

        if str(get_date_from_tle(tle1)) == reference_date:
            return get_100km(id, tle1, tle2)
    return None

def get_100km(id, tle1, tle2):
    # ephem object reads in given tle data
    ephem_satellite = ephem.readtle('NORAD' + str(id), tle1, tle2)

    # initialize date
    date = get_date_from_tle(tle1)
    one_hr = timedelta(hours=1)

    # increase date by one hour until elevation is less than 100km
    altitude = 9999
    count = 0
    while altitude >= 100:
        # checks if loop has gone beyond 6 months (30 days each)
        if count >= 4320:
            return "", ""
        # increment date and make readable to pyephem
        date = date + one_hr
        count += 1
        str_date = datetime.strftime(date, "%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # compute satellite
        ephem_satellite.compute(ephem_date)
        altitude = ephem_satellite.elevation / 1000

    return altitude, str(date)

# get minimum dst within the next 14 days after reference altitude occurrence
# dst files downloaded from https://wdc.kugi.kyoto-u.ac.jp/dst_realtime/index.html in wdc format
def get_dst(id):
    reference_epoch = get_reference(id)[1]
    reference_epoch = datetime.strptime(reference_epoch, "%Y-%m-%d %H:%M:%S%z")
    reference_year = reference_epoch.year
    reference_days = day2doy(reference_epoch.year, reference_epoch.month, reference_epoch.day)
    reference_hour = reference_epoch.hour

    reference_time = (reference_year - 2000) * 365 * 24 + (reference_days - 1) * 24 + reference_hour - 1

    # number of days after reference epoch
    cutoff = 14
    dst_list = []
    dst_bag = sorted(glob.glob('../data/dst/dst*'))

    for file in dst_bag:
        with open(file) as data:
            for lines in data:
                year = int(lines[3:5]) + 2000
                month = int(lines[5:7])
                day = int(lines[8:10])

                day_of_year = day2doy(year, month, day)

                # extract dst data from file
                for dst, hour in zip(range(20, 119, 4), range(1, 25)):
                    # number of hours since 2000
                    time = (year - 2000) * 365 * 24 + (day_of_year - 1) * 24 + hour - 1

                    if reference_time < time < (reference_time + cutoff * 60):
                        dst_list.append(float(lines[dst:dst+4]))
    return min(dst_list)


def write_epochs_to_csv(epochs_list):
    # delete epochs.csv every time this program runs to get a fresh set of data
    if os.path.exists(f'../data/epochs.csv'):
        os.remove(f'../data/epochs.csv')

    with open(f'../data/epochs.csv', 'w') as epochs:
        # write headers
        epochs.write("NORAD ID, REFERENCE ALTITUDE EPOCH, REFERENCE ALTITUDE (KM), ESTIMATED REENTRY EPOCH, ESTIMATED REENTRY ALTITUDE (KM), PREDICTION EPOCH, PREDICTION ALTITUDE (KM), MIN DST\n")

        count = 0
        for satellite in epochs_list:
            count += 1
            print(f'{count}: {get_id(satellite)}')
            epochs.write(f'{get_id(satellite)},{get_reference_epoch(satellite)},{get_reference_alt(satellite)},{get_estimated_reentry_epoch(satellite)},{get_estimated_reentry_alt(satellite)},{get_prediction_epoch(satellite)},{get_prediction_alt(satellite)},{get_min_dst(satellite)}\n')

def main():
    epochs_list = []

    with open(f'../data/reentry_ids_masterlist.txt', 'r') as masterlist:
        count = 1
        # pass over headers
        masterlist.readline()

        for id in masterlist:
            id = id.strip()
            satellite = satellite_epochs(id)
            epochs_list.append(satellite)
            print(f'{count}: {id}')
            count += 1

    write_epochs_to_csv(epochs_list)

if __name__ == '__main__':
    main()