from asyncio import sleep
from multiprocessing.connection import wait
from random import randint, random
from secrets import choice
from tkinter import *
from tkinter import ttk
import time
import requests
from datetime import date, datetime, timedelta
import schedule

''' video stuff '''
from tkvideo import tkvideo
#from tkVideoPlayer import TkinterVideo

'''image stuff'''
#from io import BytesIO
import cairosvg
from PIL import ImageTk, Image

''' OS parts '''
import os
#import datetime
#import os #used to find config file and\or save status to file
import pause

'''my library NHL portion'''
from lib import nhl, alert, media, nhlplayer

# Creating a GUI Windows
window = Tk()
#mainframe = ttk.Frame(window, padding="1 1 1 1")
mainframe = ttk.Frame(window, padding="0 0 0 0")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
window.columnconfigure(0, weight=0)
window.rowconfigure(0, weight=0)
#window_popup = Tk()

#Create left pane
left_pane = ttk.PanedWindow(mainframe)
left_pane.grid(row=0, column=0, sticky="nsew")
left_pane_frame = ttk.Frame(left_pane, width=100)
left_pane.add(left_pane_frame)

# Create right pane
right_pane = ttk.PanedWindow(mainframe)
right_pane.grid(row=0, column=1, sticky="nsew")
right_pane_frame = ttk.Frame(right_pane, width=100)
right_pane.add(right_pane_frame)

window.title("NHL Scoreboard") #gets changed below after Team to follow is determined

#set window color
bgcolorDefault = window.cget("background") #get default color to store to later change back too
window.configure(background=bgcolorDefault) #set back to default color

original_bgcolor = "white"
original_bgcolor = "light grey" #original_bgcolor is user selected color
original_bgcolor = "light blue" #original_bgcolor is user selected color
original_bgcolor = bgcolorDefault #original_bgcolor is user selected color

bgcolor = original_bgcolor #bgcolor used by all widgets
window['bg']= bgcolor

# window size
window_width = 1200 #900
window_height = 600 #600

# get the screen dimension
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# find the center point main window
offset_x = 0 #350, set to 0 to be center or XXX to shift over
offset_y = 0 #set to 0 to center or YYY to shift over
center_x = int((screen_width/2 - window_width/2) + offset_x)
center_y = int((screen_height/2 - window_height/2) + offset_y)
# set the position of the window to the center of the screen, window.geometry("800x600+200+200")
#window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}") #centred windowed size set above

#full sized window based on screen size
window.geometry(f"{screen_width}x{screen_height}+{0}+{0}") #full sized window based on screen size


content_date = date.today()
content_date = content_date.strftime('%Y-%m-%d') #format should end us as "2022-02-22"
print(content_date)
    
'''
guides and resources
tkinter
https://pythonguides.com/python-tkinter-label/

Gitub
https://github.com/199-cmd/ChangeImageInTkinter
https://github.com/arim215/nhl_goal_light
https://github.com/rpi-ws281x/rpi-ws281x-python #get led lights working
'''

''' Initialize '''
roster_counter = 0
num_roster_players = 20 #2g, 6d, 12f. during roster() find number of players on roster
delay_checked = False #delay_checked
delay = 0.0 #delay used before starting goal notifications, set to 0 and see if too early compared to TV??
delay = float(delay) #delay used before starting goal notifications
gameInfoUpdated = False #update game info flag
updateSpeed = int(10*1000) #delay before checking game status & game scores
game_status = "waiting"
old_score = 100 #old_score for followed team, play notification
new_score = 0 #new score for followed team, play notification
home_score = 0 #home score for GUI
away_score = 0 #away score for GUI
old_home_score = 0
old_away_score = 0
away_name = "" #away name ex Maple Leafs
away_team = "" #away team name GUI ex Toronto Maple Leafs
home_name = "" #home name ex Maple Leafs
home_team = "" #home team name GUI ex Toronto Maple Leafs
away_team_ID = "10"
home_team_ID = "10"
gameday = False #gameday status
season = False #season
home_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")
away_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")

#my own class NHLPlayer in file player.py
#from nhlplayer import NHLPlayer
#player = nhlplayer.NHLPlayer("8478483") #Marner is 8478483, Mathews is 8479318
#print(player.fullname)

TeamRoster = []

MM16 = "8478483" #mitch
AM34 = "8479318" #mathews
JT91 = "8475166" #taveras
WN88 = "8477939" #Nylandr
JC36 = "8475789" #Campbell
MB58 = "8478047" #bunting
MR44 = "8476853" #reilly

