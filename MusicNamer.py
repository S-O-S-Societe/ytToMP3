# -*- coding: utf-8 -*-
"""
Created on Sat May  6 19:20:55 2023

@author: baudo
"""

from os import listdir
from os.path import join
import ytmusicapi as ytapi
from tqdm import tqdm
from mutagen.mp3 import MP3
from Music import Music

DOWNLOAD_FOLDER = r"C:\Users\baudo\Downloads"



class MusicNamer:
    """This object manages the mp3 in a folder and search for a matching music
        in youtube music
    """

    def __init__(self, target_path : str = DOWNLOAD_FOLDER, folder : str = DOWNLOAD_FOLDER) -> None:
        """
        Object initializer

        Parameters
        ----------
        default_folder : str, optional
            The folder where you want to pick the untagged mp3 files.
            The default is DOWNLOAD_FOLDER.

        """
        self.folder = folder
        self.target_path = target_path
        self.api    = ytapi.YTMusic()
        self.processing_state = 0


    @staticmethod
    def isMP3(filename : str) -> bool :
        """
        Checks if a file is an mp3 file

        Parameters
        ----------
        filename : str
            path to the mp3 file.

        Returns
        -------
        bool
            True if the file is mp3, False otherwise.

        """

        return filename.endswith(".mp3")

    @staticmethod
    def remove_suffix(input_string, suffix):
        if suffix and input_string.endswith(suffix):
            return input_string[:-len(suffix)]
        return input_string

    def cleanFilename(self, filename : str) -> str :
        """
        Remove unecessary file extension and characters before using it for search

        Parameters
        ----------
        filename : str
            path to the mp3 file.

        Returns
        -------
        str
            The cleaned filename.

        """

        return self.remove_suffix(filename,".mp3")


    @staticmethod
    def getMP3Duration(filename : str) -> float :
        """

        Parameters
        ----------
        filename : str
            path to the mp3 file.

        Returns
        -------
        float
            The duration of the mp3 file in seconds.

        """

        # return eyed3.load(filename).info.time_secs
        return MP3(filename).info.length


    def listMP3Files(self) -> list :
        """

        Returns
        -------
        list
            List of cleaned music names in the folder, without the whole path.

        """
        clean_mp3 = list(map(self.cleanFilename,
                   list(filter(self.isMP3, listdir(self.folder)))))
        self.files = [join(self.folder, f + '.mp3') for f in clean_mp3]


    def getMusicAttributes(self, musicName : str, search_key : str = None, attribute : str = None) -> list :
        """

        Parameters
        ----------
        musicName : str
            name of the music.
        attribute : str, optional
            If specified, will return only this attribute for all of the proposals.
            The default is None.

        Raises
        ------
        AttributeError
            Raised if a unknown attribute was entered.

        Returns
        -------
        list(dict)
            The attributes of each possible matches as a list of dict.

        """
        query = self.api.search(query=musicName,limit=10)
        if (attribute is not None) and (search_key is not None) :
            return [qu[attribute] for qu in list(filter(lambda q : attribute in list(q.keys()), query))]
        elif (attribute is not None) and (search_key is None):
            return [qu for qu in list(filter(lambda q : attribute in list(q.keys()), query))]
        return query


    def associateMusicToFile(self, musicname : str, filename : str) -> dict :
        """
        For a single mp3 file and its associated name, find the best match based
        on duration equality in the matches found by the ytmusic api

        Parameters
        ----------
        musicname : str
            The name of your mp3 file.
        filename : str
            The path to your mp3 file.

        Returns
        -------
        dict
            The attributes of the best match found.

        """

        a_duration = self.getMP3Duration(filename)
        matches = self.getMusicAttributes(musicname, 'duration_seconds', 'duration_seconds')
        best_match = matches.index(min(matches, \
                                          key = lambda n : abs(n - a_duration)))
        print(f"""matching duration : {min(a_duration, matches[best_match])
              /max(a_duration, matches[best_match]) * 100 :.2f} %""")
        return self.getMusicAttributes(musicname, attribute="duration_seconds")[best_match]


    def renameFiles(self) -> None :
        """
        Loops over all the mp3 files in the source folder, and make a Music
        object out of the best match found in ytmusic api


        """

        for file in tqdm(self.files):
            music_path = join(self.folder, file)
            Music(music_path, self.target_path, self.associateMusicToFile(file, music_path))
            self.processing_state += 1
