import glob
from special_tools import day2doy
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from colormaps import plasma_w, idl39_w

class SevereEvent:
    def __init__(self, id):
        df = pd.read_csv(f"../data/starlink_reentries_2020_2025/propagations/propagation_{id}.csv")
        self.ref_epochs = str_list_to_datetime(df['EPOCH (BEGINNING WITH REFERENCE TLE)'])
        self.ref_alts = df['ALTITUDE (KM)']
        self.pred_epochs = str_list_to_datetime(df['PREDICTION EPOCH'])
        self.pred_alts = df['PREDICTION ALT (KM)']
        self.dst_list = get_dst_list(self.ref_epochs)
        self.error_list = self.get_error_list()

        # colormesh constants for ease of access
        self.max_height = 300
        self.min_height = 100
        self.num_ybins = len(self.ref_alts)
        self.bin_height = (self.max_height - self.min_height) / self.num_ybins
        self.num_days = len(self.ref_epochs)

        # the colormesh in question
        self.colors = self.fill_colors()

    def get_error_list(self):
        error_list = []
        for i in range(len(self.ref_epochs)):
            error_list.append((self.ref_epochs[i] - self.pred_epochs[i]).days)
        return error_list


    def fill_colors(self):
        colors = np.zeros((self.num_ybins, self.num_days))
        for i in range(len(self.error_list)):
            xbin = (self.ref_epochs[i] - self.ref_epochs[0]).days
            ybin = int((self.ref_alts[i] - self.min_height) / self.bin_height)
            error = self.error_list[i]
            colors[ybin, xbin] = abs(error)
        return colors

def get_xbin_list(event):
    xbins = []
    for i in range(len(event.ref_epochs)):
        time_after_ref = event.ref_epochs[i] - event.ref_epochs[0]
        # get timedelta days as a float
        xbins.append((time_after_ref.total_seconds() * 3600) / 24)
    return xbins

def get_ybin_list(event):
    ybins = []
    for i in range(len(event.ref_alts)):
        ybins.append((event.ref_alts[i] - event.min_height) / event.bin_height)
    return ybins

def round_datetime(date_list):
    new_dates = []
    for date in date_list:
        new_date = datetime(date.year, date.month, date.day, date.hour)
        new_dates.append(new_date)
    return new_dates

def get_dst_list(ref_epochs):
    time, dst = get_dst(ref_epochs[0])

    rounded_dates = round_datetime(ref_epochs)
    epoch_dst = []

    for date in rounded_dates:
        index = time.index(date)
        epoch_dst.append(dst[index])
    return epoch_dst

def get_dst(begin_time):

    """
        Get dst data and corresponding datetimes

        dtime: a datetime object (needs to coincide with the epoch of refeence altitude)

    """

    year = begin_time.timetuple()[0]
    doy = begin_time.timetuple()[7]
    hour = begin_time.timetuple()[3]
    minute = begin_time.timetuple()[4]
    second = begin_time.timetuple()[5]

    # begin time in hours after 2020
    begin_time_hours = (year - 2020) * 24 * 365 + (doy - 1) * 24 + hour + minute / 60. + second / 3600.

    # open list to store dst data and datetime objects (ti)
    dst, ti = [], []

    # loop over all dst files (look for folder in Box: data/dst)
    dst_bag = sorted(glob.glob('../data/dst/dst*'))

    for file in dst_bag:
        with open(file) as data:
            for lines in data:

                yy = int(lines[3:5]) + 2000
                MM = int(lines[5:7])
                dd = int(lines[8:10])

                dy = day2doy(yy, MM, dd)

                for i, j in zip(range(20, 119, 4), range(1, 25)):

                    dst_time = (yy - 2020) * 365 * 24 + (dy - 1) * 24 + j - 1

                    if begin_time_hours - 1 <= dst_time:
                        dst.append(float(lines[i:i + 4]))
                        ti.append(datetime(yy, MM, dd, j - 1))

    return ti, dst

def str_list_to_datetime(str_list):
    datetime_list = []
    for i in range(len(str_list)):
        dt = datetime.strptime(str_list[i][:-6], "%Y-%m-%d %H:%M:%S")
        datetime_list.append(dt)
    return datetime_list

def main():
    id = 48451
    event = SevereEvent(id)

    '''fig, (alt_ax, dst_ax) = plt.subplots(2, 1)

    # create alt plot
    alt_ax.set_title(f"NORAD ID {id} Reentry Altitude")
    alt_ax.set_xlabel("Epoch")
    alt_ax.set_ylabel("Altitude (km)")
    alt_ax.plot(event.ref_epochs, event.ref_alts)

    # create dst plot
    dst_ax.set_title(f"NORAD ID {id} Reentry Dst")
    dst_ax.set_ylabel("Dst")
    dst_ax.set_xlabel("Epoch")
    dst_ax.plot(event.ref_epochs, event.dst_list)

    plt.tight_layout()'''

    # create colormesh
    plt.pcolormesh(event.colors, cmap=plasma_w)
    plt.colorbar(label = "Error in Days")
    plt.yticks(np.linspace(0, event.num_ybins, 9), np.linspace(event.min_height, event.max_height, 9))
    plt.scatter(get_xbin_list(event), get_ybin_list(event), c='black', s=3)
    plt.show()

main()
