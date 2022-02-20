from tkinter import *
# Creating a GUI Windows

window_popup = Tk()

window_popup.title("Media Highlights")


# window size
window_width = 640
window_height = 360


# get the screen dimension
screen_width = window_popup.winfo_screenwidth()
screen_height = window_popup.winfo_screenheight()

# find the center point main window
offset_x = 350 #set to 0 to be center or XXX to shift over
offset_y = 0 #set to 0 to center or YYY to shift over
center_x = int((screen_width/2 - window_width/2) + offset_x)
center_y = int((screen_height/2 - window_height/2) + offset_y)
# find the center point popup window
window_popup_offset_x = 350 #set to 0 to be center or XXX to shift over
window_popup_offset_y = 30 #set to 0 to center or YYY to shift over
window_popup_center_x = int((screen_width/2 - window_width/2) + window_popup_offset_x)
window_popup_center_y = int((screen_height/2 - window_height/2) + window_popup_offset_y)

# set the position of the window to the center of the screen, window.geometry("800x600+200+200")
window_popup.geometry(f'{window_width}x{window_height}+{window_popup_center_x}+{window_popup_center_y}')

window_popup.attributes('-topmost', 1)


'''
guides and resources
tkinter
https://pythonguides.com/python-tkinter-label/

Gitub
https://github.com/199-cmd/ChangeImageInTkinter
https://github.com/arim215/nhl_goal_light
https://github.com/rpi-ws281x/rpi-ws281x-python #get led lights working
'''

''' video stuff '''
''' pip3 install tkvideo '''
from tkvideo import tkvideo


# create label
video_label = Label(window_popup)
video_label.pack()
# read video to display on label
video = "https://hlslive-wsczoominwestus.med.nhl.com/editor/bec9b46f-07af-4a7a-9c06-c5899da0843a.mp4"
video = "https://hlslive-wsczoominwestus.med.nhl.com/editor/dc6c3957-01cb-40a0-93e3-47247d1e1b5d.mp4" #FLASH_1200K_640X360" : 
#video = "https://hlslive-wsczoominwestus.med.nhl.com/editor/ab0160bf-aef0-44bb-8c5d-f79c16964ac0.mp4" #896x504
#video = "https://hlslive-wsczoominwestus.med.nhl.com/publish-hls/4326975/MasterTablet.m3u8"
player = tkvideo(video, video_label, loop = 1, size = (640, 360))
player.play()

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



'''tkinter GUI update'''
window_popup.mainloop()


