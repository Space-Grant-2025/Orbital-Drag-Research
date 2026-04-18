import csv
import datetime
import os
from epoch_sat_obj import Epoch

none_count = 0

def get_reference_epoch(target_id):
    with open(f"../../data/epoch_masterlist.csv", "r") as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        for row in csv_reader:
            current_id = int(row[0])
            if current_id == target_id:
                reference_epoch = datetime.datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S%z")
                ref_line1 = row[3]
                ref_line2 = row[4]
                return reference_epoch, ref_line1, ref_line2
    return None, None, None

def read_data_from_csv(id):
    epoch_list = []
    with open(f"../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv", "r") as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)

        reference_epoch, ref_line1, ref_line2 = get_reference_epoch(id)
        for row in csv_reader:
            current_time = datetime.datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S%z")
            if current_time >= reference_epoch:
                current_alt = float(row[2])
                instance_line1 = row[9]
                instance_line2 = row[10]
                epoch_object = Epoch(id, current_time, current_alt, ref_line1, ref_line2, instance_line1, instance_line2)
                epoch_list.append(epoch_object)
    return epoch_list

def write_file(id):
    epoch_list = read_data_from_csv(id)
    with open(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv", "w") as file:
        file.write("TLE INSTANCE EPOCH,TLE INSTANCE ALTITUDE (KM),TLE INSTANCE LINE 1,TLE INSTANCE LINE 2,PREDICTION FROM REFERENCE EPOCH ALTITUDE (KM),PREDICTION DELTA (KM)\n")

        for epoch in epoch_list:
            file.write(f"{epoch.get_tle_instance_epoch()},{epoch.get_tle_instance_alt()},{epoch.get_instance_line1()},{epoch.get_instance_line2()},{epoch.get_prediction_alt()},{epoch.get_delta_alt()}\n")


def main():
    if not os.path.exists("../../data/starlink_reentries_2020_2025/epoch_files"):
        os.makedirs("../../data/starlink_reentries_2020_2025/epoch_files")

    with open("../../data/starlink_reentries_list.txt", "r") as file:
        file.readline()
        count = 1
        for line in file:
            id = int(line)
            if os.path.exists(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv"):
                continue
            write_file(id)
            print(f"{count}: {id}")
            count += 1
    global none_count
    print("NONE COUNT: " + str(none_count))

if __name__ == "__main__":
    main()