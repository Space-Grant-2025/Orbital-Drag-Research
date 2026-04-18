import os
import statistics
from _csv import reader


class Reentered_Satellite():
    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        if row[2] == 'None':
            if os.path.exists(f"../data/other_reentries/human_readable/tle_{id}.csv"):
                with open(f"../data/other_reentries/human_readable/tle_{id}.csv") as file:
                    csv_reader = reader(file)
                    # pass over headers
                    next(csv_reader)
                    row1 = next(csv_reader)
                    self.launch_date = row1[0][:10]
            elif os.path.exists(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv"):
                with open(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv") as file:
                    csv_reader = reader(file)
                    # pass over headers
                    next(csv_reader)
                    row1 = next(csv_reader)
                    self.launch_date = row1[0][:10]
            else:
                self.launch_date = None
        else:
            self.launch_date = row[2]
        self.reentry_date = row[3]
        self.mass = row[4]
        self.avg_alt = find_avg_alt(id)


def find_avg_alt(id):
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