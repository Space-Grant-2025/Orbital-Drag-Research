import os
import re

count = 0

masterlist_ids = []
oliveira_ids = []

# checks reentry masterlist to see if both a csv and txt file exists for each NORAD id
# prints id and message if does not exist
def check_csv_txt_exists(id):
    global count
    txt_exists = os.path.isfile(f'../data/tles/tle_{id}.txt')
    csv_exist = os.path.isfile(f'../data/human_readable/tle_{id}.csv')
    if not txt_exists and not csv_exist:
        count += 1
        print(f'{count}: {id} neither file exists')
        return
    if not txt_exists:
        count += 1
        print(f'{count}: {id} txt file does not exist')
    if not csv_exist:
        count += 1
        print(f'{count}: {id} csv file does not exist')

def run_check_csv_txt():
    with open('../data/reentry_ids_masterlist.txt', 'r') as file:
        # pass over headers
        file.readline()

        # loop through norad ids and create file of tle data
        for id in file:
            id = id.strip()
            masterlist_ids.append(id)
            check_csv_txt_exists(id)
    print("Finished checking csv and txt files\n")

# checks oliveira's list of ids against masterlist
# prints NORAD ID and reentry data
# only ones not in original list are 48160 and 54046 (i don't know why)
def check_oliveira_data_against_masterlist():
    with open(f'../data/oliveira_data.txt', 'r') as file:
        global count
        count = 0
        # pass over headers
        file.readline()
        file.readline()

        for line in file:
            find_id = re.compile('\\d{5}')
            id = find_id.search(line).group()

            find_reentry = re.compile('\\t\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}')
            reentry = find_reentry.search(line).group().strip()

            if id not in masterlist_ids:
                count += 1
                oliveira_ids.append(id)
                print(f'{count}: {id} not in masterlist. Reentry: {reentry}')
    print("Finished checking Oliveira data\n")

def add_oliveira_data_to_masterlist():
    with open('../data/reentry_ids_masterlist.txt', 'a') as masterlist:
        for id in oliveira_ids:
            masterlist.write(id + "\n")

run_check_csv_txt()
check_oliveira_data_against_masterlist()
add_oliveira_data_to_masterlist()