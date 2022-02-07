import requests
import datetime
from dateutil import tz
import pause
import json
'''
*********************************************
local json file
reference: https://www.geeksforgeeks.org/read-json-file-using-python/
*********************************************
'''
NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/"
NHL_API_URL = "/home/pi/nhl_scoreboard/json/"

def get_team_id(team_name):
    """ Function to get team of user and return NHL team ID"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())
    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {0}".format(team_name))

def check_game_status(team_id,date):
    """ Function to check if there is a game now with chosen team. Returns True if game, False if NO game. """
    # Set URL depending on team selected and date

    fn = open('{0}exampleNHLfile.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())
    
    try:
        #get game state from API (no state when no games on date)
        #game_status = requests.get(url).json()
        game_status = results['dates'][0]['games'][0]['status']['detailedState']
        return game_status

    except IndexError:
        #Return No Game when no state available on API since no game
        return 'No Game'

    except requests.exceptions.RequestException:
        # Return No Game to keep going
        return 'No Game'

def fetch_scores(team_id):
    """ Function to get the score of the game depending on the chosen team.
    Inputs the team ID and returns the score found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    
    fn = open('{0}exampleNHLfile.json'.format(NHL_API_URL), "r")
    fnScore = open('{0}exampleNHLfile.json'.format(NHL_API_URL), "r")
    #results = json.loads(fn.read())

    # Avoid request errors (might still not catch errors)
    try:
        score = json.loads(fnScore.read())

        #game_time = str(score['dates'][0]['games'][0]['teams'])
        #print (game_time)
        
        game = json.loads(fn.read())
        homeTeamScore = int(game['dates'][0]['games'][0]['teams']['home']['score'])
        homeTeamName = game['dates'][0]['games'][0]['teams']['home']['team']['name']
        awayTeamScore = int(game['dates'][0]['games'][0]['teams']['away']['score'])
        awayTeamName = game['dates'][0]['games'][0]['teams']['away']['team']['name']

        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])

        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        #print(homeTeamName, str(homeTeamScore), ":", str(awayTeamScore), awayTeamName, ", Time: {0}:{1}:{2}  ".format(now.hour, now.minute, now.second),end='\r')
        return score, homeTeamScore, awayTeamScore

    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0

def get_next_game_date(team_id):
    "function to get the time of the next game as original format - 30sec to start checking before game starts?"
    date_test = datetime.date.today()
    gameday = check_game_status(team_id, date_test)

    #Keep going until game day found
    '''
    while ("Scheduled" not in gameday):
        date_test = date_test + datetime.timedelta(days=1)
        gameday = check_game_status(team_id, date_test)
    '''

    #Get start time of next game
    fn = open('{0}futuregame.json'.format(NHL_API_URL), "r")
    utc_game_time = json.loads(fn.read())
    utc_game_time = utc_game_time['dates'][0]['games'][0]['gameDate']
    next_game_time24hr = convert_to_local_time(utc_game_time) - datetime.timedelta(seconds=30)
    next_game_time12hr = convert_to_local_time(utc_game_time) - datetime.timedelta(hours=12)
    next_game_day = date_test
    return next_game_time24hr, next_game_day, next_game_time12hr

def get_next_game_info2(team_id):
    """ Function to get game info (both team names & IDs) for next game that team_id plays"""
    date_test = datetime.date.today()
    gameday = check_game_status(team_id, date_test)

    #Keep going until game day found
    '''
    while ("Scheduled" not in gameday):
        date_test = date_test + datetime.timedelta(days=1)
        gameday = check_game_status(team_id, date_test)
    '''

    #Get start time of next game
    fn = open('{0}futuregame.json'.format(NHL_API_URL), "r")
    next_game_info = json.loads(fn.read())
    home_team = next_game_info['dates'][0]['games'][0]['teams']['home']['team']['name']
    home_team_ID = next_game_info['dates'][0]['games'][0]['teams']['home']['team']['id']
    away_team = next_game_info['dates'][0]['games'][0]['teams']['away']['team']['name']
    away_team_ID = next_game_info['dates'][0]['games'][0]['teams']['away']['team']['id']
    return home_team, home_team_ID, away_team, away_team_ID

