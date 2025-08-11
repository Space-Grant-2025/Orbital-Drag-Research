import sys
from datetime import timedelta
import csv
import os
from read_tle_by_id import get_date_from_tle, get_jb2008_density
from datetime import datetime
import ephem

class reference_tle():
    def __init__(self, id, line1, line2):
        self.line1 = line1
        self.line2 = line2
        # ephem object reads in given tle data
        ephem_satellite = ephem.readtle('NORAD' + str(id), line1, line2)
        # assign values
        self.id = id

        # process date
        self.date = get_date_from_tle(line1)
        str_date = datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # create flight data
        ephem_satellite.compute(ephem_date)
        self.altitude = ephem_satellite.elevation / 1000 # in km
        self.longitude = ephem_satellite.sublon
        self.latitude = ephem_satellite.sublat

# getters
def get_ref_id(self):
    return self.id
def get_name(self):
    return self.name
def get_date(self):
    return self.date
def get_altitude(self):
    return self.altitude
def get_longitude(self):
    return self.longitude
def get_latitude(self):
    return self.latitude
def get_jb2008(self):
    return get_jb2008_density(self)
def get_tle1(self):
    return self.line1
def get_tle2(self):
    return self.line2

class prediction_epochs():
    def __init__(self, id):
        self.id = id
        self.ref_date = get_reference(id)[0]
        self.ref_alt = get_reference(id)[1]
        self.prediction_date
        self.prediction_alt
        self.reentry_date = get_reference(id)[4]
        self.prediction_delta = self.prediction_date - self.reentry_date

# getters
def get_prediction_id(self):
    return self.id
def get_prediction_date(self):
    return self.ref_date
def get_prediction_alt(self):
    return self.ref_alt

# returns tle object corresponding to reference altitude/data of satellite
def get_reference(id):
    with open("../data/epoch_masterlist.csv", 'r') as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)
        for row in csv_reader:
            if int(row[0]) == id:
                reference_date = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")
                reference_alt = float(row[2])
                reference_line1 = row[3]
                reference_line2 = row[4]
                reentry_date = datetime.strptime(row[5], "%Y-%m-%d %H:%M:%S%z")
                reentry_alt = float(row[6])
                return reference_date, reference_alt, reference_line1, reference_line2, reentry_date, reentry_alt

def get_predictions(tle):


def predict_100km(tle):
    id = get_ref_id(tle)
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
        file.write("ID,REFERENCE DATE,REFERENCE ALTITUDE (KM),PREDICTION DATE,PREDICTION ALTITUDE (KM),PREDICTION-REENTRY DELTA,REFERENCE JB2008 DENSITY\n")

        for instance in generate_reference_predictions_data(id):
            file.write(f"{get_ref_id(instance)},{get_ref_date(instance)},{get_ref_alt(instance)},{get_prediction_date(instance)},{get_prediction_alt(instance)},{get_prediction_delta(instance)},{get_jb2008_density(instance)}\n")

if __name__ == "__main__":
    from pyatmos import jb2008
    from pyatmos import download_sw_jb2008, read_sw_jb2008

    # compile lastest jb2008 data
    jb2008_swfile = download_sw_jb2008()
    jb2008_swdata = read_sw_jb2008(jb2008_swfile)

    if not os.path.exists("../data/starlink_reentries_2020_2025/epoch_files/"):
        os.makedirs("../data/starlink_reentries_2020_2025/epoch_files/")

    with open("../data/starlink_reentries_list.txt", "r") as file:
        # pass over headers
        next(file)
        count = 1
        for line in file:
            id = line.strip()
            # make sure file doesn't already exist
            if not os.path.exists(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv"):
                write_data_to_csv(id)
                print(f"{count}: {id}")
                count += 1