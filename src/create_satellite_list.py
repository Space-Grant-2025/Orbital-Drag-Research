from csv import reader
import datetime
import pyautogui

class satellite_mass:
    def __init__(self, id, name, launch_date, reentry_date, mass):
        self.id = id
        self.name = name
        self.launch_date = launch_date
        self.reentry_date = reentry_date
        self.mass = mass

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
def get_lifetime(self):
    return self.lifetime

def create_satellite_list():
    satellite_list = []
    with open(f'../data/payloads.csv', 'r') as mass_file:
        mass_reader = reader(mass_file)
        # pass over headers
        next(mass_reader)

        # create satellite object for every row in starlink_masses
        for row in mass_reader:
            satellite_id = int(row[0])
            name = row[1]
            if row[2] != '':
                satellite_launch_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
            else:
                satellite_launch_date = None
            if row[3] != '':
                satellite_reentry_date = datetime.datetime.strptime(row[3], "%Y-%m-%d").date()
            else:
                satellite_reentry_date = None

            with open('../data/mcdowell_satcat.csv', 'r') as satcat_file:
                satcat_reader = reader(satcat_file)
                # pass over headers
                next(satcat_reader)

                for row in satcat_reader:
                    if row[1].isdigit():
                        row_id = int(row[1])
                    if row_id == satellite_id:
                        # if space-track launch date is none, add mcdowell's launch date
                        if satellite_launch_date != '':
                            satellite_launch_date = create_date(row[7])
                        # if space-track reentry date is none, add mcdowell's reentry date
                        if satellite_reentry_date != '':
                            satellite_reentry_date = create_date(row[11])
                        if row[19].isdigit():
                            mass = int(row[19])
            print(satellite_launch_date)
            satellite = satellite_mass(satellite_id, name, satellite_launch_date, satellite_reentry_date, mass)
            satellite_list.append(satellite)
            pyautogui.press('shift')
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

def write_satellite_list_to_file():
    satellite_list = create_satellite_list()
    with open('../data/satellite_masses_list.csv', 'w') as satellite_file:
        satellite_file.write("NORAD CAT ID,NAME,LAUNCH DATE,REENTRY DATE,DRY MASS (KG)\n")
        for satellite in satellite_list:
            satellite_file.write(f"{get_id(satellite)},{get_name(satellite)},{get_launch_date(satellite)},{get_reentry_date(satellite)},{get_mass(satellite)}\n")

if __name__ == '__main__':
    write_satellite_list_to_file()