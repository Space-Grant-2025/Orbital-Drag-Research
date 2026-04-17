from datetime import datetime
import datetime
import math
import re

import ephem

# gravitational constant
GRAV = 6.6743e-11
# mass of Earth
MASS_EARTH = 5.9722e24

class Satellite:
    def __init__(self, id, line0, line1, line2):
        # ephem object reads in given tle data
        ephem_satellite = ephem.readtle('NORAD' + str(id), line1, line2)

        # assign values
        self.id = id
        self.name = line0[1:]
        self.tle_line1 = line1
        self.tle_line2 = line2

        # process date
        self.date = self.get_date_from_tle()
        str_date = datetime.strftime(self.date,"%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # propagate flight data
        try:
            ephem_satellite.compute(ephem_date)
            self.latitude = ephem_satellite.sublat
            self.longitude = ephem_satellite.sublong
            self.altitude = ephem_satellite.elevation / 1000 # in km
            self.mean_motion = 2 * math.pi * float(line2[52:62]) / 86400.
            self.velocity = (GRAV * MASS_EARTH * self.mean_motion) ** (1 / 3.) * 1e-3
        except RuntimeError:
            self.latitude = None
            self.longitude = None
            self.altitude = None
            self.mean_motion = None
            self.velocity = None

    def get_utc(self):
        return self.date.timestamp()

    def get_day_of_year(self):
        return self.date.timetuple().tm_yday

    # gets in the float representing the date on the first line of the tle and returns datetime object
    def get_date_from_tle(self):
        find_date = re.compile('\\d{5}\\.\\d{8}')
        tle_date = find_date.search(self.tle_line1).group()

        year = 0
        # checks if the year listed is before 2000 (not necessary, but good practice)
        if int(tle_date[:2]) > 50:
            year = 1900 + int(tle_date[:2])
        else:
            year = 2000 + int(tle_date[:2])
        # holds the day of year and fraction of day
        total_days = float(tle_date[2:])

        # fraction represents the fraction of the day
        fraction = total_days - int(total_days)
        total_days = math.trunc(total_days)

        # converts number of days in year to day and month
        month = int(datetime.strptime(f"{year} {total_days}", '%Y %j').strftime('%m'))
        day = int(datetime.strptime(f"{year} {total_days}",'%Y %j').strftime('%d'))

        # converts fraction of day into human_readable
        hour = int(fraction * 24)
        min = int(fraction * 1440 - hour * 60)
        sec = int(fraction * 86400 - hour * 3600 - min * 60)

        # create datetime object
        date = datetime(year, month, day, hour, min, sec, tzinfo=datetime.timezone.utc)

        # millisecs and rounding secs for more precision
        millisecs = fraction * 86400 - hour * 3600 - min * 60 - sec

        if millisecs >= .5:
            date = date + datetime.timedelta(0, 1)

        return date