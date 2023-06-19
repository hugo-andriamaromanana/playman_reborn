from src.generator.scrapper import Scrapper
import requests
from src.generator.tools.pandas_functions import get_csv
from src.generator.tools.json_functions import get_json
from os import path

class Playlist():
    
    def __init__(self, playlist_name: str, playlist_ID: str, current_user: str):
        
        self.current_user = Scrapper.current_user
            
        self.key = Scrapper.key
        
        self.playlist_name = playlist_name
        
        self.current_user = current_user
        
        self.playlist_ID = playlist_ID
        
        self.playlist_items = self.get_playlist_items()
        

    def get_playlist_items(self) -> list:
            
            url = "https://www.googleapis.com/youtube/v3/playlistItems"
            params = {
                'part': 'snippet',
                'playlistId': self.playlist_ID,
                'maxResults': 50,
                'key': self.key
            }
    
            response = requests.get(url, params=params).json()
            arr = []
            arr.append(response)
    
            while 'nextPageToken' in arr[-1].keys():
                params['pageToken'] = arr[-1]['nextPageToken']
                response = requests.get(url, params=params).json()
                arr.append(response)
            return arr

    def get_all_playlists_titles(self, playlist_name) -> list:
        df = get_csv(path.join(path.dirname(__file__), '..','..', 'docs', self.current_user, 'items.csv'))
        return list(df['title'].loc[df['playlist_name'] == playlist_name])

