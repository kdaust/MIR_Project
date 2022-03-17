import requests
import configparser

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
    return False
  print('Successfully authenticated.')
  return True


parser = configparser.ConfigParser()
parser.read("config.txt")

CLIENT_ID = parser.get("config", "client_id")
CLIENT_SECRET = parser.get("config", "client_secret")

authenticate(CLIENT_ID, CLIENT_SECRET)