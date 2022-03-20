import requests
import json

NHL_API_PLAYER_URL = "http://statsapi.web.nhl.com/api/v1/people/"
# format for Marner is http://statsapi.web.nhl.com/api/v1/people/8478483

NHL_PLAYER_PIC_URL = "https://cms.nhl.bamgrid.com/images/headshots/current/168x168/" 
# format for Marner is https://cms.nhl.bamgrid.com/images/headshots/current/168x168/8478483.jpg

#response = requests.get(NHL_API_URL + ID).json()
#print('player url: ' + NHL_API_PLAYER_URL)

class NHLPlayer:

    def __init__(self, ID):
        NHL_PLAYER_PIC_URL = NHL_PLAYER_PIC_URL = "https://cms.nhl.bamgrid.com/images/headshots/current/168x168/"
        NHL_PLAYER_PIC_URL = NHL_PLAYER_PIC_URL + ID + ".jpg"

        NHL_API_PLAYER_URL = "http://statsapi.web.nhl.com/api/v1/people/"
        NHL_API_PLAYER_URL = NHL_API_PLAYER_URL + ID

        response = requests.get(NHL_API_PLAYER_URL).json()

        self.firstname = response['people'][0]['firstName']
        self.lastname = response['people'][0]['lastName']
        self.fullname = response['people'][0]['fullName']
        self.number = response['people'][0]['primaryNumber']
        self.birthday = response['people'][0]['birthDate']
        self.age = response['people'][0]['currentAge']
        self.nationality = response['people'][0]['nationality']
        self.hand = response['people'][0]['shootsCatches']
        self.position = response['people'][0]['primaryPosition']['abbreviation']
        self.size = str(response['people'][0]['height']) + ', ' + str(response['people'][0]['weight']) + 'lbs'
        self.headpic_url = NHL_PLAYER_PIC_URL

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname 
    
    def get_fullname(self):
        return self.fullname
    
    def get_number(self):
        return self.number
            
    def get_birthday(self):
        return self.birthday
            
    def get_age(self):
        return self.age
            
    def get_nationality(self):
        return self.nationality
            
    def get_hand(self):
        return self.hand

    def get_position(self):
        return self.position
            
    def get_size(self):
        return self.size
    
    def get_headpic_url(self):
        return self.headpic_url
    
''' test
player = NHLPlayer("8478483")
print(player.firstname)
print(player.lastname)
print(player.fullname)
print(player.number)
print(player.birthday)
print(player.age)
print(player.nationality)
print(player.hand)
print(player.size)
'''




