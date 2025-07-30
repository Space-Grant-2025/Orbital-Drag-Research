from csv import reader
from create_mass_lifetime_plots import *

def get_all_reentries_list():
    start_year = 1957
    end_year = 2025
    satellite_list = []
    with open("../data/all_satellite_info.csv", "r") as file:
        reader = csv.reader(file)
        # pass over headers
        next(reader)
        for row in reader:
            satellite = make_sat_object(row)
            # make sure within year specification
            if get_reentry_date(satellite) is not None and get_launch_date(satellite) is not None and get_reentry_date(satellite) <= end_of_may:
                if start_year <= get_launch_date(satellite).year <= end_year:
                    satellite_list.append(satellite)
    return satellite_list

def write_reentries_to_file():
    satellite_list = get_all_reentries_list()
    with open(f"../data/other_reentries_list.txt", "w") as file:
        for satellite in satellite_list:
            if "STARLINK" not in get_name(satellite):
                file.write(f"{get_id(satellite)}\n")

if __name__ == "__main__":
    write_reentries_to_file()