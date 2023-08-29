# -*- coding: utf-8 -*-
"""
Created on Sun May  7 11:07:46 2023

@author: baudo
"""

from MusicNamer import MusicNamer
from gui import GUI
from PyQt5.QtWidgets import QApplication
import sys 


if __name__ == "__main__":

    app = QApplication([])
    screen = GUI()
    screen.show()
    sys.exit(app.exec_())

    # parser = argparse.ArgumentParser(
    #     prog="ytToMP3",
    #     description="Add album, artist, etc. to the mp3 files in a folder and move them in another one",
    # )
    # parser.add_argument("-f", "--path_to_folder", type=str, required=True)
    # parser.add_argument("-t", "--path_to_target", type=str, required=True)
    # args = parser.parse_args()
    # musicNamer = MusicNamer(target_path=args.path_to_target, folder=args.path_to_folder)
    musicNamer = MusicNamer(target_path="/home/bbosc/Downloads/", folder="/home/bbosc/Downloads/")
    musicNamer.renameFiles()
