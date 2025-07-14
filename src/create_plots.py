from csv import reader

import matplotlib
import matplotlib.pyplot as plot
from matplotlib.ticker import LinearLocator

class satellite_data:
    def __init__(self, id, date, altitude, longitude, latitude, jb2008, nrlmsise, local_time):
        self.id = id
        self.date = date
        self.altitude = altitude
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
    satellite_list = []
    with open('../data/human_readable/tle_' + str(id) + '.csv', 'r') as file:
        csv_reader = reader(file)
        # pass over header line
        next(csv_reader)
        for row in csv_reader:
            date = row[0]
            altitude = row[1]
            longitude = row[2]
            latitude = row[3]
            jb2008 = row[4]
            nrlmsise = row[5]
            local_time = row[6]

            satellite = satellite_data(id, date, altitude, longitude, latitude, jb2008, nrlmsise, local_time)
            satellite_list.append(satellite)
    return satellite_list

def plot_density_altitude(satellite_list):

    with plot.rc_context({'axes.autolimit_mode': 'round_numbers'}):
        jb2008_list, altitude_list = zip(*[(get_jb2008(x), get_altitude(x)) for x in satellite_list])
        plot.plot(jb2008_list, altitude_list)
        plot.ylabel("Altitude [km]")
        plot.xlabel("JB2008 Density")
        plot.title("NORAD CAT ID " + str(get_id(satellite_list[0])))
        plot.show()

if __name__ == '__main__':
    plot_density_altitude(gather_data_from_csv(44235))