def get_team_arena_name(team_id):
    """ Function to get team of user and return arena name"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())

    for team in results['teams']:
        if team['id'] == team_id:
            arena = team['venue']['name']
            return arena
            
    raise Exception("Could not find arena name for team {0}".format(team_id))

def get_team_arena_city(team_id):
    """ Function to get team of user and return arena location"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())

    for team in results['teams']:
        if team['id'] == team_id:
            city = team['venue']['city']
            return city
            
    raise Exception("Could not find arena city for team {0}".format(team_id))

def get_team_history(team_id):
    """ Function to get team franchise start date"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())

    for team in results['teams']:
        if team['id'] == team_id:
            firstYearOfPlay = team['firstYearOfPlay']
            return firstYearOfPlay
            
    raise Exception("Could not find history info for team {0}".format(team_id))

def get_team_division_info(team_id):
    """ Function to get team of user and return division name"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())

    for team in results['teams']:
        if team['id'] == team_id:
            division = team['division']['name']
            return division
            
    raise Exception("Could not find division info for team {0}".format(team_id))

def get_team_conference_info(team_id):
    """ Function to get team of user and return conference name"""

    fn = open('{0}teams.json'.format(NHL_API_URL), "r")
    results = json.loads(fn.read())

    for team in results['teams']:
        if team['id'] == team_id:
            conference =  team['conference']['name']
            return conference
            
    raise Exception("Could not find conference info for team {0}".format(team_id))



''' future use
**************

**************
'''

def get_teams():
    """ Function to get a list of all the teams name"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()
    teams = []

    for team in results['teams']:
        teams.append(team['franchise']['teamName'])

    return teams

def get_logos():
    """ Function to get team_ID number then return team logo
        #https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/10.svg   TML logo"""

    url = '{0}teams'.format(NHL_API_URL)
    response = requests.get(url)
    results = response.json()

    for team in results['teams']:
        if team['franchise']['teamName'] == team_name:
            return team['id']

    raise Exception("Could not find ID for team {0}".format(team_name))

def get_next_game_info(team_id):
    """ Function to get game info (both team names etc) for next game that team_id plays"""

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    try:
        game = requests.get(url).json()
        homeTeamScore = int(game['dates'][0]['games'][0]['teams']['home']['score'])
        homeTeamName = game['dates'][0]['games'][0]['teams']['home']['team']['name']
        awayTeamScore = int(game['dates'][0]['games'][0]['teams']['away']['score'])
        awayTeamName = game['dates'][0]['games'][0]['teams']['away']['team']['name']

        # Print score for test
        #print("Score: {0} Time: {1}:{2}:{3}".format(score, now.hour, now.minute, now.second),end='\r')
        print("Next game is", homeTeamName, "at home against", awayTeamName)

        return

    except requests.exceptions.RequestException:
        print("Error encountered, returning 0 for score")
        return 0