TeamRoster.extend([MM16,AM34,JT91,WN88,JC36,MB58,MR44])
profile_player = choice(TeamRoster) #pick random person to start up


def checkConnected():
    url = "http://www.nhl.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to: " + url)
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("No internet connection. Timed out after " + str(timeout) + " seconds!!!")
        #sleep(600) #10mins, in seconds
        retry = 10*60*1000
        window.after(retry, checkConnected) #retry after Xms, must be cancel, idle, info, or an integer

'''check internet see if www.nhl.com replies'''
checkConnected()


#default
skater_default = nhlplayer.NHLPlayer(profile_player)
print(skater_default.fullname)

#myTeam is the team I want to follow
myTeam = "Hurricanes"
myTeam = "Panthers"
myTeam = "Sharks"
myTeam = "Wild"
myTeam = "Golden Knights"
myTeam = "Canadiens"
myTeam = "Stars"
myTeam = "Lightning"
myTeam = "Senators"
myTeam = "Flames"
myTeam = "Lightning"
myTeam = "Oilers"
myTeam = "Oilers"
myTeam = "Devils"
myTeam = "Islanders"
myTeam = "Rangers"
myTeam = "Maple Leafs" #default

window.title(myTeam + ' NHL Scoreboard')
ScoreVerse = "vs"

'''
#960x640, need to resize to be smaller before opening
default image set to NHL logo
'''

drSVG = '/home/pi/nhl_scoreboard/images/SVG/'
drPNG = '/home/pi/nhl_scoreboard/images/PNG/'
img_width = 200
img_height = int(img_width * 200/227) #keep ratio of 960x640\

'''load in all PNG and resize them to be used later'''

img = []
home_logo = []
imgPNG = os.listdir(drPNG)

for imgToOpen in imgPNG:
    img = Image.open(drPNG+imgToOpen)
    home_logo = ImageTk.PhotoImage(img)
    #print(drPNG+imgToOpen)
    #print(img)


alert.setup() #lights and music\audio
#print ("Team ID : {0} \nDelay to use : {1}\n".format(team_id,delay))
print ("Delay to use : {0}\n".format(delay))

def utilsVideo():
    '''play a video highlight'''
    #window_popup()
    ''' video stuff '''
    ''' pip3 install tkvideo '''
    
    video_label = LabelMedia
    
    #read video to display on label
    video_url = "https://hlslive-wsczoominwestus.med.nhl.com/editor/bec9b46f-07af-4a7a-9c06-c5899da0843a.mp4"
    video_url = "https://hlslive-wsczoominwestus.med.nhl.com/editor/dc6c3957-01cb-40a0-93e3-47247d1e1b5d.mp4" #FLASH_1200K_640X360"
    video_url = "https://hlslive-wsczoominwestus.med.nhl.com/editor/c9f56ab7-04e4-4f16-82ac-14a5fe6918e3.mp4" #FLASH_192K_320X180"
    
    content_team_id = "10"
    content_date = "2022-02-26" #Marner 4 goal game
    content_url = media.get_content_url(content_team_id, content_date)
    #print('content_url returned is: ' + content_url)
    video_url = media.get_video_url(content_team_id, content_url)
    #print('info returned is ' + description + highlight_description + video_url)
    player = tkvideo(video_url, video_label, loop = 0, size = (320, 180), hz = 60)
    player.play()
    description, highlight_description, playerID = media.get_goal_description(content_team_id, content_url)
    highlight_description1, highlight_description2 = split(highlight_description)
    LabelDesc3["text"] = 'Goal!!! {0}'.format(description)
    LabelDesc4["text"] = '{0}'.format(highlight_description1)
    LabelDesc5["text"] = '{0}'.format(highlight_description2)

def utilsVideoStop():
    #video_label.pack_forget()
    #player.play()
    video_label_pic= Image.open('/home/pi/nhl_scoreboard/images/PNG/NHL.png')
    video_label = ImageTk.PhotoImage(video_label_pic)

def newWindow():
    window_popup = Toplevel(window)
    
    # find the center point popup window
    window_popup_window_width = 320 #640
    window_popup_window_height = 180 #360
    window_popup_offset_x = offset_x #set to window's offset_x, or use something else, 0 to be center or XXX to shift over
    window_popup_offset_y = (window_height/2/2)+30 #set to window's bottom edge, so 1/2
    window_popup_center_x = int((screen_width/2 - window_popup_window_width/2) + window_popup_offset_x)
    window_popup_center_y = int((screen_height/2 - window_popup_window_height/2) + window_popup_offset_y)
    window_popup.geometry(f'{window_popup_window_width}x{window_popup_window_height}+{window_popup_center_x}+{window_popup_center_y}')
    window_popup.title("Media Highlights")
    
    # create label
    video_label = Label(window_popup)
    video_label.pack()
    #wait until ended or stoppe then use    Toplevel(window).destroy()


