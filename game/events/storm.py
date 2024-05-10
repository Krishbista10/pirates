from game import event
from game.player import Player
from game.display import announce
from game.context import Context
import game.config as config
import random

class Storm(Context, event.Event):
    '''Encounter with a strong storm while sailing.'''

    def __init__(self):
        super().__init__()
        self.name = "Storm"
        self.verbs['brave'] = self
        self.verbs['wait'] = self
        self.verbs['wait'] = self
        self.verbs['take'] = self
        self.verbs['cover'] = self
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "brave":
            self.go = True
            self.result["message"] = "You decide to brave the storm and continue your journey."
        elif verb == "wait" or verb == "cover" or verb == "take":
            self.go = True
            self.result["message"] = "You decide to take cover and wait out the storm."
        elif verb == "help":
            self.go = False
            self.result["message"] = "You can either brave the storm and continue your journey or wait for the storm to pass."
        else:
            print("Invalid choice. Please choose 'brave', 'wait', or 'help'.")
            self.go = False

    def process(self, world):
        announce("An unexpected and strong storm hits the pirates as they were sailing the open oceans")
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "The sky is disguised by gloomy clouds, the waves dash against the hull, and the winds howl. The pirates face a decision: they can either brave the storm and continue their journey, or they can take cover and wait out the storm."
        while not self.go:
            Player.get_interaction([self])
        return self.result