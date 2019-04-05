# ifgame.py
# An IF game skeleton for simple, old-fashioned text adventures

import sys
from ifdata import *

# ----------
# SOME DATA
# ----------

# ALL known directions that the player may enter at prompt
known_directions = ('east', 'e', 'west', 'w', 'north', 'n', 'south', 's')

# The short list of formal directions, to be used by parser.
# See the defined nouns dictionary for matching known directions
# to formal ones.
formal_directions = ('north', 'east', 'south', 'west')

# initialize parser input class
parsed = ParsedCommand()

# ---------------------
# DISPLAY ROOM ROUTINE
# ---------------------

def show_room():
    print()
    if pc.location in room_list:
        for room in room_list:
            if pc.location == room:
                if pc.location.is_visited:
                    pc.location.show_short_desc()
                else:
                    pc.location.show_long_desc()
                    pc.location.is_visited = True
    else:
        print("ERROR: pc.location not in room_list")
        sys.exit()

# ---------------------
# VERB/ACTION ROUTINES
# ---------------------


def do_go():
    if parsed.noun in formal_directions:
        # loop through current room exits

        exit_found = False

        for exit in pc.location.exits:
            if parsed.noun == exit:
                for room in room_list:
                    if pc.location.exits[parsed.noun] == room.id:
                        exit_found = True
                        pc.location = room
                        break

        if exit_found == False:
            print("You can't go that way.")

    else:
        print("That is not a valid direction")
        return


def do_take():
    if parsed.noun == "NA":
        print("What do you want to take?")
        return

    item_there = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            item_there = True
            if item.is_takeable:
                pc.location.inventory.drop(item)
                pc.inventory.add(item)
                print("Taken.")
            else:
                print("You can't take that.")

    if item_there == False:
        print("I dont see a(n)",parsed.noun,"here.")

    return


def do_drop():
    if parsed.noun == "NA":
        print("What do you want to drop?")
        return

    item_carried = False

    for item in pc.inventory:
        if parsed.noun == item.id:
            pc.inventory.drop(item)
            pc.location.inventory.add(item)
            item_carried = True
            print("Dropped.")

    if item_carried == False:
        print("You are not carrying a",parsed.noun)

    return


def do_look():
    if parsed.noun == "NA":
        pc.location.is_visited = False
        return

    item_found = False

    for item in pc.location.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True

    for item in pc.inventory:
        if parsed.noun == item.id:
            print(item.desc)
            item_found = True

    if item_found == False:
        print("I don't see a(n)",parsed.noun,"here.")

    return


def do_inventory():
    print("You are carrying:")

    if len(pc.inventory) == 0:
        print("Nothing")
    else:
        pc.inventory.display()

def do_say():
    print("Saying something")


def do_quit():
    print("Exiting the game...")
    sys.exit()


def do_help():
    print("To play the game, enter either a VERB or a VERB NOUN command combination.")
    print("For a list of verbs understood by the parser, enter \"verbs\".")
    print("The game will be won when you have returned the cube to the starting room.")
    return


def do_verbs():
    print("The following verbs are recognized by the game:\n"
          "GO, GET, TAKE, DROP, LOOK, EXAMINE, INVENTORY, HELP, VERBS, and QUIT\n"
          "\nYou may enter the first letter of a direction by itself to move in\n"
          "that direction. You may also enter X for LOOK or EXAMINE, or I for\n"
          "INVENTORY.")


def do_nothing():
    pass

# ---------------
# DEFINED VERBS
# ---------------

# set up dictionary of verbs and the fucntions they use
verbs = Verbs()

# default verbs -- add your own routines as you go
verbs.add(go=do_go)
verbs.add(get=do_take, take=do_take)
verbs.add(drop=do_drop)
verbs.add(look=do_look, x=do_look, examine=do_look)
verbs.add(i=do_inventory, inventory=do_inventory)
verbs.add(say=do_say)
verbs.add(verbs=do_verbs)
verbs.add(help=do_help)
verbs.add(q=do_quit, quit=do_quit)

# used by the parser to indicate no action/incorrect verb
verbs.add(NA=do_nothing)

# -----------------
# PARSER ROUTINES
# -----------------

def parser_get_input():
    # clear all previously entered parser information
    parsed.reset()

    # get player input
    parsed.raw_input = (input("> ").lower()).split()


def parser_match_words():
    # make sure at least one and no more than two words are entered
    if len(parsed.raw_input) > 2 or len(parsed.raw_input) < 1:
        print("Commands must contain a two word verb/noun combination")
        parsed.verb = 'NA'
        return

    # if only one word entered, set to default noun (NA)
    # this indicates no noun was given
    if len(parsed.raw_input) == 1:
        parsed.raw_input.append("NA")

    # separate words
    first_word = parsed.raw_input[0]
    second_word = parsed.raw_input[1]

    # if direction only is entered, make noun the direction and verb "go"
    if first_word in known_directions:
        second_word = first_word
        first_word = "go"

    # match the verb typed/parsed with the appropriate entry in the verbs dictionary
    parsed.verb = parser_match_verb(first_word)

    # match the noun typed/parsed with the appropriate entry in the nouns dictionary
    parsed.noun = parser_match_noun(second_word)


def parser_match_verb(word):
    # match verb with entry in dictionary
    temp_verb = verbs.match_verb(word)

    # if verb is ERR (error, not found) return error message and return NA (no action)
    if temp_verb == "ERR":
        print("I do not know how to", word)
        return 'NA'
    # otherwise return appropriate verb from dictionary
    else:
        return temp_verb


def parser_match_noun(word):
    # match noun with entry in dictionary
    temp_noun = nouns.match_noun(word)

    # if noun is ERR (error, not found) return error message and return NA (noun unknown)
    if temp_noun == "ERR":
        print ("I do not know what a(n)", word, "is.")
        parsed.verb = 'NA'   # be sure to select do_nothing as a verb routine
        return
    # otherwise return appropriate noun from dictionary
    else:
        return temp_noun


def select_verb_routine(verb_selection):
    # use verbs dictionary to match verb with appropriate routine
    return verbs.match_routine(verb_selection)


# ----------
# THE GAME
# ----------

game_continues = True

while game_continues == True:
    # display the room information
    show_room()

    # have the player enter input
    parser_get_input()

    # match the verb/noun given with appropriate dictionary entries
    parser_match_words()

    # select the appropriate function to process parser results
    parsed.routine = select_verb_routine(parsed.verb)

    # run the selected function
    parsed.routine()
