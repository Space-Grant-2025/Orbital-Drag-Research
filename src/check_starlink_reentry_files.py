import os
import re

count = 0

masterlist_ids = []
oliveira_ids = []

# checks reentry masterlist to see if both a csv and txt file exists for each NORAD id
# prints id and message if does not exist
def check_files_exists(id):
    global count
    txt_exists = os.path.isfile(f'../data/starlink_reentries_2020_2025/starlink_tles/tle_{id}.txt')
    csv_exist = os.path.isfile(f'../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv')
    lifetime_exist = os.path.isfile(f"../data/starlink_reentries_2020_2025/lifetime_profiles/{id}_lifetime_profile.png")
    altitude_time_exist = os.path.isfile(f"../data/starlink_reentries_2020_2025/reentry_graphs/altitude_time/{id}_altitude_time.png")
    jb2008_time_exist = os.path.isfile(f"../data/starlink_reentries_2020_2025/reentry_graphs/jb2008_time/{id}_jb2008_time.png")
    nrlmsise_time_exist = os.path.isfile(f"../data/starlink_reentries_2020_2025/reentry_graphs/nrlmsise_time/{id}_nrlmsise_time.png")

    if not txt_exists:
        count += 1
        print(f'{count}: {id} txt file does not exist')
    if not csv_exist:
        count += 1
        print(f'{count}: {id} csv file does not exist')
    if not lifetime_exist:
        count += 1
        print(f'{count}: {id} lifetime graph does not exist')
    if not altitude_time_exist:
        count += 1
        print(f'{count}: {id} altitude_time graph does not exist')
    if not jb2008_time_exist:
        count += 1
        print(f'{count}: {id} jb2008_time graph does not exist')
    if not nrlmsise_time_exist:
        count += 1
        print(f'{count}: {id} nrlmsise_time graph does not exist')


def run_check_files():
    with open('../data/starlink_reentries_list.txt', 'r') as file:
        # pass over headers
        file.readline()

        # loop through norad ids and create file of tle data
        for id in file:
            id = id.strip()
            masterlist_ids.append(id)
            check_files_exists(id)
    print("Finished checking files\n")

# checks oliveira's list of ids against masterlist
# prints NORAD ID and reentry data
# only ones not in original list are 48160 and 54046 (i don't know why)
def check_oliveira_data_against_masterlist():
    with open(f'../data/external_datasets/oliveira_data.txt', 'r') as file:
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
    with open('../data/starlink_reentries_list.txt', 'a') as masterlist:
        for id in oliveira_ids:
            masterlist.write(id + "\n")
    print("Added Oliveira data to masterlist\n")

run_check_files()
check_oliveira_data_against_masterlist()
add_oliveira_data_to_masterlist()
