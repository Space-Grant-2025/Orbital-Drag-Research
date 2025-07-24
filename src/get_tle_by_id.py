import pyautogui
import requests
import configparser
import datetime
import time
import os.path

# given a NORAD ID, returns the TLE data for the corresponding satellite
def get_tle(id):
    # api uris
    uri_base = 'https://www.space-track.org'
    request_login = '/ajaxauth/login'
    request_cmd_action = '/basicspacedata/query'
    request_find_starlinks = '/class/gp_history/NORAD_CAT_ID/' + str(id) + '/orderby/TLE_LINE1%20ASC/'
    #request_find_starlinks = '/class/gp_history/NORAD_CAT_ID/' + str(id) + '/orderby/TLE_LINE1%20ASC/format/json'

    # login credentials read in from the .ini file
    config = configparser.ConfigParser()
    config.read('./SLTrack.ini')
    config_usr = config.get('configuration', 'username')
    config_pwd = config.get('configuration', 'password')
    # not using right now
    # config_out = config.get('configuration', 'output')
    site_credentials = {'identity': config_usr, 'password': config_pwd}

    # open a session with space-track
    with requests.Session() as session:
        # send http packet with login credentials and save response
        response = session.post(uri_base + request_login, data = site_credentials)

        # 200 is good, 400 is error on our end, 500 is error on their end
        if response.status_code != 200:
            print(f"{response}\n{response.text}\nPOST fail on login")
        # raise error for bad login
        if response.content.decode('ascii') == "{\"Login\":\"Failed\"}":
            print(f"{response}\n{response.text}\nERROR: Bad login credentials")

        # send http packet asking for starlink data and save the response (the tle data)
        tle = session.get(uri_base + request_cmd_action + request_find_starlinks)
        return tle.text

# given tle data, add it to txt file
def write_tle_to_file(text, id):
    with open("../data/tles/tle_" + str(id) + ".txt", "w") as file:
        for line in text.split('},{'):
            line_arr = line.split(',')
            tle0 = line_arr[37][12:].strip("\"")
            tle1 = line_arr[38][12:].strip("\"")
            tle2 = line_arr[39][12:].strip("\"")
            file.write(f'{tle0}\n{tle1}\n{tle2}\n')

# loops through the norad ids in the txt file
def main():
    start_time = datetime.datetime.now()

    with open('../data/reentry_ids_masterlist.txt', 'r') as file:
        if not os.path.exists("../data/tles/"):
            os.makedirs("../data/tles/")

        # pass over headers
        file.readline()

        # progress tracker
        count = 1

        # loop through norad ids and create file of tle data
        for id in file:
            id = int(id.strip())

            if os.path.exists("../data/tles/tle_" + str(id) + ".txt"):
                continue

            tle = get_tle(id)
            write_tle_to_file(tle, id)

            # jitter to keep computer awake
            pyautogui.press('shift')

            # progress tracker
            print(f'{count}: {id}')
            count += 1

            # delay requests to prevent bandwidth excess as requested by space-track
            time.sleep(12)

    # prints total time program takes to run because i'm curious
    end_time = datetime.datetime.now()
    print(str(f'Finished: {end_time - start_time}'))

if __name__ == '__main__':
    main()