''' TkinterVideo  
    videoplayer = TkinterVideo(master=window_popup, scaled=True, pre_load=False)
    videoplayer.load(video)
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play() # play the video
'''

def logo(image1, image2):
    global home_logo
    global away_logo
    imagename1 = str(image1) + '.png' #convert ID# integer  to string with .png
    default = imgPNG.index(imagename1) #find default image's index in imgPNG list
    defaultIMG1 = drPNG+str(imgPNG[default]) #combine dir and image filename to create file location
    imgX1= Image.open(defaultIMG1)
    home_logo = ImageTk.PhotoImage(imgX1)
    
    imagename2 = str(image2) + '.png' #convert ID# integer  to string with .png
    default = imgPNG.index(imagename2) #find default image's index in imgPNG list
    defaultIMG2 = drPNG+str(imgPNG[default]) #combine dir and image filename to create file location
    imgX2= Image.open(defaultIMG2)
    away_logo = ImageTk.PhotoImage(imgX2)

def updateGamesPlayed(record):
    #gets team record and converts to W, L, OTL then to games played and remaining games
    split = record.rsplit()
    split = split[0].rsplit("-")
    W = int(split[0])
    L = int(split[1])
    OTL = int(split[2])
    GP = W + L + OTL
    GR = 82 - GP
    GP_GR = str(GP) + 'gp | ' + str(GR) + 'gr'
    return GP_GR

def updateTeamInfo(nextGameDate):
    '''update info only before or after a game, not during'''
    global away_team_ID
    global home_team_ID
    global gameInfoUpdated
    
    LabelCityAway["text"] = nhl.get_team_arena_city(away_team_ID)
    LabelArenaAway["text"] = nhl.get_team_arena_name(away_team_ID)
    LabelHistoryAway["text"] = 'Founded in ' + nhl.get_team_history(away_team_ID)
    LabelDivisionAway["text"] = nhl.get_team_division_info(away_team_ID) + ' Division'
    LabelConferenceAway["text"] = nhl.get_team_conference_info(away_team_ID) + ' Conference'   
    LabelRecordAway["text"] = nhl.get_team_record_info(away_team_ID, nextGameDate)
    LabelGamesAway["text"] = updateGamesPlayed(LabelRecordAway["text"])

    LabelCityHome["text"] = nhl.get_team_arena_city(home_team_ID)
    LabelArenaHome["text"] = nhl.get_team_arena_name(home_team_ID)
    LabelHistoryHome["text"] = 'Founded in ' + nhl.get_team_history(home_team_ID)
    LabelDivisionHome["text"] = nhl.get_team_division_info(home_team_ID) + ' Division'
    LabelConferenceHome["text"] = nhl.get_team_conference_info(home_team_ID) + ' Conference'
    LabelRecordHome["text"] = nhl.get_team_record_info(home_team_ID, nextGameDate)
    LabelGamesHome["text"] = updateGamesPlayed(LabelRecordHome["text"])
    
def donothing():
    filewin = Toplevel(window)
    button = Button(filewin, text="Do nothing button")
    button.pack()
    
def setup():
    '''verify or setup somthing goes here'''
    
def utilsMode():
    '''use local JSON file instead of www.nhl.com live data'''
    global original_bgcolor #original background colour
    global bgcolor #background colour
    #set window color
    current_color = window.cget("background")
    if current_color != "yellow":
        bgcolor = "yellow"
    else:
        bgcolor = original_bgcolor
    window['bg']= bgcolor

def utilsAudio():
    '''verify or setup somthing goes here'''
    
    '''check light and audio'''
    #alert.activate_goal_light() # play a test sound?
    alert.activate_audio('Another One Bites The Dust')

def utilsImgtoPNG():
    '''convert all svg files one dir and save as PNG to another'''
    global img_width
    global img_height
    global drSVG
    global drPNG
    
    for file in os.listdir(drSVG):
        #if os.path.isfile(file) and file.endswith(".svg"):
        if file.endswith(".svg"):
            name = file.split('.svg')[0]
            print(name)
            #cairosvg.svg2png(url='https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/1.svg',write_to=name+'/home/pi/nhl_scoreboard/images/y.png')
            cairosvg.svg2png(url=drSVG+name+'.svg',write_to=drPNG+name+'.png',parent_width=img_width, parent_height=img_height)
   
