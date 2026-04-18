import datetime
import os
import math
import pyautogui
from tle_to_sat_obj import Satellite

# inverse flattening at each pole for Earth ellipsoid (WGS 84)
FLATTENING = 1. / 298.257223563
# eccentricity squared of WGS 84 orbit
ECCENTRICTIY_2 = 2 * FLATTENING * (1 - FLATTENING)

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


# creates flight data for date in given tle and adds the values to lists
def process_starlink_tle_data(id):
    tle_list = []
    with open('../../data/starlink_reentries_2020_2025/starlink_tles/tle_' + str(id) + '.txt') as data:
        # list of all the lines
        lines = data.readlines()[:]
    data.close()

    for x in range(0, len(lines), 3):
        # create tle object and add to list
        line0 = lines[x].strip("\n")
        line1 = lines[x + 1].strip("\n")
        line2 = lines[x + 2].strip("\n")
        data = Satellite(id, line0, line1, line2)
        tle_list.append(data)
    return tle_list

def process_other_tle_data(id):
    tle_list = []
    with open('../../data/other_reentries/other_tles/tle_' + str(id) + '.txt') as data:
        # list of all the lines
        lines = data.readlines()[:]
    data.close()

    for x in range(0, len(lines), 3):
        # create tle object and add to list
        line0 = lines[x].strip("\n")
        line1 = lines[x + 1].strip("\n")
        line2 = lines[x + 2].strip("\n")
        data = Satellite(id, line0, line1, line2)
        tle_list.append(data)
    return tle_list

def write_starlink_data_to_csv(id, tle_list):
    with open('../../data/starlink_reentries_2020_2025/human_readable/tle_' + str(id) + '.csv', 'w') as file:

        file.write("DATE,NAME,ALTITUDE,VELOCITY,LATITUDE,LONGITUDE,JB2008 DENSITY,NRLMSISE00 DENSITY,LOCAL TIME,TLE LINE 1,TLE LINE 2\n")

        for tle in tle_list:
            # write values to file
            file.write(f'{str(tle.get_date())},{tle.get_name()},{tle.get_altitude()},{tle.get_velocity()},{tle.get_latitude()},{tle.get_longitude()},{get_jb2008_density(tle)}, {get_nrlmsise_density(tle)}, {get_local_time(tle.get_day_of_year(), tle.get_longitude(), tle.get_utc())},{tle.get_line1()},{tle.get_line2()}\n')

def write_other_data_to_csv(id, tle_list):
    with open('../../data/other_reentries/human_readable/tle_' + str(id) + '.csv', 'w') as file:

        file.write("DATE,NAME,ALTITUDE,LATITUDE,LONGITUDE,LOCAL TIME,TLE LINE 1,TLE LINE 2\n")
        tle_list = sorted(tle_list, key=lambda tle: tle.date)
        for tle in tle_list:
            # write values to file
            file.write(f'{str(tle.get_date())},{tle.get_name()},{tle.get_altitude()},{tle.get_latitude()},{tle.get_longitude()},{get_local_time(tle.get_day_of_year(), tle.get_longitude(), tle.get_utc())},{tle.get_line1},{tle.get_line2}\n')

def read_starlink_tles():
    start_time = datetime.datetime.now()
    with open('../../../data/starlink_reentries_list.txt', 'r') as file:

        if not os.path.exists("../../../data/starlink_reentries_2020_2025/human_readable/"):
            os.makedirs("../../../data/starlink_reentries_2020_2025/human_readable/")

        # pass over headers
        file.readline()

        # progress tracker
        count = 1
        # loop through norad ids and create file of tle data
        for id in file:
            id = int(id.strip())

            if os.path.exists("../../data/starlink_reentries_2020_2025/human_readable/tle_" + str(id) + ".csv"):
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
    with open('../../../data/other_reentries_list.txt', 'r') as file:

        if not os.path.exists("../../data/other_reentries/human_readable/"):
            os.makedirs("../../data/other_reentries/human_readable/")

        # progress tracker
        count = 1
        # loop through norad ids and create file of tle data
        for id in file:
            id = int(id.strip())
            # check not starlink reentry 2020 to 2025
            if os.path.exists(f"../../data/starlink_reentries_2020_2025/starlink_tles/tle_{id}.txt"):
                continue
            # check file doesn't exist already
            if os.path.exists("../../data/other_reentries/human_readable/tle_" + str(id) + ".csv"):
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
    #read_other_tles()
