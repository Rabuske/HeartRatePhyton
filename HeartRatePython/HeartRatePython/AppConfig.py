import json

# Singleton metaclass to read the configuration file
class AppConfigSingleton(object):
    _instance = None
    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_)
        return class_._instance

class AppConfig(AppConfigSingleton):
    confData = None

    def __init__(self, fileName = None):
        if (fileName == None and self.confData == None):
            self.load("config.json")
            return
        if fileName != None:
            self.load(fileName)
            return

    def load(self, fileName):
        self.confData = json.load(open(fileName))
            
    def get(self, config):
        return self.confData[config]