def split(string_to_split):
    #take a string that is too long and split into 2 smaller strings
    line1 = ""
    line2 = ""
    length = 70
    if len(string_to_split) > length: #split long desc into two lines
        midpos = string_to_split.rindex(" ", 0, length + 1)
        string1 = slice(0, midpos, 1) 
        string2 = slice(midpos, 140, 1)
        line1 = (string_to_split[string1])
        line2 = (string_to_split[string2] + "...")
        line2 = line2.lstrip()
    else: # keep short strings into 1 desc
        line1  = string_to_split
        line2 =  ""
    return line1, line2
        
def get_goal_info(content_team_id):
    global new_score
    video_label = LabelMedia
    
    content_date = date.today()
    content_date = content_date.strftime('%Y-%m-%d') #format should end us as "2022-02-22"
    
    #content_team_id = "10"
    #content_date = "2022-02-22" #for debug when using local json file
    
    print('check for media content...')
    #time.sleep(60) #wait 2 mins for media content to be ready
    content_url = media.get_content_url(content_team_id, content_date)
    #print('content_url returned is: ' + content_url)
    video_url = media.get_video_url(content_team_id, content_url)
    #print('info returned is ' + description + highlight_description + video_url)
    
    '''
    player = tkvideo(video_url, video_label, loop = 0, size = (320, 180), hz = 60)
    player.play()
    '''

    description, highlight_description, playerID, goal_count = media.get_goal_description(content_team_id, content_url)
    if (description is not ""):
        LabelDesc3["text"] = 'Goal {0}! {1}'.format(goal_count, description)
        #split returned description to two lines
        highlight_description1, highlight_description2 = split(highlight_description)
        LabelDesc4["text"] = '{0}'.format(highlight_description1)
        LabelDesc5["text"] = '{0}'.format(highlight_description2)
        skater_scored = nhlplayer.NHLPlayer(playerID)
        update_player_info(skater_scored)

        if goal_count == new_score and highlight_description == "getting goal highlights...":
            print("cancel schedule................... " + str(goal_count))
            return schedule.CancelJob #cancel schedule if all goal descriptions returned until next goal detected
        print("keep schedule running................... " + str(goal_count))

    else:
        LabelDesc3["text"] = 'Getting goal info ... '.format()
        LabelDesc4["text"] = ''.format()
        LabelDesc5["text"] = ''.format()

def roster_update():
    global myTeam
    global roster_counter
    global num_roster_players
    global TeamRoster
    
    if roster_counter == 0:
        team_id = nhl.get_team_id(myTeam)
        TeamRoster = nhlplayer.NHLRoster(team_id)
        num_roster_players = len(TeamRoster.rosterIDs)
        print("# players on roster:" + str(num_roster_players))
    #print("count:" + str(roster_counter) + ", of total#:" + str(num_roster_players))
    skater = nhlplayer.NHLPlayer(TeamRoster[roster_counter])
    update_player_info(skater)

    roster_counter = roster_counter + 1
    if roster_counter == (num_roster_players - 1): #last player, reset counter
        roster_counter = 0

def update_player_info(Player):
    LabelPlayerPic.configure(image=Player.image)
    LabelPlayerPic.image = Player.image

    if Player.alternate_captain == True:
        LabelPlayerDesc1["text"] = Player.fullname + " \"A\"" + " | " + Player.number

    elif Player.captain == True:
        LabelPlayerDesc1["text"] = Player.fullname + " \"C\"" + " | " + Player.number 

    else:
        LabelPlayerDesc1["text"] = Player.fullname + " | " + Player.number 

    if Player.position_abbreviation == "G" or Player.position_abbreviation == "g":
        LabelPlayerDesc2["text"] = Player.size + ", " + Player.position + ", Catches " + Player.hand
    else:
        LabelPlayerDesc2["text"] = Player.size + ", " + Player.position + ", Shoots " + Player.hand
    LabelPlayerDesc3["text"] = "Birthday: " + Player.birthday + ", Age " + str(Player.age)
    if Player.state_province == "n\a": #some players don't have states or provinces
         LabelPlayerDesc4["text"] = "Born: " + Player.city + ", " + Player.country
    else:
        LabelPlayerDesc4["text"] = "Born: " + Player.city + ", " + Player.state_province + ", " + Player.country
    LabelPlayerDesc5["text"] = "Nationality: " + Player.nationality
    LabelPlayerDesc6["text"] = ""
    LabelPlayerDesc7["text"] = ""
    LabelPlayerDesc8["text"] = ""
    #time.sleep(1)         

