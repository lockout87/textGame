#!/usr/bin/python

class ROOM():
    def __init__(self):
        self.exits       = {}
        self.description = ''

#	def __init__(self, exits, description='This room is too dark to describe. So so sad.'):
#		assert isinstance(exits, dict), "Exits should be a dict"
#		self.exits = exits
#		self.description = description

    def getExits(self):
        output = ''
        for exit in self.exits:
            output += exit + ', '
        output = output[:-2]
        return output

    def getDescription(self):
        return self.description

    def setExits(self, exits):
        assert isinstance(exits, dict), "Exits should be a dict"
        self.exits = exits

    def setDescription(self, description):
        self.description = description

    def addToExits(self, addExits):
        for key, value in addExits.iteritems():
            self.exits[key] = value

class INTERFACE():
    def __init__(self):
        self.allRooms       = self.roomSetup()
        self.currentRoom    = self.allRooms['Door Step']
        self.commands       = {"go"   : self.go,
                               "help" : self.help}

    def roomSetup(self):
        doorStep = ROOM()
        entry	 = ROOM()
        rooms    = {
                    'Door Step' :   doorStep,
                    'Entry'     :   entry,
                   }

        doorStep.setExits({"Entry": entry})
        doorStep.setDescription("You are on the doorstep of a terribly dark and evil fortress. "
                                "Inside is the princess. As a Knight of the Order - you are tasked"
                                " with saving her. Unfortunately, your training was cut short, as "
                                "the other Knights were busy at the time. Good Luck, and may the "
                                "Force be with you.")

        entry.setExits({"Door Step":doorStep})
        entry.setDescription("You have entered the building. "
                             "Beware of Everything, for you "
                             "are no longer safe.")

        return rooms

    def displayRoom(self):#, room=self.currentRoom):
        assert isinstance(self.currentRoom, ROOM), "Shit ain't a room bitch"
        print self.currentRoom.getDescription()
        print "Available exits are:"
        print self.currentRoom.getExits()

    def waitForAction(self):
        text = raw_input("What would you like to do?")
        for key, value in self.commands.iteritems():
            if text.startswith(key):
                self.commands[key](text)

    def go(self, text):
        text.strip('go ')
        for key, value in self.allRooms.iteritems():
            if text.startswith(key):
                self.currentRoom = value

    def help(self, text):
        print "helping"


interface = INTERFACE()

while True:
    interface.displayRoom()
    interface.waitForAction()
