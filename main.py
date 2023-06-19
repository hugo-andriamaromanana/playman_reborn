from src.generator.tools.json_functions import *

from src.generator.scrapper import Scrapper
from src.generator.playlist import Playlist
from src.generator.song import Song
from src.user_creation import *
from src.generator.tools.format_data import clean_title
from src.generator.tools.pandas_functions import add_dic_to_items_csv

import sys


def main(username: str, channel_id: str):
    

    if channel_id == 'None':
        channel_id = get_channel_ID(username)

    if not user_exist(username):
        create_user_files(username, channel_id)
        print(f'User: "{username}" created successfully')
        save_channel_id(username, channel_id)


    existing_playlists = Scrapper(username).playlists
    
    for name in existing_playlists:
        
        data= Playlist(name, existing_playlists[name],username).playlist_items
        current_titles=Playlist(name, existing_playlists[name]).get_all_playlists_titles(name)
        
        for i in range(len(data)):
            for j in range(len(data[i]['items'])):
                
                title=clean_title(data[i]['items'][j]['snippet']['title']).strip()
                
                if title not in current_titles:
                    
                    add_dic_to_items_csv(Song(data[i]['items'][j]['snippet']['resourceId']['videoId'],title).return_song_data(),username)
                    print(f'New song added: {title}')
                    
                else:
                    print(f'Song already in playlist: {title}')


if __name__ == '__main__':
    # main(sys.argv[1], sys.argv[2])
    main('Hugo', 'None')