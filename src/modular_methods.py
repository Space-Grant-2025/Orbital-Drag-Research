import pandas as pd
from datetime import datetime, date
from math import sin, cos
import numpy as np

end_of_may = date(2025, 5, 31)


def get_reference_epoch(id):
    '''
    Convert string in McDowell foramt to datetime object

    Parameters
    ---------
    id: int
        satellite NORAD id

    Returns
    -------
    ref_epoch: datetime object
        returns reference epoch as a datetime object
    '''
    epoch_df = pd.read_csv('../data/epoch_masterlist.csv')
    target_row = epoch_df[epoch_df['NORAD ID'] == id]
    ref_alt = target_row["REFERENCE ALTITUDE EPOCH"].iloc[0]
    return datetime.strptime(ref_alt, "%Y-%m-%d %H:%M:%S%z")


def create_mcdowell_date(date_str):
    '''
    Convert string in McDowell foramt to datetime object

    Parameters
    ---------
    date_str: str
        date string

    Returns
    -------
    date_obj: datetime object
        returns datetime object or None if date is not found
    '''

    if date_str is not None:
        if len(date_str) >= 10:
            date_str = date_str[:11]
            year = int(date_str[:4])
            month = date_str[5:8]
            day = int(date_str[9:11].strip())
            date_obj = datetime.strptime(f'{year}-{month}-{day}', "%Y-%b-%d").date()
            return date_obj
        elif len(date_str) == 5:
            date_str = date_str[:4]
            year = int(date_str[:4])
            date_obj = date(year, 1, 1)
            return date_obj
        else:
            return None
    return None


def doy2date(year, day):
    '''
	Convert day of year as three different date objects.

	Parameters
	---------
	year: int
		year
	day: int
		day

	Returns
	-------
	dtime1, dtime2, dtime3: datetime tuple
		tuple in format (datetime object, date object in the form YYYYMMDD, date object in the form YYYY/MM/DD)

	'''

    date = '{:>4} {:>3}'.format(year, day)
    month = int(datetime.strptime(date, '%Y %j').strftime('%m'))
    day = int(datetime.strptime(date, '%Y %j').strftime('%d'))
    dtime1 = datetime(year, month, day)
    dtime2 = '{:>4}{:>02d}{:>02d}'.format(year, month, day)
    dtime3 = '{:>4}-{:>02d}-{:>02d}'.format(year, month, day)

    return dtime1, dtime2, dtime3


def day2doy(year, month, day):
    '''
	Converts day of month to day of year using a datetime object

	Parameters
	----------
	year: str
		year string
	month: str
		month string
	day: str
		day string

	Returns
	-------
	doy: time_struct time
		day of year
	'''

    FMT = '%Y:%m:%d'
    DATE = '{:>4}:{:>02}:{:>02}'.format(int(year), int(month), int(day))
    doy = datetime.strptime(DATE, FMT).timetuple().tm_yday

    return doy


def get_xlt(doy, xlon, utc):
    '''
	Computes local time as a function of day of year, geographic longitude, and universal time using the equation of time (EoT)


	Parameters
	----------
	doy: int
	    day of year (1 - 365 or 366 if year is a leap year)
    xlon: float
        geographic longitude (-180 <= xlon <= 180)
    utc: float
        fraction of universal time (hours)

	Returns
	-------
	xlt: float
		local time

	'''

    if xlon < 0:
        xlon = 360 + xlon

    B = (doy - 81) * 360.0 / 365.0
    EoT = 9.87 * sin(2 * B) - 7.53 * cos(B) - 1.5 * sin(B)

    lt = int(xlon / 15.)
    lstm = 15. * (lt - utc)
    tc = 4. * (xlon - lstm) + EoT
    xlt = abs(lt + tc / 60.)

    if xlt >= 24:
        xlt = xlt - 24

    if xlt < 0:
        xlt = xlt + 24

    return xlt


def smooth(var, size):
    """
    Smooths an array within windows determined by an integer

    Parameters
	----------
    var: array
        variable to be smoothed
    size: int
        size of smooth window (integer)

	Returns
	-------
    y_smooth: array
        smoothed variable
	"""

    box = np.ones(size) / size
    y_smooth = np.convolve(var, box, mode='same')

    return y_smooth
