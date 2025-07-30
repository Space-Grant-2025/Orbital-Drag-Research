import sys
from datetime import timedelta
from types import NoneType
import os
from read_tle_by_id import get_date_from_tle
from datetime import datetime
import ephem

class tle_epochs():
    def __init__(self, id, line0, line1, line2):
        self.line1 = line1
        self.line2 = line2
        # ephem object reads in given tle data
        ephem_satellite = ephem.readtle('NORAD' + str(id), line1, line2)
        # assign values
        self.id = id
        self.name = line0[1:]

        # process date
        self.date = get_date_from_tle(line1)
        str_date = datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)
        str_date = datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # propagate flight data
        ephem_satellite.compute(ephem_date)
        self.altitude = ephem_satellite.elevation / 1000 # in km

# getters
def get_tle_id(self):
    return self.id
def get_name(self):
    return self.name
def get_date(self):
    return self.date
def get_altitude(self):
    return self.altitude
def get_tle1(self):
    return self.line1
def get_tle2(self):
    return self.line2

class reference_predictions():
    def __init__(self, id, ref_date, ref_alt, reentry_date, reentry_alt):
        self.id = id
        self.ref_date = ref_date
        self.ref_alt = ref_alt
        self.reentry_date = reentry_date
        self.reentry_alt = reentry_alt

# getters
def get_ref_id(self):
    return self.id
def get_ref_date(self):
    return self.ref_date
def get_ref_alt(self):
    return self.ref_alt
def get_reentry_date(self):
    return self.reentry_date
def get_reentry_alt(self):
    return self.reentry_alt


def get_tle_list(id):
    tle_list = []
    with open(f"../data/starlink_reentries_2020_2025/starlink_tles/tle_{id}.txt", "r") as file:
        lines = file.readlines()
        for x in range(0, len(lines), 3):
            tle0 = lines[x].strip()
            tle1 = lines[x + 1].strip()
            tle2 = lines[x + 2].strip()

            tle = tle_epochs(id, tle0, tle1, tle2)
            tle_list.append(tle)
    return tle_list


def get_reference(id, tle_list):
    closest_alt = float(sys.maxsize), NoneType
    for tle in tle_list:
        # current values
        current_alt = get_altitude(tle)
        # distances of minimum and current values from 280
        curr_distance_from_280 = abs(current_alt - 280)
        min_distance_from_280 = abs(closest_alt[0] - 280)
        if curr_distance_from_280 < min_distance_from_280:
            closest_alt = current_alt, tle
    return closest_alt[1]

def predict_100km(tle):
    id = get_tle_id(tle)
    tle1 = get_tle1(tle)
    tle2 = get_tle2(tle)
    # ephem object reads in given tle data
    ephem_satellite = ephem.readtle('NORAD' + str(id), tle1, tle2)

    # initialize date
    date = get_date(tle)
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

    return altitude, date

def write_data_to_csv(id):
    with open(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv", "w") as file:
        file.write("ID,REFERENCE DATE,REFERENCE ALTITUDE (KM),PREDICTION DATE,PREDICTION ALTITUDE (KM)\n")

        for object in generate_reference_predictions_data(id):
            file.write(f"{get_ref_id(object)},{get_ref_date(object)},{get_ref_alt(object)},{get_reentry_date(object)},{get_reentry_alt(object)}\n")

def generate_reference_predictions_data(id):
    reference_predictions_list = []
    tle_list = get_tle_list(44235)
    reference_object = get_reference(44235, tle_list)
    index = tle_list.index(reference_object)

    for x in range(index, len(tle_list)):
        tle = tle_list[x]
        altitude, date = predict_100km(tle)
        reference_object = reference_predictions(get_tle_id(tle), get_date(tle), get_altitude(tle), date, altitude)
        reference_predictions_list.append(reference_object)
    return reference_predictions_list

if __name__ == "__main__":
    if not os.path.exists("../data/starlink_reentries_2020_2025/epoch_files/"):
        os.makedirs("../data/starlink_reentries_2020_2025/epoch_files/")

    write_data_to_csv(44235)