def update():
    global bgcolor #background colour
    global delay #delay before starting goal notification
    global gameInfoUpdated #update game info flag
    global updateSpeed #delay before checking game status & game scores
    global game_status
    global old_score #old_score for followed team, play notification
    global new_score #new score for followed team, play notification
    global home_score #home score for GUI
    global away_score #away score for GUI
    global old_home_score
    global old_away_score
    global away_name #away name for GUI
    global away_team #away team name ex Toronto Maple Leafs
    global home_name #home name for GUI
    global home_team #home team name ex Toronto Maple Leafs
    global home_logo
    global away_logo
    global away_team_ID
    global home_team_ID

    '''check internet see if www.nhl.com replies'''
    checkConnected()

    '''get info from NHL.com'''
    #print (game_status)
    team_id = nhl.get_team_id(myTeam)
    today = date.today()

    game_status = nhl.check_game_status(team_id,today) #send team_id and today's date, get back game status
        
    if (gameInfoUpdated is False): #update game info
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        logo(home_team_ID, away_team_ID) #home_logo , away_logo
        updateTeamInfo(nextGameDate)
        gameInfoUpdated = True #update game info flag
        print('Game info updated. ' +  ' Home: ' + str(home_team) + str(home_team_ID) + ', Away: ' + str(away_team) + str(away_team_ID))
            
    if ('No Game' in game_status):
        #get_goal_info(team_id)
        
        #no game today, find next game info  
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        print(game_status + ' today, next game is: ' + str(home_team) + ' vs ' + str(away_team))
        updateSpeed = int(30*60*1000) # 30mins, delay as game hasn't started
        
        next_game_date_24hr, next_game_day, next_game_date_12hr  = nhl.get_next_game_date(team_id)
        today = date.today()
        next_home_team = home_team #set next game info and keep today's game info separate
        next_away_team = away_team #set next game info and keep today's game info separate
                
        if (today == next_game_day):
            game_status = nhl.check_game_status(team_id,today) #send team_id and today's date, get back game status
         
        '''Update GUI info'''
        LabelAwayScore["text"] = "-"
        LabelHomeScore["text"] = "-"
        LabelAwayName["text"] = next_away_team #was away_name
        LabelHomeName["text"] = next_home_team #was home_name   
         
        if (team_id == away_team_ID):
            LabelDesc1["text"] = '{0} (away) vs {1} (home)'.format(away_team, home_team)
        else:
            LabelDesc1["text"] = '{0} (home) vs {1} (away)'.format(home_team, away_team)
        if (today == next_game_day):
            LabelDesc2["text"] = '{0} next game is TODAY! {1}'.format(myTeam, next_game_date_12hr)
        else:
            LabelDesc2["text"] = '{0} next game is {1}'.format(myTeam, next_game_date_12hr)
        LabelDesc3["text"] = ""
        LabelDesc4["text"] = ""
        LabelDesc5["text"] = ""
        roster_update()
                
    elif ('Scheduled' in game_status):
        #game later today, find next game info
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        print(game_status + ', game today: ' + str(home_team) + ' vs ' + str(away_team))
        updateSpeed = int(2*60*1000) # 2min, delay as game hasn't started
        next_game_date_24hr, next_game_day, next_game_date_12hr  = nhl.get_next_game_date(team_id)
        today = date.today()
        LabelAwayName["text"] = away_team #was away_name
        LabelHomeName["text"] = home_team #was home_name
        LabelAwayScore["text"] = "-"
        LabelHomeScore["text"] = "-"
        if (team_id == away_team_ID):
            LabelDesc1["text"] = '{0} (away) vs {1} (home)'.format(away_team, home_team)
        else:
            LabelDesc1["text"] = '{0} (home) vs {1} (away)'.format(home_team, away_team)
        LabelDesc2["text"] = '{0} next game is TODAY! {1}'.format(myTeam, next_game_date_12hr)
        LabelDesc3["text"] = ""
        LabelDesc4["text"] = ""
        LabelDesc5["text"] = ""
        roster_update()
    
    elif ('In Progress' in game_status) or ('Pre-Game' in game_status):
        new_score, home_score, away_score  = nhl.fetch_scores(team_id)
        
        if ('Pre-Game' in game_status):
            LabelAwayName["text"] = away_team
            LabelHomeName["text"] = home_team
            LabelAwayScore["text"] = "0"
            LabelHomeScore["text"] = "0"
            updateSpeed = int(60*1000) # 1min, delay as game hasn't started
            LabelDesc1["text"] = '{0} warmups, get ready!'.format(game_status)
            LabelDesc2["text"] = ""
            LabelDesc3["text"] = ""
            LabelDesc4["text"] = ""
            LabelDesc5["text"] = ""
            roster_update()

        else:
            LabelAwayName["text"] = away_team
            LabelHomeName["text"] = home_team
            LabelDesc1["text"] = 'Game {0}!'.format(game_status)
            updateSpeed = int(1250) # 1sec, game on check often
            LabelDesc2["text"] = ""
            print(game_status + ':' + str(updateSpeed) + '. home:' + str(home_score) + ', away:' + str(away_score))
 
            '''Update GUI info'''
            LabelAwayScore["text"] = away_score
            LabelHomeScore["text"] = home_score
             
            '''Detect if score changed...'''
            if ((home_score > old_home_score) and (team_id is home_team_ID)) or ((away_score > old_away_score) and (team_id is away_team_ID)):
                LabelDesc2["text"] = "GOAL!"
                old_home_score = home_score
                old_away_score = away_score
                old_score = new_score
                alert.activate_goal_audio()
                get_goal_info(team_id)
                schedule.every(90).seconds.do(get_goal_info, content_team_id=team_id)
                #schedule.every(30).seconds.at_time(time.noe + 2 mins).do(get_goal_info, content_team_id=team_id) #schedule in 2mins to run every 30secs 
                print('goal detected.....')
                
            if (home_score < old_home_score) or (away_score < old_away_score):
                #score error, score decreased somehow
                old_home_score = home_score
                old_away_score = away_score
                

    elif ('Final' in game_status) or ('Game Over' in game_status):
        updateSpeed = int(30*60*1000) # 30mins
        #alert.cleanup()
        gameInfoUpdated = False #update game info flag
        schedule.CancelJob #cancel schedule until next goal detected, don't want schedule to run during a late game next day
        print (game_status + ':' + str(updateSpeed) + ". Game ended, cleaning up!")
        
        #put something here for game ended, team won
        
        '''Update GUI info'''
