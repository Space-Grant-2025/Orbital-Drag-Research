from csv import reader
from reentered_sat_obj import Reentered_Satellite as Satellite

def make_sat_list():
    satellite_list = []

    with open('../../data/other_reentries_list.txt', 'r') as reentries:
        count = 1

        for line in reentries:
            id = line.strip()

            with open("../../data/all_satellite_info.csv", "r") as file:
                csv_reader = reader(file)
                # pass over headers
                next(csv_reader)

                for row in csv_reader:
                    if row[0] == id:
                        satellite = Satellite(row)
                        satellite_list.append(satellite)
                        print(f"{count}: {id}")
                        count += 1

    return satellite_list

def write_sat_list_to_file():
    satellite_list = make_sat_list()

    with open('../../data/all_reentries_info.csv', 'w') as file:
        file.write("ID,NAME,LAUNCH_DATE,REENTRY_DATE,MASS,MEAN ALTITUDE (KM)\n")
        for sat in satellite_list:
            file.write(f"{sat()},{sat.get_name()},{sat.get_launch_date()},{sat.get_reentry_date()},{sat.get_mass()},{sat.get_avg_alt()}\n")

if __name__ == '__main__':
    write_sat_list_to_file()