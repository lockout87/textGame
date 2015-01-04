#!/usr/bin/python
import sys, os, termios, fcntl

def waitForKeyPress():
    try:
        raw_input("Please press enter to continue...")
    except IOError:
        pass

class OBJECT():
    def __init__(self, name, description, destroyedDescription = "", hasHP = False):
        assert isinstance(hasHP, bool), "hasHP needs to be True or False"
        self.hasHP = hasHP
        self.name   = name
        self.setDescription(description)
        self.destroyedDescription = ''

    def setDescription(self, text):
        text.replace('\n', ' ')
        for x in range(0, len(text)):
            if x % 80 == 0:
                text = text[:x] + '\n' + text[x:]
        self.description = text

    def setDestroyed(self):
        self.hasHP = False
        self.setDescription(self.destroyedDescription)

class ROOM():
    def __init__(self):
        self.exits       = {}
        self.description = ''
        self.objects     = {}

#	def __init__(self, exits, description='This room is too dark to describe. So so sad.'):
#		assert isinstance(exits, dict), "Exits should be a dict"
#		self.exits = exits
#		self.description = description

    def getExits(self):
        output = ''
        for key in self.exits.viewkeys():
            output = output + key + ', '
        output = output[:-2]
        return output

    def getDescription(self):
        return self.description

    def setExits(self, roomsDict, exitsList):
        assert isinstance(roomsDict, dict), "roomsDict should be a dict"
        assert isinstance(exitsList, list), "Exits should be a list"
        self.exits = {key : roomsDict[key] for key in exitsList}

    def setDescription(self, text):
        temp = text.split()
        text = " ".join(temp)
        for x in range(0, len(text)):
            if x % 120 == 0:
                text = text[:x] + '\n' + text[x:]
        self.description = text

    def addToExits(self, addExits):
        for key, value in addExits.iteritems():
            self.exits[key] = value

    def addObject(self, objects):
        for key, value in objects.iteritems():
            self.objects[key] = value

class ROOMSETUP():
    def __init__(self):
        self.roomList = ["Door Step",
                         "Entry",
                         "First Bed",
                         "First Bath",
                         "Garage",
                         "First Stair",
                         "Landing",
                         "Second Bath",
                         "Kitchen",
                         "Gaming Area",
                         "Living Room",
                         "Second Landing",
                         "Second Bed",
                         "Guest Bed"
                         ]
        self.allRooms = self.roomBuilder()

    def roomBuilder(self):
        doorStep    = ROOM()
        entry       = ROOM()
        firstBed    = ROOM()
        firstBath   = ROOM()
        garage      = ROOM()
        firstStair  = ROOM()
        landing     = ROOM()
        secondBath  = ROOM()
        kitchen     = ROOM()
        gamingArea  = ROOM()
        livingRoom  = ROOM()
        secondStair = ROOM()
        secondLand  = ROOM()
        secondBed   = ROOM()
        guestBed    = ROOM()
        rooms    = {
                    'Door Step'     :   doorStep,
                    'Entry'         :   entry,
                    'First Bed'     :   firstBed,
                    'First Bath'    :   firstBath,
                    'Garage'        :   garage,
                    'First Stair'   :   firstStair,
                    'Landing'       :   landing,
                    'Second Bath'   :   secondBath,
                    'Kitchen'       :   kitchen,
                    'Gaming Area'   :   gamingArea,
                    'Living Room'   :   livingRoom,
                    'Second Stair'  :   secondStair,
                    'Second Landing':   secondLand,
                    'Second Bed'    :   secondBed,
                    'Guest Bed'     :   guestBed
                   }
        doorStepExits = ["Entry"]
        doorStep.setExits(rooms, doorStepExits)
        doorStep.setDescription("You are on the doorstep of a terribly dark and evil fortress.\n"
                                "Inside is the princess. As a Knight of the Order - you are tasked\n"
                                "with her safety. Unfortunately, your training was cut short, as\n"
                                "the other Knights were busy at the time. Good Luck, and may the\n"
                                "Force be with you or some shit.\n")

        entryExits = ['Door Step',
                      'First Bed',
                      'First Bath',
                      'Garage',
                      ]
        entry.setExits(rooms, entryExits)
        entry.setDescription("You have entered the building. Beware of Everything, for you\n"
                             "are no longer safe."
                            )

        firstBedExits = ['Entry']
        firstBed.setExits(rooms, firstBedExits)
        firstBed.setDescription("This room is poopy.")
        return rooms