#         LabelAwayScore["text"] = away_score
#         LabelHomeScore["text"] = home_score
#         LabelAwayName["text"] = away_team
#         LabelHomeName["text"] = home_team
#         if (team_id == away_team_ID): #if myteam's ID is away team and they win or lost
#             if (old_away_score > old_home_score):
#                 LabelDesc1["text"] = '{0} status is {1}. {0} won!'.format(myTeam, game_status)
#                 alert.activate_audio('Another One Bites The Dust')
#             else:
#                 LabelDesc1["text"] = '{0} status is {1}. {0} lost!'.format(myTeam, game_status)
#         elif (team_id == home_team_ID): #if myteam's ID is away team and they win or lost
#             if (old_home_score > old_away_score):
#                 LabelDesc1["text"] = '{0} status is {1}. {0} won!!!'.format(myTeam, game_status)
#                 alert.activate_audio('Another One Bites The Dust')
#             else:
#                 LabelDesc1["text"] = '{0} status is {1}. {0} lost!!!'.format(myTeam, game_status)
#                 print(str(old_home_score) + ',' + str(old_away_score))
#         
#         else:
#             LabelDesc1["text"] = '{0} : {1}. {2} INVALID Result!'.format(myTeam, team_id, game_status)

        LabelDesc1["text"] = ""
        LabelDesc2["text"] = ""
        LabelDesc3["text"] = ""
        LabelDesc4["text"] = ""
        LabelDesc5["text"] = ""

 
    else:
        print(game_status + ':' + str(updateSpeed) + ". ***invalid state***")
        updateSpeed = int(30*60*1000) # 30mins
        
    # save the panel's image from 'garbage collection'
    # panel1.image = image1
    LabelHomePic.configure(image=home_logo)
    LabelAwayPic.configure(image=away_logo)
    LabelHomePic.image = home_logo
    LabelAwayPic.image = away_logo

 
    '''run schedule(s)'''
    schedule.run_pending()
    print("run pending schedules...")
    
    #window.after(updateSpeed, update) #run update function after Xms, must be cancel, idle, info, or an integer
    window.after(updateSpeed, update) #run update function after Xms, must be cancel, idle, info, or an integer

    
