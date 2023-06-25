from src.generator.tools.format_data import format_time, format_date, string_to_arr, remove_tags
from src.generator.tools.format_data import *
import requests

class Song():

    def __init__(self, url: str, title: str):
        
        self.key = get_json(path.join(path.dirname(
            __file__), '..', 'settings', 'params.json'))['key']
        
        self.url = url
        self.title = title
        
        self.metadata = self.more_metadata(url)
        
        self.publishedAt = self.metadata['publishedAt']
        self.duration = self.metadata['duration']
        self.topic_categories = self.metadata['topic_categories']
        self.view_count = self.metadata['view_count']
        self.like_count = self.metadata['like_count']
        self.comment_count = self.metadata['comment_count']
        self.tags = self.metadata['tags']
        self.channel_title = self.metadata['channel_title']
        self.channel_ID = self.metadata['channel_ID']

    
    def more_metadata(self, url: str) -> dict:

        url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,topicDetails,statistics&id={url}&key={self.key}'
        response = requests.get(url).json()
        meta_data = {}

        meta_data['duration'] = response['items'][0]['contentDetails'].get('duration', 'NaN')
        meta_data['publishedAt'] = response['items'][0]['snippet'].get('publishedAt', 'NaN')
        meta_data['topic_categories'] = response['items'][0]['topicDetails'].get('topicCategories', 'NaN')
        meta_data['view_count'] = response['items'][0]['statistics'].get('viewCount', 'NaN')
        meta_data['like_count'] = response['items'][0]['statistics'].get('likeCount', 'NaN')
        meta_data['comment_count'] = response['items'][0]['statistics'].get('commentCount', 'NaN')
        meta_data['tags'] = response['items'][0]['snippet'].get('tags', 'NaN')
        meta_data['channel_title'] = response['items'][0]['snippet'].get('channelTitle', 'NaN')
        meta_data['channel_ID'] = response['items'][0]['snippet'].get('channelId', 'NaN')
        
        return meta_data
    
    
    def add_playlist_ID_name(self, playlist_ID: str, playlist_name: str) -> None:
        self.playlist_ID = playlist_ID
        self.playlist_name = playlist_name
        return None
    
    def return_song_data(self) -> dict[str,str]:
        return {
            'title': self.title,
            'publishedAt': format_date(self.publishedAt),
            'duration': format_time(self.duration),
            'topic_categories': str(remove_tags(string_to_arr(self.topic_categories))),
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'tags': self.tags,
            'channel_title': self.channel_title,
            'playlist_name': self.title,
            'channel_ID': self.channel_ID,
            'playlist_ID': self.playlist_ID,
            'url': self.url
        }
