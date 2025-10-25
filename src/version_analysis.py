from datetime import datetime
from datetime import date
import csv
import matplotlib.pyplot as plt

end_of_may = date(2025, 5, 31)
min_date = date.today()

class satellite_version:
    def __init__(self, row):
        self.id = int(row[0])
        self.name = row[1]

        # launch and reentry dates
        if row[2] != "None":
            self.launch_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        else:
            self.launch_date = None
        if row[3] != "None":
            self.reentry_date = datetime.strptime(row[3], "%Y-%m-%d").date()
        else:
            self.reentry_date = None

        # mass and altitude
        self.mass = float(row[4])
        if row[5] != 'None':
            self.altitude = row[5]
        else:
            self.altitude = None

        # lifetime
        if self.reentry_date == None or self.launch_date == None:
            self.lifetime = None
        else:
            self.lifetime = self.reentry_date - self.launch_date

        # assign pl_name
        start_index = len("Starlink ")
        end_index = row[6].find("-")
        self.pl_name = row[6][start_index:end_index]

        # assign version
        self.version = 'None'
        if "V0.9" in self.pl_name:
            self.version = "v0.9"
        if "V1.0" in self.pl_name:
            self.version = "v1"
        match self.pl_name[len("Group "):]:
            case "2":
                self.version = "v1.5"
            case "3":
                self.version = "v1.5"
            case "4":
                self.version = "v1.5"
            case "5":
                self.version = "v1.5"
            case "6":
                self.version = "v2 mini"
            case "7":
                self.version = "v2 mini"
            case "8":
                self.version = "v2 mini"
            case "9":
                self.version = "v2 mini"
            case "10":
                self.version = "v2 mini"
            case "11":
                self.version = "v2 mini"
            case "12":
                self.version = "v2 mini"
            case "13":
                self.version = "v2 mini"
            case "15":
                self.version = "v2 mini"
            case "17":
                self.version = "v2 mini"
            case "N":
                self.version = "v2 mini"
        if "TINTIN" in self.name:
            self.version = "v0.1"
        if self.launch_date == date(2021, 6, 30):
            self.version = "v1.5"
        if self.launch_date == date(2021, 1, 24):
            self.version = "v1"


def make_list():
    global min_date
    sat_list = []
    with open("../data/all_satellite_info.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "Starlink" in row[6]:
                sat = satellite_version(row)
                if sat.launch_date < min_date:
                    min_date = sat.launch_date
                if sat.launch_date <= end_of_may:
                    sat_list.append(sat)
    print(min_date)
    return sat_list


def make_graph():
    version_masses = ['227kg', '260kg', '306kg', '1240kg']
    # version, num
    sat_dict = {"v0.9": 0, "v1": 0, "v1.5": 0, "v2 mini": 0}
    for sat in make_list():
        if sat.version != "None" and sat.version != "v0.1":
            sat_dict[sat.version] += 1
        else:
            print(sat.version)
    plt.title(f"Starlink Satellite Versions (n = {sum(sat_dict.values())})")
    plt.xlabel("Starlink Version")
    plt.ylabel("Counts")
    plt.bar(sat_dict.keys(), sat_dict.values(), label = version_masses, color = ["blue", "green", "orange", "red"])
    plt.legend()
    plt.savefig("../data/mass_graphs/starlink_versions.png")

make_graph()