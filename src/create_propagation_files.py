from create_epoch_files import *
from src.read_tle_by_id import get_date_from_tle

none_count = 0

class satellite_prediction():
    def __init__(self, id, ref_line1, ref_line2):

        self.id = id
        self.ref_epoch = get_date_from_tle(ref_line1)
        ephem_date = self.ref_epoch.strftime("%Y-%m-%d %H:%M:%S")

        ref_satellite = ephem.readtle('NORAD' + str(id), ref_line1, ref_line2)
        ref_satellite.compute(ephem_date)

        self.ref_alt = ref_satellite.elevation / 1000
        self.pred_epoch, self.pred_alt = predict_100km(self.id, ref_line1, ref_line2, self.ref_epoch)

# getters
def get_id(self):
    return self.id
def get_ref_epoch(self):
    return self.ref_epoch
def get_ref_alt(self):
    return self.ref_alt
def get_pred_epoch(self):
    return self.pred_epoch
def get_pred_alt(self):
    return self.pred_alt

twelve_hours = datetime.timedelta(hours=12)
six_months = datetime.timedelta(days=182)

def get_satellite_data(id):
    data_list = []

    with open(f"../data/starlink_reentries_2020_2025/epoch_files/epoch_{id}.csv", "r") as file:
        csv_reader = csv.reader(file)
        # pass over headers
        next(csv_reader)
        for row in csv_reader:
            ref_line1 = row[2]
            ref_line2 = row[3]
            satellite_data = satellite_prediction(id, ref_line1, ref_line2)
            data_list.append(satellite_data)

    return data_list


def predict_100km(id, ref_line1, ref_line2, ref_epoch):
    global none_count
    # starting alt higher than starlink sat
    altitude = 999999
    epoch = ref_epoch
    sat = ephem.readtle('NORAD' + str(id), ref_line1, ref_line2)

    while altitude > 110:
        try:
            ephem_epoch = epoch.strftime("%Y-%m-%d %H:%M:%S")
            sat.compute(ephem_epoch)
            altitude = sat.elevation / 1000
            epoch += twelve_hours
        except:
            none_count += 1
            return None, None

    return epoch, altitude

def write_data(id):
    data_list = get_satellite_data(id)

    with open(f"../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv", "w") as file:
        file.write("EPOCH (BEGINNING WITH REFERENCE TLE),ALTITUDE (KM),PREDICTION EPOCH,PREDICTION ALT (KM)\n")

        for item in data_list:
            file.write(f"{get_ref_epoch(item)},{get_ref_alt(item)},{get_pred_epoch(item)},{get_pred_alt(item)}\n")

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
    print(f"None Count: {none_count}")

main()