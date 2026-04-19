from datetime import datetime
import datetime
import math
from src.special_tools import get_date_from_tle
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
        self.date = get_date_from_tle(self.tle_line1)
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