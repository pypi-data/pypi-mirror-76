#! Python
# (C) 2020 Novus Space

import os

''' Main class '''
class novusInit:
    def __init__(self):
        self.dependencies = 1
        self.directory = 'novusspace'
        self.checkDependencies()

    @staticmethod
    def checkDependencies():
        try:
            import shutil
            import requests
        except ImportError:
            exit('[ERROR] Missing module(s)')


''' Initialsation of novusspace module'''
novusInit()
