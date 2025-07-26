from csv import reader
from datetime import datetime
import datetime
from create_reentry_plots import f10, gather_f10_data

class satellite_reentry:
    def __init__(self, id, date, name, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time):
        self.id = id
        self.date = date
        self.name = name
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
def get_name(self):
    return self.name
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
            date = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            name = row[1]
            altitude = row[2]
            velocity = row[3]
            longitude = row[4]
            latitude = row[5]
            jb2008 = row[6]
            nrlmsise = row[7]
            local_time = row[8]

            satellite_instance = satellite_reentry(id, date, name, altitude, velocity, longitude, latitude, jb2008, nrlmsise, local_time)
            satellite_list.append(satellite_instance)
    return satellite_list

class satellite_mass:
    def __init__(self, id, name, payload, launch_date, reentry_date, mass, dry_mass):
        self.id = id
        self.name = name
        self.payload = payload
        self.launch_date = create_date(launch_date)
        self.reentry_date = create_date(reentry_date)
        self.mass = mass
        self.dry_mass = dry_mass
        if self.reentry_date is not None and self.launch_date is not None:
            self.lifetime = self.reentry_date - self.launch_date
        else:
            self.lifetime = None

# getters
def get_id(self):
    return self.id
def get_name(self):
    return self.name
def get_payload(self):
    return self.payload
def get_launch_date(self):
    return self.launch_date
def get_reentry_date(self):
    return self.reentry_date
def get_mass(self):
    return self.mass
def get_dry_mass(self):
    return self.dry_mass
def get_lifetime(self):
    return self.lifetime

# type should be "all" or "starlink"
def get_satellite_list(type):
    satellite_list = []
    with open(f'../data/{type}_masses.csv', 'r') as mass_file:
        csv_reader = reader(mass_file)
        # pass over headers
        next(csv_reader)

        # create satellite object for every row in starlink_masses
        for row in csv_reader:
            if row[0].isdigit():
                id = int(row[0])
            else:
                id = None
            name = row[1]
            payload = row[2]
            if row[3] != "-":
                launch_date = row[3]
            else:
                launch_date = None
            if row[4] != "-":
                reentry_date = row[4]
            else:
                reentry_date = None
            if row[5].isdigit():
                mass = int(round(float(row[5])))
            else:
                mass = None
            if row[6].isdigit():
                dry_mass = int(round(float(row[6])))
            else:
                dry_mass = None

            satellite = satellite_mass(id, name, payload, launch_date, reentry_date, mass, dry_mass)
            satellite_list.append(satellite)
    return satellite_list

def create_date(date_str):
    if date_str is not None:
        if len(date_str) >= 10:
            date_str = date_str[:11]
            year = int(date_str[:4])
            month = date_str[5:8]
            day = int(date_str[9:11].strip())
            date = datetime.datetime.strptime(f'{year}-{month}-{day}', "%Y-%b-%d").date()
            return date
        elif len(date_str) == 5:
            date_str = date_str[:4]
            year = int(date_str[:4])
            date = datetime.date(year, 1, 1)
            return date
        else:
            return None
    return None