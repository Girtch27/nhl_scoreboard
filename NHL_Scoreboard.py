from tkinter import *
# Creating a GUI Window
window = Tk()
window.title("NHL Scoreboard") #gets changed below after Team to follow is determined
#set window color
bgcolorDefault = window.cget("background") #get default color to store to later change back too
window.configure(background=bgcolorDefault) #set back to default color

original_bgcolor = "light grey" #original_bgcolor is user selected color
original_bgcolor = "light blue" #original_bgcolor is user selected color
original_bgcolor = bgcolorDefault #original_bgcolor is user selected color

bgcolor = original_bgcolor #bgcolor used by all widgets
window['bg']= bgcolor

#size
windowWidth = 900
windowHeight = 600
windowXpos = 675
windowYpos = 40
SwindowWidth = str(windowWidth)
SwindowHeight = str(windowHeight)
SwindowXpos = str(windowXpos)
SwindowYpos = str(windowYpos)
windowSize = (SwindowWidth + "x" + SwindowHeight + "+" + SwindowXpos + "+" + SwindowYpos)
#window.geometry("800x600+200+200")
window.geometry(windowSize)

'''
guides and resources
tkinter
https://pythonguides.com/python-tkinter-label/

Gitub
https://github.com/199-cmd/ChangeImageInTkinter
https://github.com/arim215/nhl_goal_light
https://github.com/rpi-ws281x/rpi-ws281x-python #get led lights working
'''

'''image stuff'''
#from io import BytesIO
import cairosvg
from PIL import ImageTk, Image

''' OS parts '''
import os
import datetime
#import os #used to find config file and\or save status to file
import pause

'''my library NHL portion'''
from lib import nhl, alert

''' Initialize '''
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
gameday = False #gameday status
season = False #season
home_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")
away_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")

#myTeam is the team I want to follow

