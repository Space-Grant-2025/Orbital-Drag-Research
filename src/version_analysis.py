from datetime import datetime
import csv

class satellite_version:
    def __init__(self, row):
        self.id = int(row[0])
        self.name = row[1]
        if row[2] != "None":
            self.launch_date = datetime.strptime(row[2], "%Y-%m-%d").date()
        else:
            self.launch_date = None
        if row[3] != "None":
            self.reentry_date = datetime.strptime(row[3], "%Y-%m-%d").date()
        else:
            self.reentry_date = None
        self.mass = float(row[4])
        if row[5] != 'None':
            self.altitude = row[5]
        else:
            self.altitude = None
        if self.reentry_date == None or self.launch_date == None:
            self.lifetime = None
        else:
            self.lifetime = self.reentry_date - self.launch_date

        start_index = len("Starlink ")
        end_index = row[6].find("-")
        self.pl_name = row[6][start_index:end_index]

        self.version = None

        # match pl_name
        if "V0.9" in self.pl_name:
            self.version = "v0.9"
        if "V1.0" in self.pl_name:
            self.version = "v1"
        # match groups
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
        # match name
        if "TINTIN" in self.name:
            self.version = "v0.1"




def make_list():
    with open("../data/all_satellite_info.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if "Starlink" in row[6]:
                sat = satellite_version(row)
                if sat.version == None:
                    print(sat.name)
make_list()