class COMMANDS():
    def __init__(self):
        self.commands       = {"go"     : self.go,
                               "attack" : self.attack,
                               "lift"   : self.lift,
                               "open"   : self.open,
                               "help"   : self.help,
                               }

    def go(self, text, state):
        """
        Is used to enter a room.
        For instance "go Entry"
        """
        text = text.replace('go ', '', 1)
        print text
        for key, value in state.currentRoom.exits.iteritems():
            if text.startswith(key.lower()):
                state.changeCurrentRoom(value)

    def help(self, text, state):
        """
        Displays the commands.
        """
        print "You have the following options:"
        for key, value in self.commands.iteritems():
            print key
            print self.commands[key].__doc__

    def attack(self, text, state):
        """
        Allows you to attack something.
        """
        text = text.replace('attack ', '', 1)
        for key, value in state.currentRoom.objects.iteritems():
            if text.startswith(key.lower()):
                if value.hasHP():
                    print "You attack the {0} with your {1}.".format(key, state.player.currentWeapon)
                else:
                    print "You cannot attack the {0}".format(key)

    def lift(self, text, state):
        """
        Allows you to lift something.
        """
        text = text.replace('lift', '', 1)
        for key, value in state.currentRoom.objects.iteritems():
            if text.startswith(key.lower()):
                if value.liftAble():
                    print "You lift the {0}.".format(key)
            else:
                print "You cannot lift the {0}."

    def open(self, text, state):
        """
        Allows you to lift something.
        """
        text = text.replace('lift', '', 1)
        for key, value in state.currentRoom.objects.iteritems():
            if text.startswith(key.lower()):
                if value.liftAble():
                    print "You lift the {0}.".format(key)
                else:
                    print "You cannot lift the {0}.".format(key)

class STATE():
    def __init__(self, currentRoom, player):
        self.currentRoom    =   currentRoom
        self.player         =   player

    def changeCurrentRoom(self, newRoom):
        self.currentRoom = newRoom


class PLAYER():
    def __init__(self):
        self.weapon     = OBJECT("Fists", "You ball your hands into fists. Not the greatest weapon, but it'll have to do")
        self.inventory  =   []

    def addInventory(self, item):
        assert isinstance(item, OBJECT), "Can't put non-objects in your backpack"
        self.inventory.append(item)

    def setWeapon(self, item):
        assert isinstance(item, OBJECT), "Must equip object as items."
        self.inventory.append(self.weapon)
        if item in self.inventory:
            self.inventory.remove(item)
        self.weapon = item

class INTERFACE():
    def __init__(self):
        self.roomSetup      = ROOMSETUP()
        self.allRooms       = self.roomSetup.allRooms
        self.currentState   = STATE(self.allRooms["Door Step"], PLAYER())
        self.commands       = COMMANDS().commands


    def displayRoom(self):
        assert isinstance(self.currentState.currentRoom, ROOM), "Shit ain't a room bitch"
        print self.currentState.currentRoom.getDescription()
        print "Available exits are:"
        print self.currentState.currentRoom.getExits()

    def waitForAction(self):
        text = raw_input("What would you like to do?")
        text = text.lower()
        for key, value in self.commands.iteritems():
            if text.startswith(key.lower()):
                self.commands[key](text, self.currentState)



interface = INTERFACE()

while True:
    interface.displayRoom()
    interface.waitForAction()
