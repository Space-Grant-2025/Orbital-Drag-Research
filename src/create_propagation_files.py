from create_epoch_files import *

twelve_hours = datetime.timedelta(hours=12)
six_months = datetime.timedelta(days=182)

def get_satellite_data(id):
    epoch_list = []
    alt_list = []

    reference_epoch, ref_line1, ref_line2 = get_reference_epoch(id)
    reference_epoch = datetime.datetime(reference_epoch.year, reference_epoch.month, reference_epoch.day, reference_epoch.hour, reference_epoch.minute, reference_epoch.second)
    satellite = ephem.readtle('NORAD' + str(id), ref_line1, ref_line2)

    # starting value that is higher than any starlink sat will be
    altitude = 9999999
    current_epoch = reference_epoch

    while altitude > 100 and current_epoch <= (reference_epoch + six_months):
        satellite.compute(str(current_epoch))
        # in km
        altitude = satellite.elevation / 1000

        epoch_list.append(current_epoch)
        alt_list.append(altitude)

        current_epoch += twelve_hours

    return epoch_list, alt_list

def write_data(id):
    epoch_list, alt_list = get_satellite_data(id)

    with open(f"../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv", "w") as file:
        file.write("EPOCH (BEGINNING WITH REFERENCE TLE),ALTITUDE (KM)\n")

        for x in range(len(epoch_list)):
            file.write(f"{epoch_list[x]},{alt_list[x]}\n")

def main():
    if not os.path.exists("../data/starlink_reentries_2020_2025/propagations"):
        os.makedirs("../data/starlink_reentries_2020_2025/propagations")

    with open("../data/starlink_reentries_list.txt", "r") as file:
        # pass over headers
        next(file)

        for line in file:
            id = int(line)
            print(id)
            write_data(id)
main()