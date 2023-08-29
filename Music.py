# -*- coding: utf-8 -*-
"""
Created on Sun May  7 10:44:30 2023

@author: baudo
"""

from os import rename
from os.path import join
from requests import get
import eyed3

class Music:
    """
    Music object that tags an mp3 file with supposedly correct tags and
    then relocate it to the wanted folder
    """

    def __init__(self, path : str, target_folder : str, attributes : dict) -> None :
        """
        Parameters
        ----------
        path : str
            path to the mp3 file.
        attributes : dict
            the result of the ytmusicapi query. Contains music informations

        """

        self.attributes = attributes
        self.path = path
        self.target_folder = target_folder
        self.audio = eyed3.load(path)

        self.assignTags()
        self.relocate(path, self.attributes['title'])


    def relocate(self, file : str, title : str) -> None :
        """
        Relocate the current mp3 file to the Music folder

        Parameters
        ----------
        file : str
            path to the mp3 file.
        title : str
            The 'true' music title. Will be the new file name

        """

        rename(file, join(self.target_folder, title + '.mp3'))


    def assignTags(self) -> None :
        """
        Assign the title, album, cover, etc. tags to the mp3 file

        """

        self.audio.tag.title  = self.attributes['title']
        self.audio.tag.artist = self.attributes['artists'][0]['name']
        try:
            self.audio.tag.album  = self.attributes['album']['name']
            cover = self.attributes['thumbnails'][1]['url']
            self.audio.tag.images.set(3, get(cover, timeout = 3).content,\
                                  'image/jpeg')
        except (KeyError,IndexError):
            pass
        self.audio.tag.save(encoding='utf-8',version=eyed3.id3.ID3_V2_3)
