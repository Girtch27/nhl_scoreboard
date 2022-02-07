from tkinter import *
from tkinter import ttk

teamID = 26


def TestLogic1():
    global teamID
    home_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/10.png")
    LabelHomePic.configure(image=home_logo)
    LabelHomePic.image = home_logo
    teamID = 2

def TestLogic2():
    global teamID
    #tgImg = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/8.png")
    strID = str(teamID)
    home_logo = PhotoImage(file='/home/pi/nhl_scoreboard/images/PNG/' + strID + '.png')
    print('btn2 ' + '/home/pi/nhl_scoreboard/images/PNG/' + strID + '.png')
    LabelHomePic.configure(image=home_logo)
    LabelHomePic.image = home_logo
    if teamID == 8:
        teamID = 53
    else:
        teamID = 8
    window.after(1500, TestLogic2) #run update function after Xms, must be cancel, idle, info, or an integer

def NHL():
    global teamID
    home_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")
    #print('btn2 ' + '/home/pi/nhl_scoreboard/images/PNG/' + ID + '.png')
    LabelHomePic.configure(image=home_logo)
    LabelHomePic.image = home_logo
    teamID = 8

window = Tk()
 
window.geometry('1010x740+200+200')
  
home_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")
LabelHomePic=ttk.Label(window, image=home_logo)
LabelHomePic.place(x=400, y=400)

away_logo = PhotoImage(file="/home/pi/nhl_scoreboard/images/PNG/NHL.png")
LabelAwayPic=ttk.Label(window, image=away_logo)
LabelAwayPic.place(x=100, y=400)

testBtn1=ttk.Button(window, text="Image1", command=TestLogic1)
testBtn1.place(x=400, y=200)

testBtn2=ttk.Button(window, text="Image2", command=TestLogic2)
testBtn2.place(x=400, y=300)

testBtn3=ttk.Button(window, text="NHL", command=NHL)
testBtn3.place(x=400, y=400)

window.mainloop()