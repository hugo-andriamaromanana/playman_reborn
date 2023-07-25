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

    scrapper= Scrapper(username)
    
    existing_playlists = scrapper.playlists
    
    for name in existing_playlists:
        
        current_playlist= Playlist(name, existing_playlists[name],username, scrapper.key)
        
        data= current_playlist.playlist_items
        current_titles=current_playlist.get_all_playlists_titles(existing_playlists[name])
        
        print('-------------------')
        print(f'Checking playlist: {name}')
        print(current_titles)
        print('-------------------')
        
        for i in range(len(data)):
            for j in range(len(data[i]['items'])):
                
                title=clean_title(data[i]['items'][j]['snippet']['title']).strip()
                
                song_url=data[i]['items'][j]['snippet']['resourceId']['videoId']
                
                if title not in current_titles:
                    
                    try:
                        song=Song(song_url,title)
                    except:
                        print(f'Error adding song: {title}')
                        continue
                    
                    song.add_playlist_ID_name(current_playlist.playlist_ID,current_playlist.playlist_name)
                    
                    add_dic_to_items_csv(song.return_song_data(),username)
                    print(f'New song added: {title}')
                    
                else:
                    continue


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
    # main('Hugo', 'None')