def fetch_home_name(team_id):
    """ Function to get the home team name of the game depending on the chosen team.
    Inputs the team ID and returns the home team name found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    try:
        score = requests.get(url).json()

        #game_time = str(score['dates'][0]['games'][0]['teams'])
        #print (game_time)
        
        game = requests.get(url).json()
        homeTeamScore = int(game['dates'][0]['games'][0]['teams']['home']['score'])
        homeTeamName = game['dates'][0]['games'][0]['teams']['home']['team']['name']
        awayTeamScore = int(game['dates'][0]['games'][0]['teams']['away']['score'])
        awayTeamName = game['dates'][0]['games'][0]['teams']['away']['team']['name']
        homeTeamID = int(score['dates'][0]['games'][0]['teams']['home']['team']['id'])

        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])

        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        print(homeTeamName, str(homeTeamScore), ":", str(awayTeamScore), awayTeamName, ", Time: {0}:{1}:{2}  ".format(now.hour, now.minute, now.second),end='\r')
        return homeTeamName, homeTeamID

    except requests.exceptions.RequestException:
        print("Error encountered, returning no home team name found")
        return 0

def fetch_away_name(team_id):
    """ Function to get the away team name of the game depending on the chosen team.
    Inputs the team ID and returns the away team name found on web. """

    # Get current time
    now = datetime.datetime.now()

    # Set URL depending on team selected
    url = '{0}schedule?teamId={1}'.format(NHL_API_URL, team_id)
    # Avoid request errors (might still not catch errors)
    try:
        score = requests.get(url).json()

        #game_time = str(score['dates'][0]['games'][0]['teams'])
        #print (game_time)
        
        game = requests.get(url).json()
        homeTeamScore = int(game['dates'][0]['games'][0]['teams']['home']['score'])
        homeTeamName = game['dates'][0]['games'][0]['teams']['home']['team']['name']
        awayTeamScore = int(game['dates'][0]['games'][0]['teams']['away']['score'])
        awayTeamName = game['dates'][0]['games'][0]['teams']['away']['team']['name']
        awayTeamID = int(score['dates'][0]['games'][0]['teams']['away']['team']['id'])

        if int(team_id) == int(score['dates'][0]['games'][0]['teams']['home']['team']['id']):
            score = int(score['dates'][0]['games'][0]['teams']['home']['score'])

        else:
            score = int(score['dates'][0]['games'][0]['teams']['away']['score'])

        # Print score for test
        #print(homeTeamName, str(homeTeamScore), ":", str(awayTeamScore), awayTeamName, ", Time: {0}:{1}:{2}  ".format(now.hour, now.minute, now.second),end='\r')
        return awayTeamName, awayTeamID

    except requests.exceptions.RequestException:
        print("Error encountered, returning no away team name found")
        return 0

def get_next_game_info3(team_id):
    "get the team IDs of the next game"
    date_test = datetime.date.today()
    gameday = check_game_status(team_id, date_test)

    #Keep going until game day found
    while ("Scheduled" not in gameday):
        date_test = date_test + datetime.timedelta(days=1)
        gameday = check_game_status(team_id, date_test)

    #Get start time of next game
    url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id, date_test)
    #print(url)
    next_game_info = requests.get(url).json()
    home_id = next_game_info['dates'][0]['games'][0]['teams']['home']['team']['id']
    away_id = next_game_info['dates'][0]['games'][0]['teams']['away']['team']['id']
    return home_id, away_id

def convert_to_local_time(utc_game_time):
    "convert to local time from UTC"
    utc_game_time = datetime.datetime.strptime(utc_game_time, '%Y-%m-%dT%H:%M:%SZ') #with time zone
    utc_game_time = utc_game_time.replace(tzinfo=tz.tzutc())
    local_game_time = utc_game_time.astimezone(tz.tzlocal())

    return local_game_time

def game_start_delay(team_id,date):
    url = '{0}schedule?teamId={1}&date={2}'.format(NHL_API_URL, team_id,date)

    is_game_started = False

    while is_game_started:
        try:
            #get game state from API (no state when no games on date)
            gamePK = requests.get(url).json()
            gamePK = gamePK['dates'][0]['games'][0]['gamePk']

            url = '{0}game/{1}/feed/live'.format(NHL_API_URL,gamePK)
            live_feed = requests.get(url).json()
            #url = '{0}game/{1}/content'.format(NHL_API_URL,gamePK)
            #game_content = requests.get(url).json()
            #game_content = game_content['media']['milestones']['items'][1]['timeAbsolute']

            live_feed = live_feed['liveData']['linescore']['periods'][0]['startTime']
            live_feed = convert_to_local_time(live_feed)

            live_feed = live_feed.strftime("%X")
            live_feed = datetime.datetime.strptime(live_feed, '%H:%M:%S')
            goal_pressed = input("Press any key when period starts")
            now_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%X"), '%H:%M:%S')
            delay_count = now_time - live_feed
            is_game_started = False
            return delay_count

        except IndexError:
            #Return No Game when no state available on API since no game
            is_game_started = True
            pass

        except requests.exceptions.RequestException:
            # Return No Game to keep going
            is_game_started = True
            pass

        except KeyError:
            is_game_started = True
            pass