'''create menu bar'''
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Select Team", command=donothing)
filemenu.add_command(label="Select Delay Notification", command=donothing)
filemenu.add_command(label="Select Mode", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Setup Audio", command=donothing)
filemenu.add_command(label="Setup Light", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Close", command=donothing)
#filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="Setup", menu=filemenu)

utilsmenu = Menu(menubar, tearoff=0)
utilsmenu.add_command(label="Download Logos", command=donothing)
utilsmenu.add_command(label="Convert Logos to PNG", command=utilsImgtoPNG)
utilsmenu.add_separator()
utilsmenu.add_command(label="Play Media Player", command=utilsVideo)
utilsmenu.add_command(label="Stop Media Player", command=utilsVideoStop)
utilsmenu.add_command(label="Test Audio", command=utilsAudio)
utilsmenu.add_command(label="Test Light", command=donothing)
utilsmenu.add_command(label="Test All", command=donothing)
utilsmenu.add_separator()
utilsmenu.add_checkbutton(label="Enable debug mode", command=utilsMode) #add_checkbutton
menubar.add_cascade(label="Utils", menu=utilsmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

exitmenu = Menu(menubar, tearoff=0)
exitmenu.add_command(label="Exit", command=exit)
menubar.add_cascade(label="Exit", menu=exitmenu)
'''create menu bar'''

'''create label widgets'''
LabelSpareRow1 = Label(left_pane_frame, bg = bgcolor, text="")
LabelSpareRow2 = Label(left_pane_frame, bg = bgcolor, text="")
LabelSpareRow3 = Label(left_pane_frame, bg = bgcolor, text="")
LabelSpareRow4 = Label(left_pane_frame, bg = bgcolor, text="")
LabelHomeTeam = Label(left_pane_frame, bg = bgcolor, text="Home Team", font=("bold", 16), width=10)
LabelVS = Label(left_pane_frame, bg = bgcolor, text="vs", font=("bold", 24), width=2)
LabelAwayTeam = Label(left_pane_frame, bg = bgcolor, text="Away Team", font=("bold", 16), width=10)
LabelHomeName = Label(left_pane_frame, bg = bgcolor, text="name...", font=("bold", 16), width=18)
LabelAwayName = Label(left_pane_frame, bg = bgcolor, text="name...", font=("bold", 16), width=18)
LabelAwayScore = Label(left_pane_frame, bg = bgcolor, text="-", font=("bold", 80), width=5)
LabelHomeScore = Label(left_pane_frame, bg = bgcolor, text="-", font=("bold", 80), width=5)

LabelCityAway = Label(left_pane_frame, bg = bgcolor, text=" <-Location-> ")
LabelArenaAway = Label(left_pane_frame, bg = bgcolor, text=" <-Arena-> ")
LabelHistoryAway = Label(left_pane_frame, bg = bgcolor, text=" <-Franchise Year-> ")
LabelDivisionAway = Label(left_pane_frame, bg = bgcolor, text=" <-Division-> ")
LabelConferenceAway = Label(left_pane_frame, bg = bgcolor, text=" <-Conference-> ")
LabelRecordAway = Label(left_pane_frame, bg = bgcolor, text="<-W-L-OT->")
LabelGamesAway = Label(left_pane_frame, bg = bgcolor, text="<-GP, remaining->")

LabelAwayPic = Label(left_pane_frame, bg = bgcolor, image=away_logo)

LabelCityHome = Label(left_pane_frame, bg = bgcolor, text=" <-Location-> ")
LabelArenaHome = Label(left_pane_frame, bg = bgcolor, text=" <-Arena-> ")
LabelHistoryHome = Label(left_pane_frame, bg = bgcolor, text=" <-Franchise Year-> ")
LabelDivisionHome = Label(left_pane_frame, bg = bgcolor, text=" <-Division-> ")
LabelConferenceHome = Label(left_pane_frame, bg = bgcolor, text=" <-Conference-> ")
LabelRecordHome = Label(left_pane_frame, bg = bgcolor, text="<-W-L-OT->")
LabelGamesHome = Label(left_pane_frame, bg = bgcolor, text="<-GP, remaining->")

LabelHomePic = Label(left_pane_frame, bg = bgcolor, image=home_logo)

SepVert = ttk.Separator(left_pane_frame, orient='vertical')

LabelMediaText = Label(right_pane_frame, bg = bgcolor, text="Game Info | Status | Highlights", font=("bold", 16), width=25)
LabelDesc0 = Label(right_pane_frame, bg = bgcolor, text="", font=("normal", 10))
LabelDesc1 = Label(right_pane_frame, bg = bgcolor, text="previous game status...", font=("normal", 10))
LabelDesc2 = Label(right_pane_frame, bg = bgcolor, text="next game status", font=("normal", 10))
LabelDesc3 = Label(right_pane_frame, bg = bgcolor, text="desc3", font=("normal", 10))
LabelDesc4 = Label(right_pane_frame, bg = bgcolor, text="desc4", font=("normal", 10))
LabelDesc5 = Label(right_pane_frame, bg = bgcolor, text="desc5", font=("normal", 10))
LabelMedia = Label(right_pane_frame, bg = bgcolor, image=home_logo)

LabelPlayerPic = Label(right_pane_frame, bg = bgcolor, image=skater_default.image)

LabelPlayerDesc1 = Label(right_pane_frame, bg = bgcolor, font=("bold", 18))
LabelPlayerDesc2 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc3 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc4 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc5 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc6 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc7 = Label(right_pane_frame, bg = bgcolor)
LabelPlayerDesc8 = Label(right_pane_frame, bg = bgcolor)

#buttonStart = Button(window, text="Start", command=update)
buttonExit = Button(mainframe, bg = bgcolor, text="Exit", command=exit) #special command to exit & shutdown?
#buttonVerify = Button(window, text="Verify Team", command=setup) #special command to exit & shutdown?

'''LEFT define widget's grid layout'''
LabelSpareRow1.grid(row=0, column=0) #spare
LabelAwayTeam.grid(row=1, column=0)
LabelAwayName.grid(row=2, column=0)
LabelAwayScore.grid(row=3, column=0)
LabelAwayPic.grid(row=5, column=0)
LabelCityAway.grid(row=6, column=0)
LabelArenaAway.grid(row=7, column=0)
LabelHistoryAway.grid(row=8, column=0)
LabelDivisionAway.grid(row=9, column=0)
LabelConferenceAway.grid(row=10, column=0)
LabelRecordAway.grid(row=11, column=0)
LabelGamesAway.grid(row=12, column=0)

LabelVS.grid(row=2, column=1)

LabelHomeTeam.grid(row=1, column=2)
LabelHomeName.grid(row=2, column=2)
LabelHomeScore.grid(row=3, column=2)
LabelHomePic.grid(row=5, column=2)
LabelCityHome.grid(row=6, column=2)
LabelArenaHome.grid(row=7, column=2)
LabelHistoryHome.grid(row=8, column=2)
LabelDivisionHome.grid(row=9, column=2)
LabelConferenceHome.grid(row=10, column=2)
LabelRecordHome.grid(row=11, column=2)
LabelGamesHome.grid(row=12, column=2)

SepVert.grid(row=0, column=3, rowspan=12, sticky=NS)

LabelDesc0.grid(row=0, column=1, padx=1, sticky=W, columnspan=3)
LabelMediaText.grid(row=1, column=1, padx=0, sticky=EW, columnspan=3)
LabelDesc1.grid(row=2, column=1, padx=1, sticky=W, columnspan=3)
LabelDesc2.grid(row=3, column=1, padx=1, sticky=W, columnspan=3)
LabelDesc3.grid(row=16, column=1, padx=1, sticky=W, columnspan=3)
LabelDesc4.grid(row=17, column=1, padx=1, sticky=W, columnspan=3)
LabelDesc5.grid(row=18, column=1, padx=1, sticky=W, columnspan=3)
LabelMedia.grid(row=19, column=1, padx=1, rowspan=2, sticky=W, columnspan=3)

LabelPlayerPic.grid(row=4, column=1, sticky=NSEW, rowspan=11)

LabelPlayerDesc1.grid(row=4, column=2, padx=0, sticky=W)
LabelPlayerDesc2.grid(row=5, column=2, padx=0, sticky=W)
LabelPlayerDesc3.grid(row=6, column=2, padx=0, sticky=W)
LabelPlayerDesc4.grid(row=7, column=2, padx=0, sticky=W)
LabelPlayerDesc5.grid(row=8, column=2, padx=0, sticky=W)
LabelPlayerDesc6.grid(row=9, column=2, padx=0, sticky=W)
LabelPlayerDesc7.grid(row=10, column=2, padx=0, sticky=W)
LabelPlayerDesc8.grid(row=11, column=2, padx=0, sticky=W)


LabelSpareRow4.grid(row=17, column=0) #spare
'''define widget's grid layout'''

'''check for NHL.com check'''
update() #autostart, call update function which calls itself after XXXms

'''tkinter GUI update'''
window.config(menu=menubar)
window.mainloop()
