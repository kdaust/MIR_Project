import requests
import configparser
import json
import pandas as pd
from pandas import json_normalize 
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read user-modify-playback-state user-read-playback-state"

sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
        scope=scope,
        redirect_uri="https://thebeczone.ca/shiny/ccissdev/",
        client_id="3893dbdca69044e6aae96aaff3c25d68",
        client_secret="e953cb2d3b7f4e778cc4a5c8f458c9a1",
        show_dialog=True,
        cache_path="token.txt")
)
sp.devices()
songs = pd.read_csv('~/Desktop/MIR_Project/scripts/pop.csv')

songs1 = songs.loc[1:100]
songs2 = songs.loc[101:104]
sp.add_to_queue("spotify:track:6nYoTBmGFNgfTyRC8x1Fvp", device_id="9155b10b9e8e0ab14cd57066b747f2775ab0e9f4")
#Build Queue
for index, row in songs1.iterrows():
    print(row['id'])
    sp.add_to_queue(row['uri'], device_id='9155b10b9e8e0ab14cd57066b747f2775ab0e9f4')

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
