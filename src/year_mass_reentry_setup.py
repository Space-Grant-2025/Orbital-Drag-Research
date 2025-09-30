import datetime
import csv

end_of_may = datetime.date(2025, 5, 31)
MAX_MASS = 2000 #kg
MAX_ALTITUDE = 600 #km

class satellite_mass_lifetime:
    def __init__(self, row):
        self.id = int(row[0])
        self.name = row[1]
        self.launch_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
        self.reentry_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
        self.mass = float(row[4])
        if row[5] != 'None':
            self.altitude = float(row[5])
        else:
            self.altitude = None
        self.lifetime = self.reentry_date - self.launch_date

    # getters
    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_launch_date(self):
        return self.launch_date
    def get_reentry_date(self):
        return self.reentry_date
    def get_mass(self):
        return self.mass
    def get_altitude(self):
        return self.altitude
    def get_lifetime(self):
        return self.lifetime

def get_satellite_list():
    satellite_list = []
    with open("../data/all_reentries_info.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = satellite_mass_lifetime(row)
            # check critical values are not none
            if satellite.get_mass() is not None and satellite.get_launch_date() is not None and satellite.get_altitude() is not None:
                # check within year specification
                if satellite.get_launch_date() <= end_of_may:
                    # check within mass and altitude restrictions
                    if satellite.get_altitude() <= MAX_ALTITUDE and satellite.get_mass() <= MAX_MASS:
                        satellite_list.append(satellite)
    return satellite_list

def get_starlink_list():
    satellite_list = []
    with open("../data/all_reentries_info.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = satellite_mass_lifetime(row)
            # check critical values are not none
            if satellite.get_mass() is not None and satellite.get_launch_date() is not None and satellite.get_altitude() is not None:
                # check launch within year specification
                if satellite.get_launch_date() <= end_of_may:
                    # check within mass and altitude restrictions
                    if satellite.get_altitude() <= MAX_ALTITUDE and satellite.get_mass() <= MAX_MASS:
                        # check sat name
                        if 'STARLINK' in satellite.get_name():
                            satellite_list.append(satellite)
    return satellite_list

def get_not_starlink_list():
    satellite_list = []
    with open("../data/all_reentries_info.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = satellite_mass_lifetime(row)
            # check critical values are not none
            if satellite.get_mass() is not None and satellite.get_launch_date() is not None and satellite.get_altitude() is not None:
                # check within year specification
                if satellite.get_launch_date() <= end_of_may:
                    # check within mass and altitude restrictions
                    if satellite.get_altitude() <= MAX_ALTITUDE and satellite.get_mass() <= MAX_MASS:
                        # check sat name
                        if 'STARLINK' not in satellite.get_name():
                            satellite_list.append(satellite)
    return satellite_list

def make_year_dict(start_year, end_year):
    year_list = []
    for x in range(end_year - start_year + 1):
        year_list.append(start_year + x)
    year_nums = dict()
    for year in year_list:
        year_nums[year] = 0
    return year_nums

# returns launch_year, reentry_year adjusted for timeframe
def set_launch_reentry_from_timeframe(satellite, start_year, end_year):
    launch_year = int(satellite.get_launch_date().year)
    reentry_year = int(satellite.get_reentry_date().year)

    # orbits before or after timeframe
    if reentry_year < start_year or launch_year > end_year:
        launch_year = None
        reentry_year = None
    # launches before start year but reenters during timeframe
    elif launch_year <= start_year and start_year <= reentry_year <= end_year:
        launch_year = start_year
    # launches during timeframe but reenters after
    elif start_year <= launch_year <= end_year and reentry_year >= end_year:
        reentry_year = end_year
    # launches before and reenters after
    elif launch_year <= start_year and reentry_year >= end_year:
        launch_year = start_year
        reentry_year = end_year
    # otherwise, satellite launches and reenters within time frame

    return launch_year, reentry_year

# num sats orbiting throughout time period
def fill_year_dict_sat_nums(satellite_list, start_year, end_year):
    year_nums = make_year_dict(start_year, end_year)

    for satellite in satellite_list:

        launch_year, reentry_year = set_launch_reentry_from_timeframe(satellite, start_year, end_year)
        if launch_year is None or reentry_year is None:
            continue

        for x in range(reentry_year - launch_year + 1):
            year_nums[launch_year + x] += 1

    sat_nums = year_nums.values()
    sat_years = year_nums.keys()
    return sat_nums, sat_years

def fill_year_dict_launch_nums(satellite_list, start_year, end_year):
    year_launches = make_year_dict(start_year, end_year)

    # fill with num satellites
    for satellite in satellite_list:

        launch_date = satellite.get_launch_date()

        # check within data date specifications
        if launch_date <= end_of_may:
            launch_year = int(launch_date.year)
        else:
            continue

        # check within plot date specifications
        if start_year <= launch_year <= end_year:
            year_launches[launch_year] += 1

    launches_list = year_launches.values()
    year_list = year_launches.keys()

    return launches_list, year_list


def fill_year_dict_reentry_nums(satellite_list, start_year, end_year):
    year_reentries = make_year_dict(start_year, end_year)

    # fill with num satellites
    for satellite in satellite_list:

        reentry_date = satellite.get_reentry_date()

        # check within data date specifications
        if reentry_date <= end_of_may:
            reentry_year = int(reentry_date.year)
        else:
            continue

        # check within plot date specifications
        if start_year <= reentry_year <= end_year:
            year_reentries[reentry_year] += 1

    reentries_list = year_reentries.values()
    year_list = year_reentries.keys()

    return reentries_list, year_list

def fill_year_dict_mass(satellite_list, start_year, end_year):
    year_masses = make_year_dict(start_year, end_year)

    for satellite in satellite_list:
        mass = satellite.get_mass()

        launch_year, reentry_year = set_launch_reentry_from_timeframe(satellite, start_year, end_year)
        if launch_year is None or reentry_year is None:
            continue

        for x in range(reentry_year - launch_year + 1):
            year_masses[launch_year + x] += mass

    mass_list = year_masses.values()
    year_list = year_masses.keys()
    return mass_list, year_list
