import requests
import configparser
import json
import pandas as pd
from pandas import json_normalize 

def authenticate(CLIENT_ID, CLIENT_SECRET):
  AUTH_URL = 'https://accounts.spotify.com/api/token'
  auth_response = requests.post(AUTH_URL, {
      'grant_type': 'client_credentials',
      'client_id': CLIENT_ID,
      'client_secret': CLIENT_SECRET,
  })  
  resp = auth_response.json()
  
  if 'error' in resp.keys():
    print('Failed to authenticate.')
    return ''
  print('Successfully authenticated.')
  return resp['access_token']

def getSeedData(headers, genre, min_pop, max_pop):
  tracks=[]
  SEED_URL = 'https://api.spotify.com/v1/recommendations?limit=100&seed_genres=' + genre + '&min_popularity=' + min_pop + '&max_popularity=' + max_pop
  response = requests.get(SEED_URL, headers=headers)
  results = json.loads(response.text)
  x  = json_normalize(results['tracks'])
  return x



genres = ['country','pop', 'jazz']
parser = configparser.ConfigParser()
parser.read("config.txt")


CLIENT_ID = parser.get("config", "client_id")
CLIENT_SECRET = parser.get("config", "client_secret")

auth_token = 'Bearer ' + authenticate(CLIENT_ID, CLIENT_SECRET)
headers = {"Authorization": auth_token}

COLS = ['id', 'name', 'popularity', 'uri', 'href', 'artists']
for genre in genres:
  name = genre + '.csv'
  tracks=(getSeedData(headers, genre, '0','10'))
  tracks = tracks.append(getSeedData(headers, genre, '11','25'))
  tracks = tracks.append(getSeedData(headers, genre, '26','50'))
  tracks = tracks.append(getSeedData(headers, genre, '51','60'))
  tracks = tracks.append(getSeedData(headers, genre, '61','75'))
  tracks = tracks.append(getSeedData(headers, genre, '76','100'))
  tracks = tracks.drop(columns=['artists', 'available_markets', 'disc_number','duration_ms','explicit', 'is_local', 'preview_url','track_number','type', 'album.album_type','album.artists','album.available_markets','album.external_urls.spotify','album.href','album.id','album.images','album.release_date','album.release_date_precision','album.total_tracks','album.type','album.uri','external_ids.isrc','external_urls.spotify'])
  tracks.to_csv(name, index=False)

# url ='https://api.spotify.com/v1/recommendations/available-genre-seeds'
# response = requests.get(url, headers=headers)
