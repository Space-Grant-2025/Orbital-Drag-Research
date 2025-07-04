import os
from get_id_by_reentry import begin_date
from get_id_by_reentry import end_date

def check_csv_txt_exists(id):
    txt_exists = os.path.isfile(f'./data/tles/tle_{id}.txt')
    csv_exist = os.path.isfile(f'./data/human_readable/tle_{id}.csv')
    if not txt_exists and not csv_exist:
        print(f'{id} neither file exists')
        return
    if not txt_exists:
        print(f'{id} txt file does not exist')
    if not csv_exist:
        print(f'{id} csv file does not exist')

def main():
    with open('reentry-' + begin_date + '-to-' + end_date + '.txt', 'r') as file:
        # pass over headers
        file.readline()

        # loop through norad ids and create file of tle data
        for id in file:
            id = id.strip()
            check_csv_txt_exists(id)
main()
print("Finished")