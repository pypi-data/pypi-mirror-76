#! Python
# 2020 Novus Space

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


novusInit()
