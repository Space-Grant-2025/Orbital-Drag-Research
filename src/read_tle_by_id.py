import datetime
import os
import re
import ephem
import math
import pyautogui
from ephem import EarthSatellite

# inverse flattening at each pole for Earth ellipsoid (WGS 84)
flattening = 1. / 298.257223563
# eccentricity squared of WGS 84 orbit
eccentricity2 = 2 * flattening * (1 - flattening)

# gravitational constant
grav = 6.6743e-11
# mass of Earth
earth_mass = 5.9722e24

class ephem_tle:
    def __init__(self, id, line0, line1, line2):
        # ephem object reads in given tle data
        ephem_satellite = ephem.readtle('NORAD' + str(id), line1, line2)

        # assign values
        self.id = id
        self.name = line0[1:]
        self.tle_line1 = line1
        self.tle_line2 = line2

        # process date
        self.date = get_date_from_tle(line1)
        str_date = datetime.datetime.strftime(self.date,"%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # propagate flight data
        try:
            ephem_satellite.compute(ephem_date)
            self.latitude = ephem_satellite.sublat
            self.longitude = ephem_satellite.sublong
            self.altitude = ephem_satellite.elevation / 1000 # in km
            self.mean_motion = 2 * math.pi * float(line2[52:62]) / 86400.
            self.velocity = (grav * earth_mass * self.mean_motion) ** (1 / 3.) * 1e-3
        except RuntimeError:
            self.latitude = None
            self.longitude = None
            self.altitude = None
            self.mean_motion = None
            self.velocity = None

    # getters
    def get_id(self):
        return self.id
    def get_line1(self):
        return self.tle_line1
    def get_line2(self):
        return self.tle_line2
    def get_name(self):
        return self.name
    def get_tle_line1(self):
        return self.tle_line1
    def get_tle_line2(self):
        return self.tle_line2
    def get_date(self):
        return self.date
    def get_altitude(self):
        return self.altitude
    def get_velocity(self):
        return self.velocity
    def get_mean_motion(self):
        return self.mean_motion
    def get_latitude(self):
        return self.latitude
    def get_longitude(self):
        return self.longitude


    def get_utc(self):
        return self.date.timestamp()
    def get_day_of_year(self):
        return self.date.timetuple().tm_yday

# computes local time as a function of day of year, geographic longitude, and universal time using the equation of time (EoT).
def get_local_time(day_of_year, longitude, utc):
    if longitude is None:
        return None
    if longitude < 0:
        longitude = 360 + longitude

    B = (day_of_year - 81) * 360.0 / 365.0
    equation_of_time = 9.87 * math.sin(2 * B) - 7.53 * math.cos(B) - 1.5 * math.sin(B)

    lt = int(longitude / 15.)
    lstm = 15. * (lt - utc)
    tc = 4. * (longitude - lstm) + equation_of_time
    local_time = abs(lt + tc / 60.)

    if local_time >= 24:
        local_time = local_time - 24

    if local_time < 0:
        local_time = local_time + 24

    return local_time

def get_jb2008_density(tle):
    tle_date = tle.get_date()
    tle_date = tle_date.strftime("%Y-%m-%d %H:%M:%S")
    jb08 = jb2008(tle_date, (tle.get_latitude(), tle.get_longitude(), tle.get_altitude()), jb2008_swdata)
    density = jb08.rho
    return str(density)

def get_nrlmsise_density(tle):
    tle_date = tle.get_date().strftime("%Y-%m-%d %H:%M:%S")
    nrlmsise = nrlmsise00(tle_date, (tle.get_latitude(), tle.get_longitude(), tle.get_altitude()), nrlmsise_swdata)
    density = nrlmsise.rho
    return str(density)

# gets in the float representing the date on the first line of the tle and returns datetime object
def get_date_from_tle(line1):
    find_date = re.compile('\\d{5}\\.\\d{8}')
    tle_date = find_date.search(line1).group()

    year = 0
    # checks if the year listed is before 2000 (not necessary, but good practice)
    if int(tle_date[:2]) > 50:
        year = 1900 + int(tle_date[:2])
    else:
        year = 2000 + int(tle_date[:2])
    # holds the day of year and fraction of day
    total_days = float(tle_date[2:])

    # fraction represents the fraction of the day
    fraction = total_days - int(total_days)
    total_days = math.trunc(total_days)

    # converts number of days in year to day and month
    month = int(datetime.datetime.strptime(f"{year} {total_days}", '%Y %j').strftime('%m'))
    day = int(datetime.datetime.strptime(f"{year} {total_days}",'%Y %j').strftime('%d'))

    # converts fraction of day into human_readable
    hour = int(fraction * 24)
    min = int(fraction * 1440 - hour * 60)
    sec = int(fraction * 86400 - hour * 3600 - min * 60)

    # create datetime object
    date = datetime.datetime(year, month, day, hour, min, sec, tzinfo=datetime.timezone.utc)

    # millisecs and rounding secs for more precision
    millisecs = fraction * 86400 - hour * 3600 - min * 60 - sec

    if millisecs >= .5:
        date = date + datetime.timedelta(0, 1)

    return date

# creates flight data for date in given tle and adds the values to lists
def process_starlink_tle_data(id):
    tle_list = []
    with open('../data/starlink_reentries_2020_2025/starlink_tles/tle_' + str(id) + '.txt') as data:
        # list of all the lines
        lines = data.readlines()[:]
    data.close()

    for x in range(0, len(lines), 3):
        # create tle object and add to list
        line0 = lines[x].strip("\n")
        line1 = lines[x + 1].strip("\n")
        line2 = lines[x + 2].strip("\n")
        data = ephem_tle(id, line0, line1, line2)
        tle_list.append(data)
    return tle_list

def process_other_tle_data(id):
    tle_list = []
    with open('../data/other_reentries/other_tles/tle_' + str(id) + '.txt') as data:
        # list of all the lines
        lines = data.readlines()[:]
    data.close()

    for x in range(0, len(lines), 3):
        # create tle object and add to list
        line0 = lines[x].strip("\n")
        line1 = lines[x + 1].strip("\n")
        line2 = lines[x + 2].strip("\n")
        data = ephem_tle(id, line0, line1, line2)
        tle_list.append(data)
    return tle_list

def write_starlink_data_to_csv(id, tle_list):
    with open('../data/starlink_reentries_2020_2025/human_readable/tle_' + str(id) + '.csv', 'w') as file:

        file.write("DATE,NAME,ALTITUDE,VELOCITY,LATITUDE,LONGITUDE,JB2008 DENSITY,NRLMSISE00 DENSITY,LOCAL TIME,TLE LINE 1,TLE LINE 2\n")

        for tle in tle_list:
            # write values to file
            file.write(f'{str(tle.get_date())},{tle.get_name()},{tle.get_altitude()},{tle.get_velocity()},{tle.get_latitude()},{tle.get_longitude()},{get_jb2008_density(tle)}, {get_nrlmsise_density(tle)}, {get_local_time(tle.get_day_of_year(), tle.get_longitude(), tle.get_utc())},{tle.get_line1()},{tle.get_line2()}\n')

def write_other_data_to_csv(id, tle_list):
    with open('../data/other_reentries/human_readable/tle_' + str(id) + '.csv', 'w') as file:

        file.write("DATE,NAME,ALTITUDE,LATITUDE,LONGITUDE,LOCAL TIME,TLE LINE 1,TLE LINE 2\n")
        tle_list = sorted(tle_list, key=lambda tle: tle.date)
        for tle in tle_list:
            # write values to file
            file.write(f'{str(tle.get_date())},{tle.get_name()},{tle.get_altitude()},{tle.get_latitude()},{tle.get_longitude()},{get_local_time(tle.get_day_of_year(), tle.get_longitude(), tle.get_utc())},{tle.get_line1},{tle.get_line2}\n')

def read_starlink_tles():
    start_time = datetime.datetime.now()
    with open('../data/starlink_reentries_list.txt', 'r') as file:

        if not os.path.exists("../data/starlink_reentries_2020_2025/human_readable/"):
            os.makedirs("../data/starlink_reentries_2020_2025/human_readable/")

        # pass over headers
        file.readline()

        # progress tracker
        count = 1
        # loop through norad ids and create file of tle data
        for id in file:
            id = int(id.strip())

            if os.path.exists("../data/starlink_reentries_2020_2025/human_readable/tle_" + str(id) + ".csv"):
                continue

            # create new satellite object and write data to file
            write_starlink_data_to_csv(id, process_starlink_tle_data(id))

            # jitter to keep computer awake
            pyautogui.press('shift')

            # progress tracker
            print(f'{count}: {id}')
            count += 1

    # prints total time program takes to run because i'm curious
    end_time = datetime.datetime.now()
    print(str(f'Finished Starlink TLES: {end_time - start_time}'))

def read_other_tles():
    start_time = datetime.datetime.now()
    with open('../data/other_reentries_list.txt', 'r') as file:

        if not os.path.exists("../data/other_reentries/human_readable/"):
            os.makedirs("../data/other_reentries/human_readable/")

        # progress tracker
        count = 1
        # loop through norad ids and create file of tle data
        for id in file:
            id = int(id.strip())
            # check not starlink reentry 2020 to 2025
            if os.path.exists(f"../data/starlink_reentries_2020_2025/starlink_tles/tle_{id}.txt"):
                continue
            # check file doesn't exist already
            if os.path.exists("../data/other_reentries/human_readable/tle_" + str(id) + ".csv"):
                continue

            # create new satellite object and write data to file
            write_other_data_to_csv(id, process_other_tle_data(id))

            # jitter to keep computer awake
            pyautogui.press('shift')

            # progress tracker
            print(f'{count}: {id}')
            count += 1

    # prints total time program takes to run because i'm curious
    end_time = datetime.datetime.now()
    print(str(f'Finished Other TLES: {end_time - start_time}'))

if __name__ == '__main__':
    from pyatmos import jb2008, nrlmsise00
    from pyatmos import download_sw_jb2008, read_sw_jb2008
    from pyatmos import download_sw_nrlmsise00, read_sw_nrlmsise00

    # compile lastest jb2008 data
    jb2008_swfile = download_sw_jb2008()
    jb2008_swdata = read_sw_jb2008(jb2008_swfile)

    # compile lastest nrlmsise00 data
    nrlmsise_swfile = download_sw_nrlmsise00()
    nrlmsise_swdata = read_sw_nrlmsise00(nrlmsise_swfile)



    read_starlink_tles()
    read_other_tles()
