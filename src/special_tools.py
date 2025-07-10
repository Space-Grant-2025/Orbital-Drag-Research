
# This file contains special functions I frequently use in my data analyses

import sys
import datetime 
import calendar
import numpy as np 
import matplotlib as mpl 
import matplotlib.pyplot as plt 

sys.path.append('/Users/dennyoliveira/utilities/pymag/')

from math import floor, trunc
from matplotlib.colors import ListedColormap
from numpy import sin, cos, where, nan, isnan, interp, array, dot, pi, sign, arcsin, arccos, arctan2, sqrt, deg2rad, rad2deg

r2d = rad2deg
d2r = deg2rad

#plt.rcParams['axes.facecolor'] = (229.0 / 255, 229.0 / 255, 229.0 / 255)

def day2doy(yy, MM, dd):

	"""
    Purpose
    _______

		Converts day of month to day of year using a datetime object

    Inputs
    ______

        yy: 
            year

        MM:
            month

        dd:
            day

    Output
    ______

        doy:
            day of year

	"""

	FMT = '%Y:%m:%d'
	DATE = '{:>4}:{:>02}:{:>02}'.format(int(yy), int(MM), int(dd))
	doy = datetime.datetime.strptime(DATE, FMT).timetuple().tm_yday
    
	return doy

def doy2date(yy, dy):

    """
    Purpose
    _______
        Convert day of of year as three different date objects

    Inputs
    ______
            yy:
                    year

            dy:     
                    day of year

    Returns
    _______
            dtime1:
                    datetime object

            dtime2:
                    date object in the form YYYYMMDD

            dtime3:
                    date object in the form YYYY/MM/DD
    """

    date = '{:>4} {:>3}'.format(yy, dy)
    month = int(datetime.datetime.strptime(date, '%Y %j').strftime('%m'))
    day = int(datetime.datetime.strptime(date,'%Y %j').strftime('%d'))
    dtime1 = datetime.datetime(yy, month, day)
    dtime2 = '{:>4}{:>02d}{:>02d}'.format(yy, month, day)
    dtime3 = '{:>4}-{:>02d}-{:>02d}'.format(yy, month, day)

    return dtime1, dtime2, dtime3

def date2jd(dtime):

    """
    Purpose
    _______

        Converts a datetime objet into Julian Day and Modified Julian Day

    Inputs
    ______

        dtime:
            A datetime object

    Returns
    _______
        jd:
            Julian Day

        mjd:
            Modified Julian Day
    """

    year = dtime.year
    month = dtime.month
    day = dtime.day

    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year 
        monthp = month 

    if ((year < 1582) or (year == 1582 and month < 10) or (year == 1582 and month == 10 and day < 15)):
        B = 0 
    else:
        A = trunc(yearp / 100.)
        B = 2 - A + trunc(A / 4.)

    if yearp < 0:
        C = trunc((365.25 * yearp) - 0.75)
    else:
        C = trunc(365.25 * yearp)

    D = trunc(30.6001 * (monthp + 1))

    jd = B + C + D + day + 1720994.5
    mjd = jd - 2400000.5

    return jd, mjd 


def smooth(y, N):

	"""
    Purpoese
    ________
		
        Smooths an array within windows determined by an integer

    Inputs
    ______

        y:
            variable to be smoothed

        N:
            size of smooth window (integer)

    Returns
    _______

        y_smooth:
            smoothed variable
	"""

	box = np.ones(N) / N
	y_smooth = np.convolve(y, box, mode = 'same')

	return y_smooth

def get_xlt(doy, xlon, utc):

    """
    Purpose
    _______

        Computes local time as a function of day of year, geographic longitude, and
        universal time using the equation of time (EoT).

    Inputs
    ______

        doy:
            day of year (1 - 365 or 366 if year is a leap year)

        xlon:
            geographic longitude (-180 <= xlon <= 180)

        utc:
            fraction of universal time (hours)      

    Returns
    _______

        xlt:
            local time
    """

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

