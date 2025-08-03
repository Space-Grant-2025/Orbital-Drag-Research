import statistics
from csv import reader
import os

class reentered_satellite():
    def __init__(self, id, name, launch_date, reentry_date, mass):
        self.id = id
        self.name = name
        self.launch_date = launch_date
        self.reentry_date = reentry_date
        self.mass = mass
        self.avg_alt = create_avg_alt(id)

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
def get_avg_alt(self):
    return self.avg_alt

def create_avg_alt(id):
    altitude_list = []
    # check starlink 2020-2025
    if os.path.exists(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv"):
        with open(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv") as file:
            csv_reader = reader(file)
            # pass over headers
            next(csv_reader)

            for row in csv_reader:
                if row[2] != 'None':
                    altitude_list.append(float(row[2]))

    if os.path.exists(f"../data/other_reentries/human_readable/tle_{id}.csv"):
        with open(f"../data/other_reentries/human_readable/tle_{id}.csv") as file:
            csv_reader = reader(file)
            # pass over headers
            next(csv_reader)

            for row in csv_reader:
                if row[2] != 'None':
                    altitude_list.append(float(row[2]))

    try:
        avg_alt = statistics.mean(altitude_list)
    except statistics.StatisticsError:
        avg_alt = None
    return avg_alt


def make_sat_object(row):
    id = row[0]
    name = row[1]
    launch_date = row[2]
    reentry_date = row[3]
    mass = row[4]

    return reentered_satellite(id, name, launch_date, reentry_date, mass)

def make_sat_list():
    satellite_list = []

    with open('../data/other_reentries_list.txt', 'r') as reentries:
        count = 1

        for line in reentries:
            id = line.strip()

            with open("../data/all_satellite_info.csv", "r") as file:
                csv_reader = reader(file)
                # pass over headers
                next(csv_reader)

                for row in csv_reader:
                    if row[0] == id:
                        satellite = make_sat_object(row)
                        satellite_list.append(satellite)
                        print(f"{count}: {id}")
                        count += 1

    return satellite_list

def write_sat_list_to_file():
    satellite_list = make_sat_list()

    with open('../data/reentries_info.csv', 'w') as file:
        file.write("ID,NAME,LAUNCH_DATE,REENTRY_DATE,MASS,MEAN ALTITUDE (KM)\n")
        for satellite in satellite_list:
            file.write(f"{get_id(satellite)},{get_name(satellite)},{get_launch_date(satellite)},{get_reentry_date(satellite)},{get_mass(satellite)},{get_avg_alt(satellite)}\n")

if __name__ == '__main__':
    write_sat_list_to_file()