import requests
import configparser
import json
import pandas as pd
from pandas import json_normalize 
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-modify-playback-state user-read-playback-state"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
songs = pd.read_csv('jazz.csv')
print(sp.devices())

songs1 = songs.loc[1:100]
songs2 = songs.loc[101:104]

#Build Queue
for index, row in songs1.iterrows():
    print(row['id'])
    sp.add_to_queue(row['uri'], device_id='07e97f86521c36184d4142a4c8a1e53c044e51e1')

#start song
#sp.start_playback(device_id='07e97f86521c36184d4142a4c8a1e53c044e51e1')

#pause song
#sp.pause_playback(device_id='07e97f86521c36184d4142a4c8a1e53c044e51e1')

#next song
#next_track(device_id='07e97f86521c36184d4142a4c8a1e53c044e51e1')

#detect ad
#track = sp.currently_playing()
#if track.data.isAd == True:
    #skip
