import os
from csv import reader
from datetime import datetime

class satellite_data:
    def __init__(self, id, date, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time):
        self.id = id
        self.date = date
        self.altitude = altitude
        self.velocity = velocity
        self.longitude = longitude
        self.latitude = latitude
        self.jb2008 = jb2008
        self.nrlmsise = nrlmsise
        self.local_time = local_time

# getters
def get_id(self):
    return self.id
def get_date(self):
    return self.date
def get_altitude(self):
    return self.altitude
def get_velocity(self):
    return self.velocity
def get_longitude(self):
    return self.longitude
def get_latitude(self):
    return self.latitude
def get_jb2008(self):
    return self.jb2008
def get_nrlmsise(self):
    return self.nrlmsise
def get_local_time(self):
    return self.local_time

def gather_data_from_csv(id):
    # list of data points for one satellite
    satellite_list = []
    with open(f'../data/human_readable/tle_{id}.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)
        for row in csv_reader:
            date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            altitude = row[1]
            velocity = row[2]
            longitude = row[3]
            latitude = row[4]
            jb2008 = row[5]
            nrlmsise = row[6]
            local_time = row[7]

            satellite_instance = satellite_data(id, date, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time)
            satellite_list.append(satellite_instance)
    return satellite_list