#!/usr/bin/python

import datetime
import os
import pause
from lib import nhl
from lib import light

#light.activate_goal_light()

def setup_nhl():
    """Function to setup the nhl_goal_light.py with team,
    team_id and delay"""

    """Try to find a settings.txt file in the folder to automaticly setup
    the goal light with pre-desired team and delay.
    settings.txt file should as such : Enter team_id and delay,
    each on a separate line in this order. LEAVE EMPTY if you want to
    manually input every time. If program can't find settings.txt file or if
    file is empty, it will ask for user input.
    """

    lines = ""
    team = ""
    team_id = ""
    #settings_file = '/home/pi/nhl_goal_light/settings.txt'
    settings_file = 'settings.txt'
    if os.path.exists(settings_file):
        # get settings from file
        f = open(settings_file, 'r')
        lines = f.readlines()

    # find team_id
    try:
        #team_id = lines[1].strip('\n')
        team = lines[1].strip('\n')
        team_id = nhl.get_team_id(team)
    except IndexError:
        team_id = ""
    if team_id == "":
        team = input("Enter team you want to setup (without city) (Default: Canadiens) \n")
        if team == "":
            team = "Canadiens"
        else:
            team = team.title()
        # query the api to get the ID
        team_id = nhl.get_team_id(team)

    # find delay
    try:
        delay = lines[2].strip('\n')
    except IndexError:
        delay = ""
    if delay == "":
        delay = input("Enter delay required to sync : \n")
        if delay == "":
            delay = 0
    delay = float(delay)

    return (team_id, delay)


if __name__ == "__main__":

    old_score = 100
    new_score = 0
    gameday = False
    season = False
    delay_checked = False

    light.setup()
    team_id, delay = setup_nhl()
    print ("Team ID : {0} \nDelay to use : {1}\n".format(team_id,delay))
    try:

        today = datetime.date.today()
        
        while (True):
            pause.milliseconds(500)
            game_status = nhl.check_game_status(team_id,today)
            #print("game status is: ", game_status)
            if ('In Progress' in game_status) or ('Pre-Game' in game_status):

                if not delay_checked:
                    delay_checked = True
                    answer = input("do you want to check for delay? [yes]")
                    if (answer == "yes"):
                        start_delay = nhl.game_start_delay(team_id,today)
                        answer = input("delay is of {0}, do you want to update current delay ({1})? ".format(start_delay,delay))
                        if (answer == "yes"):
                            delay = input("Enter new delay : ")
                # check game
                # Check score online and save score
                new_score = nhl.fetch_score(team_id)
                # If score change...
                if new_score != old_score:
                    if new_score > old_score:
                        pause.seconds(delay)
                        # save new score
                        print("GOAL!")
                        # activate_goal_light()
                        light.activate_goal_light()
                    old_score = new_score

            else:
                if ('Final' in game_status):
                    light.cleanup()
                    print ("Game ended, cleanning up!")
                
                old_score = 100 # Reset for new game   
                
                #next_game_date = nhl.get_next_game_date(team_id)
                next_game_date = nhl.get_next_game_date(team_id)
               
                #print (str(next_game_info)) returns ('Home Team is ', 'Chicago Blackhawks', ', Away Team is ', 'San Jose Sharks')
                #next_game_info = nhl.get_next_game_info(team_id)
                #above will show previous game after game ended, doesn't show future game probably because its same day                
              

               
                print ("Going to sleep until start of next game : " + str(next_game_date))
                pause.until(next_game_date)
                today = datetime.date.today()


    except KeyboardInterrupt:
        print("\nCtrl-C pressed")
        light.cleanup()