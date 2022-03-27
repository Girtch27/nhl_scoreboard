import requests
import datetime
from dateutil import tz
import pause
import json

NHL_API_URL = "http://statsapi.web.nhl.com/api/v1/schedule?teamId="
# format is http://statsapi.web.nhl.com/api/v1/schedule?teamId=10&date=2022-02-14

def get_content_url(team_id, date):
    """ Function to get game content url which is used later for media links fo goal replays"""
    
    # Set URL depending on team selected
    url = '{0}{1}&date={2}'.format(NHL_API_URL, team_id, date)
    response = requests.get(url).json()
    #print('game url: ' + url)
    
    try:
        content_url = response['dates'][0]['games'][0]['content']['link']
        #print('content url: ' + content_url)
        content_url = ('http://statsapi.web.nhl.com/' + content_url)
        print('game url: ' + url)
        return content_url

    except requests.exceptions.RequestException:
        print("Error encountered, returning error")
        content_url = 'error'
        return content_url

def get_video_url(team_id, url):
    """ Function to get all goal's descriptions and video highlight video URL for team_ID at url"""
    """ returns only the last goal info"""
    highlight_videoURL = ""
    response = requests.get(url).json()
    milestones = response['media']['milestones']['items']
    print('game media url: ' + url + ' teamID: ' + str(team_id))
        
    for item_type in milestones: #and (team is team_id))
        if ((item_type['title'] == 'Goal') and (item_type['teamId'] == team_id)):
            description = item_type['description']
            highlight_description = item_type['highlight']['description']
            highlight_videoURL = item_type['highlight']['playbacks'][0]['url'] #0 url for 320x180, 2 is 640x360
            print('Goal video url '  + highlight_videoURL)

    return highlight_videoURL

def get_goal_description(team_id, url):
    """ Function to get all goal's descriptions and video highlight video URL for team_ID at url"""
    """ returns only the last goal info"""
    description = ""
    highlight_description = ""
    playerID = ""
    team_id_str = str(team_id)
    response = requests.get(url).json()
    milestones = response['media']['milestones']['items']
        
    for item_type in milestones: #and (team is team_id))
        if ((item_type['title'] == 'Goal') and (item_type['teamId'] == team_id_str)):
            if 'highlight' in item_type:
                if 'description' in item_type['highlight']:
                    if item_type['description'] is not "" and item_type['highlight']['description'] is not "":
                        description = item_type['description']
                        highlight_description = item_type['highlight']['description']
                        playerID = item_type['playerId']
                        print('Goal by '  + description + ', ' + highlight_description)
        
    return description, highlight_description, playerID