import requests
import os
from tqdm import tqdm
a

NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"
#home_logo = "https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/10.svg"
url = ""
pathname = "/home/pi/nhl_scoreboard/images/players"

def get_urls():
    """ Function to get a list of all the teams ID and logo webpage"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teamID = 0
    teams = []
    urls = []

    for team in results['teams']:
        #teams.append(team['franchise']['teamName'])
        teams.append(team['id'])
        teamID = team['id']
        urls.append('https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/{0}.svg'.format(teamID))
    return urls

def get_pngs():
    """ Function to create png filenames based on team ids"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teamID = 0
    teams = []

    #global pngs
    pngs = []

    for team in results['teams']:
        #teams.append(team['franchise']['teamName'])
        teams.append(team['id'])
        teamID = team['id']
        pngs.append('/home/pi/nhl_scoreboard/images/PNG/{0}.png'.format(teamID)) #create all png filenames
    return pngs


def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    global teamID
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress.iterable:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))