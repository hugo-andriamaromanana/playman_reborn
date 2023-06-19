import requests
from os import path

from src.generator.tools.json_functions import *
from src.generator.tools.pandas_functions import *


class Scrapper():

    def __init__(self, current_user: str):

        self.key = get_json(path.join(path.dirname(
            __file__), '..', 'settings', 'params.json'))['key']
        
        self.current_user = current_user

        self.channel_ID = get_json(path.join(path.dirname(
            __file__), '..', 'settings', 'users.json'))[current_user]['channel_id']
        
        self.playlists = self.get_playlist_ID_dic()

    def get_playlist_ID_dic(self) -> dict:

        url = "https://www.googleapis.com/youtube/v3/playlists"
        params = {
            'part': 'snippet',
            'channelId': self.channel_ID,
            'maxResults': 50,
            'key': self.key
        }
        response = requests.get(url, params=params).json()

        dic = {}

        for i in range(len(response['items'])):
            dic[response['items'][i]['snippet']['title']] = response['items'][i]['id']

        while 'nextPageToken' in response.keys():
            params['pageToken'] = response['nextPageToken']
            response = requests.get(url, params=params).json()

            for i in range(len(response['items'])):
                dic[response['items'][i]['snippet']
                    ['title']] = response['items'][i]['id']
        return dic
