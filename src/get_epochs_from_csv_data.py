import sys

# given a NORAD ID, reads in processed csv data and return the time when satellite altitude is closest to 280km
def get_zero_epoch(id):
    with open(f'./data/human_readable/tle_{id}.csv', 'r') as csvfile:
        # pass over header
        csvfile.readline()
        # tuple holding closest altitude and corresponding date, initialized at massive number and date placeholder
        closest_alt = float(sys.maxsize), "0000-00-00 00:00:00"

        # loop over csv data and hold altitude nearest to 280 and corresponding altitude
        for row in csvfile:
            split_row = row.split(',')
            # current values
            current_alt = float(split_row[1]), split_row[0]
            # distances of minimum and current values from 280
            curr_distance_from_280 = abs(current_alt[0] - 280)
            min_distance_from_280 = abs(closest_alt[0] - 280)
            if curr_distance_from_280 < min_distance_from_280:
                closest_alt = current_alt
    return closest_alt

print(get_zero_epoch(48384))