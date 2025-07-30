import statistics
from csv import reader
import os

class reentered_satellite():
    def __init__(self, id, name, launch_date, reentry_date, mass, avg_alt):
        self.id = id
        self.name = name
        self.launch_date = launch_date
        self.reentry_date = reentry_date
        self.mass = mass
        self.avg_alt = avg_alt

def get_altitude_from_csv(id):
    altitude_list = []
    # check starlink 2020-2025
    if os.path.exists(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv"):
        with open(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv") as file:
            csv_reader = reader(file)
            # pass over headers
            next(csv_reader)

            for row in csv_reader:
                altitude_list.append(row[2])

    if os.path.exists(f"../data/other_reentries/human_readable/tle_{id}.csv"):
        with open(f"../data/other_reentries/human_readable/tle_{id}.csv") as file:
            csv_reader = reader(file)
            # pass over headers
            next(csv_reader)

            for row in csv_reader:
                altitude_list.append(row[2])

    return statistics.mean(altitude_list)

def make_sat_object(id):
    with open("../data/all_satellite_info.csv") as file:
        csv_reader = reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            if id == int(row[0]):
                id = row[0]
                name = row[1]
                launch_date = row[2]
                reentry_date = row[3]
                mass = row[4]
                avg_alt = get_altitude_from_csv(id)

                reentered_satellite(id, name, launch_date, reentry_date, mass, avg_alt)
    return reentered_satellite