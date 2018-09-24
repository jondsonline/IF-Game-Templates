from ifclasses import *


# this class defined here to keep pertinent game info in data file
class Flags():
    def __init__(self):
        self.flag_one = False
        self.flag_two = False
        self.flag_three = False

# initialize flags
flag = Flags()

# ------
# ITEMS
# ------

# A book, a standard item
book = Item('book')
book.title = 'A Python textbook'
book.desc = "An interesting Python textbook to study from."

# A ghost, an "item" not listed in room inventory, or takeable
ghost = Item('ghost')
ghost.title = 'Friendly ghost'              # technically, this title is never used by room desc
ghost.desc = "A smiling, friendly ghost."   # must be there for response to 'LOOK' command
ghost.is_listed = False                     # do not list item in ANY inventory list
ghost.is_takeable = False                   # cannot be taken (don't forget this!!)

# ------
# ROOMS
# ------

room_list = []

# ---- STARTING ROOM ----

startroom = Room('startroom')
startroom.title = "HOME SWEET HOME"
startroom.desc = "You are in your comfortable, familiar home room."
startroom.add_exit(west='otherroom')
startroom.inventory.add(book)
room_list.append(startroom)

# ---- OTHER ROOM ----

otherroom = Room('otherroom')
otherroom.title = "STRANGE NEW ROOM"
otherroom.desc = "This is a strange, unfamiliar room. Exciting!\n" \
                 "There is a ghost here."
otherroom.add_exit(east='startroom')
room_list.append(otherroom)



# initialize player information and
# start the player in startroom
pc = Player(startroom)