myTeam = "Rangers"
myTeam = "Panthers"
myTeam = "Flames"
myTeam = "Sharks"
myTeam = "Wild"
myTeam = "Golden Knights"
myTeam = "Canadiens"
myTeam = "Stars"
myTeam = "Maple Leafs"


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

    LabelCityHome["text"] = nhl.get_team_arena_city(home_team_ID)
    LabelArenaHome["text"] = nhl.get_team_arena_name(home_team_ID)
    LabelHistoryHome["text"] = 'Founded in ' + nhl.get_team_history(home_team_ID)
    LabelDivisionHome["text"] = nhl.get_team_division_info(home_team_ID) + ' Division'
    LabelConferenceHome["text"] = nhl.get_team_conference_info(home_team_ID) + ' Conference'
    LabelRecordHome["text"] = nhl.get_team_record_info(home_team_ID, nextGameDate)
    

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


    '''get info from NHL.com'''
    #print (game_status)
    team_id = nhl.get_team_id(myTeam)
    today = datetime.date.today()
    game_status = nhl.check_game_status(team_id,today) #send team_id and today's date, get back game status
        
    if (gameInfoUpdated is False): #update game info
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        logo(home_team_ID, away_team_ID) #home_logo , away_logo
        updateTeamInfo(nextGameDate)
        gameInfoUpdated = True #update game info flag
        print('Game info updated. ' +  ' Home:' + str(home_team) + str(home_team_ID) + ', Away: ' + str(away_team) + str(away_team_ID))
            
    if ('No Game' in game_status):
        #no game today, find next game info  
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        print(game_status + ' today, next game is: ' + str(home_team) + ' vs ' + str(away_team))
        updateSpeed = int(2*60*60*1000) # 2hours, delay as game hasn't started
        
        next_game_date_24hr, next_game_day, next_game_date_12hr  = nhl.get_next_game_date(team_id)
        today = datetime.date.today()
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
                
    elif ('Scheduled' in game_status):
        #game later today, find next game info
        home_team, home_team_ID, away_team, away_team_ID, nextGameDate = nhl.get_next_game_info2(team_id)
        print(game_status + ', game today: ' + str(home_team) + ' vs ' + str(away_team))
        updateSpeed = int(1*60*60*1000) # 1hours, delay as game hasn't started
        next_game_date_24hr, next_game_day, next_game_date_12hr  = nhl.get_next_game_date(team_id)
        today = datetime.date.today()
        LabelAwayName["text"] = away_team #was away_name
        LabelHomeName["text"] = home_team #was home_name
        LabelAwayScore["text"] = "-"
        LabelHomeScore["text"] = "-"
        if (team_id == away_team_ID):
            LabelDesc1["text"] = '{0} (away) vs {1} (home)'.format(away_team, home_team)
        else:
            LabelDesc1["text"] = '{0} (home) vs {1} (away)'.format(home_team, away_team)
        LabelDesc2["text"] = '{0} next game is TODAY! {1}'.format(myTeam, next_game_date_12hr)

    elif ('In Progress' in game_status) or ('Pre-Game' in game_status):
        new_score, home_score, away_score  = nhl.fetch_scores(team_id)
        
        if ('Pre-Game' in game_status):
            LabelAwayName["text"] = away_team
            LabelHomeName["text"] = home_team
            LabelAwayScore["text"] = "0"
            LabelHomeScore["text"] = "0"
            updateSpeed = int(10*60*1000) # 10min, delay as game hasn't started
            LabelDesc1["text"] = '{0} warmups, get ready!'.format(game_status)
            LabelDesc2["text"] = ""
            
        else:
            LabelAwayName["text"] = away_team
            LabelHomeName["text"] = home_team
            LabelDesc1["text"] = 'Game {0}!'.format(game_status)
            updateSpeed = int(1000) # 1sec, game on check often
            LabelDesc2["text"] = ""
            print(game_status + ':' + str(updateSpeed) + '. home:' + str(home_score) + ', away:' + str(away_score))
 
            '''Update GUI info'''
            LabelAwayScore["text"] = away_score
            LabelHomeScore["text"] = home_score
             
            '''Detect if score changed...'''
            if (home_score > old_home_score):
                LabelHomeScore["text"] = home_score
                if (team_id is home_team_ID):
                    LabelDesc2["text"] = "GOAL!"
                    old_home_score = home_score
                    pause.seconds(delay)
                    # update score
                    old_score = new_score
                    alert.activate_goal_audio()

            if (away_score > old_away_score):
                LabelAwayScore["text"] = away_score
                if (team_id is away_team_ID):
                    LabelDesc2["text"] = "GOAL!"
                    old_away_score = away_score
                    pause.seconds(delay)
                    # update score
                    old_score = new_score
                    alert.activate_goal_audio()

    elif ('Final' in game_status) or ('Game Over' in game_status):
        updateSpeed = int(30*60*1000) # 30mins
        #alert.cleanup()
        gameInfoUpdated = False #update game info flag
        print (game_status + ':' + str(updateSpeed) + ". Game ended, cleaning up!")
        
        #put something here for game ended, team won
        
        '''Update GUI info'''
        '''
        LabelAwayScore["text"] = away_score
        LabelHomeScore["text"] = home_score
        LabelAwayName["text"] = away_team
        LabelHomeName["text"] = home_team
        if (team_id == away_team_ID): #if myteam's ID is away team and they win or lost
            if (old_away_score > old_home_score):
                LabelDesc1["text"] = '{0} status is {1}. {0} won!'.format(myTeam, game_status)
                alert.activate_audio('Another One Bites The Dust')
            else:
                LabelDesc1["text"] = '{0} status is {1}. {0} lost!'.format(myTeam, game_status)
        elif (team_id == home_team_ID): #if myteam's ID is away team and they win or lost
            if (old_home_score > old_away_score):
                LabelDesc1["text"] = '{0} status is {1}. {0} won!!!'.format(myTeam, game_status)
                alert.activate_audio('Another One Bites The Dust')
            else:
                LabelDesc1["text"] = '{0} status is {1}. {0} lost!!!'.format(myTeam, game_status)
                print(str(old_home_score) + ',' + str(old_away_score))
        
        else:
            LabelDesc1["text"] = '{0} : {1}. {2} INVALID Result!'.format(myTeam, team_id, game_status)
        '''

            
        
        LabelDesc1["text"] = ""
        LabelDesc2["text"] = ""
    
    else:
        print(game_status + ':' + str(updateSpeed) + ". ***invalid state***")
        updateSpeed = int(2*60*60*1000) # 2hr
        
    
    # save the panel's image from 'garbage collection'
    # panel1.image = image1
    LabelHomePic.configure(image=home_logo)
    LabelAwayPic.configure(image=away_logo)
    LabelHomePic.image = home_logo
    LabelAwayPic.image = away_logo
    
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
LabelSpareRow1 = Label(window, bg = bgcolor, text="")
LabelSpareRow2 = Label(window, bg = bgcolor, text="")
LabelSpareRow3 = Label(window, bg = bgcolor, text="")
LabelSpareRow4 = Label(window, bg = bgcolor, text="")
LabelHomeTeam = Label(window, bg = bgcolor, text="Home Team", font=("bold", 16), width=20, padx=5)
LabelVS = Label(window, bg = bgcolor, text="vs", font=("bold", 24), width=10, padx=1)
LabelAwayTeam = Label(window, bg = bgcolor, text="Away Team", font=("bold", 16), width=20, padx=5)
#LabelAwayTeam = Label(window, bg = bgcolor, text="Away Team", font=("bold", 16), padx=30, pady=5)
LabelHomeName = Label(window, bg = bgcolor, text="name...", font=("bold", 16), width=22, padx=5)
LabelAwayName = Label(window, bg = bgcolor, text="name...", font=("bold", 16), width=22, padx=5)
LabelAwayScore = Label(window, bg = bgcolor, text="-", font=("bold", 80), width=5, padx=1)
LabelHomeScore = Label(window, bg = bgcolor, text="-", font=("bold", 80), width=5, padx=1)
LabelDesc1 = Label(window, bg = bgcolor, text="previous game status...", anchor="e")
LabelDesc2 = Label(window, bg = bgcolor, text="next game status", anchor="e")
#LabelDesc3 = Label(window, bg = bgcolor, text="description 33333", anchor="w")
LabelCityAway = Label(window, bg = bgcolor, text=" <-Location-> ")
LabelArenaAway = Label(window, bg = bgcolor, text=" <-Arena-> ")
LabelHistoryAway = Label(window, bg = bgcolor, text=" <-Franchise Year-> ")
LabelDivisionAway = Label(window, bg = bgcolor, text=" <-Division-> ")
LabelConferenceAway = Label(window, bg = bgcolor, text=" <-Conference-> ")
LabelRecordAway = Label(window, bg = bgcolor, text="<-W-L-OT->")
LabelAwayPic = Label(window, bg = bgcolor, image=away_logo)

