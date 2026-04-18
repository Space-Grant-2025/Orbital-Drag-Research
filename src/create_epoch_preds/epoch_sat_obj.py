from datetime import datetime
import ephem

none_count = 0

class Epoch:
    def __init__ (self, id, tle_instance_epoch, tle_instance_alt, ref_line1, ref_line2, instance_line1, instance_line2):
        self.ref_line1 = ref_line1
        self.ref_line2 = ref_line2
        self.tle_instance_epoch = tle_instance_epoch
        self.tle_instance_alt = tle_instance_alt
        self.line1 = instance_line1
        self.line2 = instance_line2
        self.prediction_alt = self.make_prediction()
        if self.prediction_alt is not None:
            self.delta_alt = tle_instance_alt - self.prediction_alt
        else:
            self.delta_alt = None
            global none_count
            none_count += 1

    def make_prediction(self):
        # ephem object reads in given tle data
        satellite = ephem.readtle('NORAD' + str(self.id), self.ref_line1, self.ref_line2)
        str_date = datetime.strftime(self.tle_instance_epoch, "%Y-%m-%d %H:%M:%S")
        ephem_date = ephem.date(str_date)

        # compute satellite at date
        try:
            satellite.compute(ephem_date)
            altitude = satellite.elevation / 1000
            return altitude

        except:
            return None