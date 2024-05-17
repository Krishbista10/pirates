from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import math
from game.items import Item
from game.events.storm import Storm
import random
import game.combat as combat


class Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "island"
        self.symbol = 'K'
        self.visitable = True
        self.starting_location = Village(self)
        self.locations = {}
        self.locations["village"] = self.starting_location
        self.locations["cove"] = Cove(self)
        self.locations["jungle"] = Jungle(self)
        self.locations["graveyard"] = Graveyard(self)
        self.locations["goldmine"] = Goldmine(self)

    def enter (self, ship):
        print ("Welcome! You arrived in Kathmandu island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Village(location.SubLocation):  
    def __init__ (self, m):
        super().__init__(m)
        self.name = "village"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())
        self.events.append(drowned_pirates.DrownedPirates())
    

    def enter (self):
        announce ("You arrived at the village.")
        announce("There's a mysterious box at the centre of the village")
        announce("Inside the box you find a map. This helps you to get other locations within the island.")
        announce("The map says,if you go east you'll reach cove.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["cove"]
        elif (verb == "north" or verb == "west"):
            announce ("You walk all the way around the island within the village. It's not very interesting.")

class Cove(location.SubLocation):
    def __init__(self, main_location):
        super().__init__(main_location)
        self.name = "cove"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['solve'] = self  
        self.event_chance = 50
        self.events.append(Storm())

    def enter(self):
        announce("You arrive at the cove. If you type solve there's a riddle for you upon solving which you get food.")

    def solve_riddle(self):
        print("In the heart of the cove, a riddle lies,")
        print("Answer it right, and you'll claim your prize.")
        print("What has a face and two hands, but can't smile or clap?")

        answer = input("> ").lower()

        while answer != "clock":
            print("Incorrect. Try again.")
            answer = input("> ").lower()
        self.food

    print("Well done! You've solved the jungle's riddle.")
    print("Your reward is a step closer to your goal.")



    def process_verb(self, verb, cmd_list, nouns):
        if verb in self.verbs:
            if verb == "solve":
                self.solve_riddle()
            elif verb == "west":
                announce("You return to the village.")
                config.the_player.next_loc = self.main_location.locations["village"]
            elif verb == "north":
                config.the_player.next_loc = self.main_location.locations["jungle"]
            elif verb == "south" or verb == "east":
                announce("You walk all the way around the cove. It's not very interesting.")
        else:
            announce("You can't do that here.")


class Jungle(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "jungle"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['heal'] = self

    def enter(self):
        announce("Arrived at the jungle. You find a  magical herb that heals wounds and helps you recover.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You return to cove.")
            config.the_player.next_loc = self.main_location.locations["cove"]
        elif verb == "west":
            config.the_player.next_loc = self.main_location.locations["graveyard"]
        elif verb == "north" or verb == "east":
            announce("You walk all the way around the jungle. It's not very interesting.")
        elif verb == "heal":
            for i in config.the_player.get_pirates():
                i.health = 100
                print(i)
            print("Now your wounds are healed.")
                    

class Graveyard(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "ruins"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self

    def enter(self):
        announce("You arrived at the graveyard.")
        monsters = []
        monsters.append(KMonster("K Monster I"))
        monsters.append(KMonster("K Monster II"))
        announce("You are attacked by monsters")
        combat.Combat(monsters).combat()
        


    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            announce("You reach goldmine.")
            config.the_player.next_loc = self.main_location.locations["goldmine"]
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["graveyard"]
        elif verb == "north" or verb == "south":
            announce("You walk all the way around the graveyard. It's not very interesting.")



class Goldmine(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "goldmine"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['solve'] = self
        self.riddle_question = (
            "In the depths of the goldmine, a puzzle awaits,\n"
            "Solve it with your wit, and claim your golden bait.\n"
            "Three numbers, in a sequence they stand,\n"
            "Each one divided by 3, leaving a different remainder at hand.\n"
            "The first leaves 1, the second leaves 2,\n"
            "What is the third number, the riddle's final clue?"
        )

    def enter(self):
        announce(" You arrived at the goldmine. You have to solve a riddle to get the treasure.")

        
    def treasure_chest(self):
        for pirate in config.the_player.get_pirates():
            treasure_chest = items.TreasureChest()
            pirate.items.append(treasure_chest)
            announce(f"{pirate.name} obtained a {treasure_chest.name}!")

    def solve_riddle(self):
        print(self.riddle_question)

        answer = input("> ")

        while int(answer) % 3 != 0:
            print("Incorrect. Try again.")
            answer = input("> ")

        print("Well done! You've solved the goldmine's riddle.")
        self.treasure_chest
        print("The treasure is now yours, a reward for your wit and will.")
        # Add code to reward the player with treasure or other items

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            announce("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif verb == "east":
            config.the_player.next_loc = self.main_location.locations["graveyard"]
        elif verb == "north" or verb == "west":
            announce("You walk all the way around the cave on the beach. It's not very interesting.")
        elif verb == "solve":
            self.solve_riddle()

        

class KMonster(combat.Monster):
    def __init__(self,name):
        attacks = {}
        attacks["bite"] = ["bites",random.randrange(70,101), (10,20)]
        attacks["attack with claws"] = ["attck with",random.randrange(35,51), (1,10)]
        super().__init__(name, random.randrange(7,20), attacks, 180 + random.randrange(-20,21))