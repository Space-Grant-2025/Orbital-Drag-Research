import csv
import datetime
import ephem
import os

none_count = 0

class epochs:
    def __init__ (self, id, tle_instance_epoch, tle_instance_alt, ref_line1, ref_line2):
        self.tle_instance_epoch = tle_instance_epoch
        self.tle_instance_alt = tle_instance_alt
        self.prediction_alt = make_prediction(id, ref_line1, ref_line2, self.tle_instance_epoch)
        if self.prediction_alt is not None:
            self.delta_alt = tle_instance_alt - self.prediction_alt
        else:
            self.delta_alt = None
            global none_count
            none_count += 1

# getters
def get_tle_instance_epoch(self):
        return self.tle_instance_epoch
def get_tle_instance_alt(self):
        return self.tle_instance_alt
def get_prediction_alt(self):
    return self.prediction_alt
def get_delta_alt(self):
    return self.delta_alt

def make_prediction(id, ref_line1, ref_line2, current_date):
    # ephem object reads in given tle data
    satellite = ephem.readtle('NORAD' + str(id), ref_line1, ref_line2)
    str_date = datetime.datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")
    ephem_date = ephem.date(str_date)

    # compute satellite at date
    try:
        satellite.compute(ephem_date)
        altitude = satellite.elevation / 1000
        return altitude

    except RuntimeError:
        return None

def get_reference_epoch(target_id):
    with open(f"../data/epoch_masterlist.csv", "r") as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            current_id = int(row[0])
            if current_id == target_id:
                reference_epoch = row[1]
                ref_line1 = row[3]
                ref_line2 = row[4]
                return datetime.datetime.strptime(reference_epoch, "%Y-%m-%d %H:%M:%S%z"), ref_line1, ref_line2

def read_data_from_csv(id):
    epoch_list = []
    with open(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv", "r") as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        reference_epoch, ref_line1, ref_line2 = get_reference_epoch(id)
        for row in csv_reader:
            current_time = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            if current_time > reference_epoch:
                current_alt = float(row[2])
                epoch_object = epochs(id, current_time, current_alt, ref_line1, ref_line2)
                epoch_list.append(epoch_object)
    return epoch_list

def write_file(id):
    epoch_list = read_data_from_csv(id)
    with open(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv", "w") as file:
        file.write("TLE INSTANCE EPOCH,TLE INSTANCE ALTITUDE (KM),PREDICTION FROM REFERENCE EPOCH ALTITUDE (KM),PREDICTION DELTA (KM)\n")

        for epoch in epoch_list:
            file.write(f"{get_tle_instance_epoch(epoch)},{get_tle_instance_alt(epoch)},{get_prediction_alt(epoch)},{get_delta_alt(epoch)}\n")


def main():
    if not os.path.exists("../data/starlink_reentries_2020_2025/epoch_files"):
        os.makedirs("../data/starlink_reentries_2020_2025/epoch_files")

    with open("../data/starlink_reentries_list.txt", "r") as file:
        file.readline()
        count = 1
        for line in file:
            id = int(line)
            if os.path.exists(f"../data/starlink_reentries_list.txt/epoch_files/epoch_{id}.csv"):
                continue
            write_file(id)
            print(f"{count}: {id}")
            count += 1
    global none_count
    print("NONE COUNT: " + str(none_count))

if __name__ == "__main__":
    main()