LabelCityHome = Label(window, bg = bgcolor, text=" <-Location-> ")
LabelArenaHome = Label(window, bg = bgcolor, text=" <-Arena-> ")
LabelHistoryHome = Label(window, bg = bgcolor, text=" <-Franchise Year-> ")
LabelDivisionHome = Label(window, bg = bgcolor, text=" <-Division-> ")
LabelConferenceHome = Label(window, bg = bgcolor, text=" <-Conference-> ")
LabelRecordHome = Label(window, bg = bgcolor, text="<-W-L-OT->")
LabelHomePic = Label(window, bg = bgcolor, image=home_logo)

#buttonStart = Button(window, text="Start", command=update)
buttonExit = Button(window, bg = bgcolor, text="Exit", command=exit) #special command to exit & shutdown?
#buttonVerify = Button(window, text="Verify Team", command=setup) #special command to exit & shutdown?
'''create label widgets'''

'''define widget's grid layout'''
LabelSpareRow1.grid(row=0, column=0) #spare
LabelHomeTeam.grid(row=1, column=0)
LabelAwayTeam.grid(row=1, column=2)
LabelHomeName.grid(row=2, column=0)
LabelVS.grid(row=2, column=1)
LabelAwayName.grid(row=2, column=2)
LabelAwayScore.grid(row=3, column=2)
LabelHomeScore.grid(row=3, column=0)
#LabelSpareRow2.grid(row=4, column=0) #spare
#LabelDesc2.grid(row=6, column=0, columnspan=2)
#LabelDesc3.grid(row=7, column=0, columnspan=2)
#LabelSpareRow3.grid(row=8, column=0) #spare

#buttonVerify.grid(row=9, column=1)
LabelDesc1.grid(row=10, column=0, columnspan=3)
LabelDesc2.grid(row=11, column=0, columnspan=3)
LabelHomePic.grid(row=12, column=0, rowspan=5)
LabelAwayPic.grid(row=12, column=2, rowspan=5)

LabelCityHome.grid(row=18, column=0)
LabelArenaHome.grid(row=19, column=0)
LabelHistoryHome.grid(row=20, column=0)
LabelDivisionHome.grid(row=21, column=0)
LabelConferenceHome.grid(row=22, column=0)
LabelRecordHome.grid(row=23, column=0)

LabelCityAway.grid(row=18, column=2)
LabelArenaAway.grid(row=19, column=2)
LabelHistoryAway.grid(row=20, column=2)
LabelDivisionAway.grid(row=21, column=2)
LabelConferenceAway.grid(row=22, column=2)
LabelRecordAway.grid(row=23, column=2)

#buttonStart.grid(row=24, column=0)
#buttonExit.grid(row=24, column=3)

LabelSpareRow4.grid(row=17, column=0) #spare
'''define widget's grid layout'''

'''check for NHL.com check'''
update() #autostart, call update function which calls itself after XXXms

'''tkinter GUI update'''
window.config(menu=menubar)
window.mainloop()