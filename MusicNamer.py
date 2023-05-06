# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:20:55 2023

@author: baudo
"""

import eyed3
from os import listdir, rename
from os.path import join
import ytmusicapi as ytapi

DOWNLOAD_FOLDER = r"C:\Users\baudo\Downloads"


# album_cover_url = query['thumbnails'][0]['url']
# audio = eyed3.load(file_path)
# if (audio.tag.title == None) or (audio.tag.artist == None)or (audio.tag.album == None):
#     audio.tag.title  = query['title']
#     audio.tag.artist = query['artists'][0]['name']
#     audio.tag.album  = query['album']['name']
#     audio.tag.images.set(3,requests.get(album_cover_url).content, 'image/jpeg')
#     audio.tag.save(encoding='utf-8',version=eyed3.id3.ID3_V2_3)
# return audio

class Music:
    
    
    def __init__(self, path : str, attributes : dict) -> None :
        
        self.target_folder = r"C:\Users\baudo\Music"    
        self.attributes = attributes
        
    
    def relocate(self, file, title) -> None :
        
        rename(file, join(self.target_folder, title))

    

class MusicNamer:
    
    
    def __init__(self, default_folder : str = DOWNLOAD_FOLDER) -> None:
        
       self.folder = default_folder
       self.api    = ytapi.YTMusic()
       self.files = [join(self.folder, f + '.mp3') for f in self.listMP3Files()]
    
    
    @staticmethod
    def isMP3(filename : str) -> bool : return filename.endswith(".mp3")


    @staticmethod
    def cleanFilename(filename : str) -> str : 
        
        return filename.removesuffix(".mp3")
    
    
    @staticmethod
    def getMP3Duration(filename : str) -> float : 
        
        return eyed3.load(filename).info.time_secs
    
    
    def listMP3Files(self) -> list :
        
        return list(map(self.cleanFilename,
                   list(filter(self.isMP3, listdir(self.folder)))))
    
    
    def getMusicAttributes(self, musicName : str, attribute : str = None) -> dict :
        
        query = self.api.search(query=musicName,filter='songs',limit=1)
        if attribute is not None :
            try :
                query = [q[attribute] for q in query]
            except :
                raise AttributeError("Unknown attribute to the yt api query")
        return query

    
    def associateMusicToFile(self, musicname : str, filename : str) -> None :
        
        a_duration = self.getMP3Duration(filename)
        matches = self.getMusicAttributes(musicname, 'duration_seconds')
        best_match = matches.index(min(matches, \
                                          key = lambda n : abs(n - a_duration)))
        return self.getMusicAttributes(musicname)[best_match]    
        
    
    def renameFiles(self) -> None :
        
        for file in self.listMP3Files():
            music_path = join(self.folder, file + '.mp3')
            m = Music(music_path, self.associateMusicToFile(file, music_path))
        return m
    
    
    
if __name__ == "__main__":
    
    musicNamer = MusicNamer()
    # attr = musicNamer.associateMusicToFile("The Rock OST Compilation", join(musicNamer.folder, "The Rock OST Compilation.mp3"))
    m = musicNamer.renameFiles()



























