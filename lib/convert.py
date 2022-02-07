'''
pip3 install CairoSVG==2.5.2 for some reason pip3 install version 1.0.20 
'''
import os
import cairosvg

svg = '/home/pi/nhl_scoreboard/images/test/10.svg'
png = '/home/pi/nhl_scoreboard/images/test/10test.png'
dr = '/home/pi/nhl_scoreboard/images/'
#output_width= xxx, output_height=xxx, scale=2.0
#cairosvg.svg2png(url= svg, write_to= png, scale=2)
#cairosvg.svg2png(url= svg, write_to= png, parent_width=300, parent_height=450)

img_width = 200
img_height = int(img_width * 200/227) #keep ratio of 960x640\


for file in os.listdir(dr):
    #if os.path.isfile(file) and file.endswith(".svg"):
    if file.endswith(".svg"):
        name = file.split('.svg')[0]
        print(name)
        #cairosvg.svg2png(url='https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/1.svg',write_to=name+'/home/pi/nhl_scoreboard/images/y.png')
        cairosvg.svg2png(url=dr+name+'.svg',write_to=dr+name+'.png',parent_width=img_width, parent_height=img_height)
        #cairosvg.svg2png(url='https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/1.svg',write_to=png,parent_width=300, parent_height=450)
