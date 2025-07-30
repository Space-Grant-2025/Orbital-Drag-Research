# returns a string of all the data
import configparser
import requests

# dates in YYY-MM-DD
begin_date = "2020-01-01"
end_date = "2025-05-31"

def get_data():
    # api uris
    uri_base = 'https://www.space-track.org'
    request_login = '/ajaxauth/login'
    request_cmd_action = '/basicspacedata/query/'
    request_find_starlinks = 'class/gp/DECAY_DATE/%3E'+ begin_date + '%2C%3C' + end_date + '/OBJECT_NAME/~~STARLINK/orderby/DECAY_DATE%20asc/emptyresult/show'
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

        # send http packet asking for starlink data and save the response (the starlink data)
        data = session.get(uri_base + request_cmd_action + request_find_starlinks)

        return data.text

# takes in a list of starlink data (provided by get_data()) and creates a txt file of all the NORAD IDs
def write_ids_to_txt(data):
    with open("../data/starlink_reentries_list.txt", "w") as file:
        # list of all the lines
        lines = data.strip("[]").split("}")

        # add headers
        file.write("STARLINK REENTRIES " + begin_date + " to " + end_date + "\n")

        for x in range (len(lines) - 1):

            # create list of all the values
            lines[x] = lines[x].strip("{,")
            cells = lines[x].split(',')

            # save the values
            norad_id = cells[19][16:21]

            # write values to file
            file.write(f'{norad_id}\n')

if __name__ == "__main__":
    write_ids_to_txt(get_data())