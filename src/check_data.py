import os
import re
import pandas as pd

count = 0

masterlist_ids = []
oliveira_ids = []

# checks reentry masterlist to see if both a csv and txt file exists for each NORAD id
# prints id and message if does not exist
def check_starlink_files_exists(id):
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


def run_check_starlink_files():
    starlink_reentries = pd.read_csv('../data/starlink_reentries_list.txt')
    masterlist_ids = starlink_reentries['STARLINK REENTRIES 2020-01-01 to 2025-05-31']

    for id in masterlist_ids:
        check_starlink_files_exists(id)

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

# make sure reentries are bifurcated
def check_reentry_files():
    with open('../data/other_reentries_list.txt', 'r') as file:
        lines = file.readlines()
        num = len(lines)
        starlink_count = 0
        other_count = 0
        for id in lines:
            id = id.strip()
            if os.path.exists(f'../data/starlink_reentries_2020_2025/human_readable/tle_{id}.csv'):
                starlink_count += 1
            if os.path.exists(f'../data/other_reentries/human_readable/tle_{id}.csv'):
                other_count += 1
    print(f'Starlink: {starlink_count}\nOther: {other_count}\nTotal: {starlink_count+other_count}\nNum Lines: {num}\n')
    print("Finished checking reentry files\n")

def check_starlinks_in_reentry():
    count = 0
    starlink_list = []
    with open('../data/other_reentries_list.txt', 'r') as file:
        reentries = file.readlines()
    with open('../data/starlink_reentries_list.txt', 'r') as file:
        # pass over header
        file.readline()

        for id in file:
            if not id in reentries:
                count += 1
                starlink_list.append(id)
                print(f'{count}: {id} not in reentry list')
    return starlink_list

def add_starlink_to_reentry():
    list = check_starlinks_in_reentry()
    with open('../data/other_reentries_list.txt', 'a') as file:
        for id in list:
            file.write(id)

run_check_starlink_files()
check_oliveira_data_against_masterlist()
add_oliveira_data_to_masterlist()
check_reentry_files()
#check_starlinks_in_reentry()
add_starlink_to_reentry()
check_starlinks_in_reentry()