def make_cmap(colors, position = None, bit = False):
    
    """
    	Make_cmap takes a list of tuples which contain RGB values. The RGB
    	values may either be in 8-bit [0 to 255] (in which bit must be set to
    	True when called) or arithmetic [0 to 1] (default). make_cmap returns
    	a cmap with equally spaced colors.
    	Arrange your tuples so that the first color is the lowest value for the
    	colorbar and the last is the highest.
    	position contains values from 0 to 1 to dictate the location of each color.
    """

    bit_rgb = np.linspace(0, 1, 256)
    
    if position == None:
        position = np.linspace(0, 1, len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap', cdict, 256)

    return cmap

def ggplot(ax, edges, grid):

    """
    Purpose
    _______

        Makes plot in the ggplot style with grey background
    """

    plt.rcParams['axes.facecolor'] = (229.0 / 255, 229.0 / 255, 229.0 / 255)

    if edges == False:
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
    else:
        ax.spines['top'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)
        ax.spines['right'].set_visible(True)

    if grid == True:
        plt.grid(color = 'w', ls = '-', lw = 1.5)

    ax.tick_params('both',length=0.0,width=0.0,which='major',direction='out',right=True,top=True)
    ax.tick_params('both',length=0.0,width=0.0,which='minor',direction='out',right=True,top=True)

def nan_helper(bad_data, var):

    """
    Purpose
    _______

        Replaces bad data by numpy nan variables and then interpolates data

    Inputs
    ______

        bad_data:
                bad data (999.99, 999999., +1E30, ...) to be replaced by nana variables

        var:    
                variable to be interpolated

    Returns
    _______

        var:
            interpolated variable
    """

    var = where(var == abs(bad_data), nan, var)
    nans, VAR = isnan(var), lambda z: z.nonzero()[0]
    var[nans] = interp(VAR(nans), VAR(~nans), var[~nans])

    return var



def earth_radius_lat(xlat):

    """
    Purpose
    _______

        Calculates Earth's radius as a function of Earth's equatorial radius and polar radius at
        a given latitude using WGS (World Geodetic System) 84 reference ellipsoid.

        Reference:

        WGS84. (1984). World Geodetic System – 1984 (WGS-84) Manual (Tech. Rep.). Montreal, Canada: 
            International Civil Aviation Organization. Retrieved from 
            https://www .icao.int/NACC/Documents/Meetings/2014/ECARAIM/REF08-Doc9674.pdf

        Formula derivation with online calculator can be found here:

        https://planetcalc.com/7721/

    Input
    _____

        xlat:
            geocentric latitude

    Returns
    _______

        Re:
            Earth's radius as a function of latitude (in km)

    """

    a = 6378.137
    e2 = 0.00669437999
    b = a * sqrt(1 - e2)

    beta = xlat * pi / 180.

    n1 = (a ** 2 * cos(beta)) ** 2
    n2 = (b ** 2 * sin(beta)) ** 2

    d1 = (a * cos(beta)) ** 2
    d2 = (b * sin(beta)) ** 2

    Re = sqrt((n1 + n2) / (d1 + d2))

    return Re


def haversine(xlat1, xlon1, xlat2, xlon2):

    """
    Purpose
    _______

        Compute the distance between two points on a sphere using the Haversine formula (Gade, 2020) as a 
        function of the geographic coordinates of two pints.

    Inputs
    ______
            xlat1:
                    Geographic latitude of point 1, in degrees
            xlon1:
                    Geographic longitude of point 1, in degrees

            xlat2:
                    Geographic latitude of point 2, in degrees
            xlon2:
                    Geographic longitude of point 2, in degrees
    Returns
    _______
            d:
                distance between points 1 and 2, in km


    Reference
    _________

        Gade, K. (2020). A Non-singular Horizontal Position Representation. The Journal of Navigation, 
            63(3), 295-417. https://doi.org/10.1017/S0373463309990415
    """

    Re = 6357. 

    xlat1, xlat2 = d2r(xlat1), d2r(xlat2)
    xlon1, xlon2 = d2r(xlon1), d2r(xlon2)

    dphi = xlon2 - xlon1
    dlat = xlat2 - xlat1

    A = sqrt(sin(dlat / 2.) ** 2 + cos(xlat1) * cos(xlat2) * sin(dphi / 2.) ** 2)

    d = 2 * Re * arcsin(A)

    return d


def gd2gc(xlat, xht):

    """"
    Purpose
    _______

        Converts geocentric latitudes to geodetic latitudes according to an algorithm 
        provided by Malin and Barraclough (1981) and WGS-84 ellipsoid parameters and 
        computes geodetic Earth radius

    Input
    _____

        xlat: 
                geodetic latitude
        xht: 
                altitude

    Returns
    _______

        xlat:
                geocentric latitude

        r:
                geodetic Earth's radius

    Reference
    _________

        Malin, S. R. C., & Barraclough, D. R. (1981). An algorithm for synthesizing the geomagnetic 
            field. Computer & Geosciences, 7(4), 401-405. https://doi.org/10.1016/0098-3004(81)90082-0

    """

    colat = pi / 2 - d2r(xlat)

    Req = 6378.137
    f = 1 / 298.257223563
    Rpl = Req * (1 - f)

    ctgd = cos(colat)
    stgd = sin(colat)

    a2 = Req * Req 
    a4 = a2 * a2 
    b2 = Rpl * Rpl 
    b4 = b2 * b2 
    c2 = ctgd * ctgd 
    s2 = 1.0 - c2
    rho = sqrt(a2 * s2 + b2 * c2)

    r = sqrt(xht * (xht + 2 * rho) + (a4 * s2 + b4 * c2) / rho**2)

    cd = (xht + rho) / r 
    sd = (a2 - b2) * ctgd * stgd / (rho * r)

    cthc  = ctgd * cd - stgd * sd           
    xlat = r2d(pi/2 - arccos(cthc))

    return xlat, r


def gd2car(xlat, xlon, xht):

    """
        Purpose
        _______

            Converts

    """

    f = 1. / 298.257223563
    a = 6378.137
    b = a * (1 - f)

    theta = d2r(xlat)
    phi = d2r(xlon)

    e2 = 1 - (b / a) ** 2

    N = a / sqrt(1 - e2 * sin(theta) ** 2)

    x = (N + xht) * cos(theta) * cos(phi)
    y = (N + xht) * cos(theta) * sin(phi)
    z = ((1 - e2) * N + xht) * sin(theta)

    return x, y, z


def get_days_since_date(dtime1, dtime2):

    yy1 = dtime1.timetuple()[0]
    MM1 = dtime1.timetuple()[1]
    dd1 = dtime1.timetuple()[2]

    yy2 = dtime2.timetuple()[0]
    MM2 = dtime2.timetuple()[1]
    dd2 = dtime2.timetuple()[2]

    dy1 = day2doy(yy1, MM1, dd1)
    dy2 = day2doy(yy2, MM2, dd2)

    DOY = []

    for yy in range(yy1, yy2 ):
        DOY.append(day2doy(yy, 12, 31))

    days = sum(DOY) - dy1 + dy2

    return days

def seconds2ut(time):

    hh = int(time / 3600)
    mm = int((time - hh * 3600) / 60.)
    ss = int((time - hh * 3600 - mm * 60))

    return hh, mm, ss












