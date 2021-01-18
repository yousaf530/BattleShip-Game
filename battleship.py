

# ? User Input his 4 ships of length 4,3,2,2 in the battle field and game Starts.


import sys
import random
from random import randrange
import cProfile
import pstats
import io
#from guppy import hpy


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):

        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner

#! Check that boat does not go outside of board


def check_boatinboard(boat, taken):
    boat.sort()
    for i in range(len(boat)):
        num = boat[i]
        if num in taken:
            boat = [-1]
            break
        elif num < 0 or num > 99:
            boat = [-1]
            break
        elif num % 10 == 9 and i < len(boat) - 1:
            if boat[i+1] % 10 == 0:
                boat = [-1]
                break
        if i != 0:
            if boat[i] != boat[i-1] + 1 and boat[i] != boat[i-1] + 10:
                boat = [-1]
                break
    return boat

#! Generate random boat


def check_boat(boatsize, start, direction, taken):
    boat = []
    if direction == 1:  # ! Upward Direction
        for i in range(boatsize):
            boat.append(start - (i*10))
            boat = check_boatinboard(boat, taken)
    elif direction == 2:  # ! L to R Direction
        for i in range(boatsize):
            boat.append(start + i)
            boat = check_boatinboard(boat, taken)
    elif direction == 3:  # ! Downward Direction
        for i in range(boatsize):
            boat.append(start + (i*10))
            boat = check_boatinboard(boat, taken)
    elif direction == 4:  # ! R to L Direction
        for i in range(boatsize):
            boat.append(start - i)
            boat = check_boatinboard(boat, taken)
    return boat

#! Gets the user input guess and perform checks


def get_shot(guesses):
    ok = None
    while ok is None:
        try:
            shot = int(input("\nKindly enter your guess: "))
            if shot < 0 or shot > 99:
                print("Incorrect shot. Kindly enter number btw 0-99\n")
            elif shot in guesses:
                print("Already Guessed. Enter another number.\n")
            else:
                ok = "y"
                break
        except:
            print("Incorrect shot. Kindly enter btw 0-99\n")
    return shot

#! Prints the Computer Turn Battleship board on the screen


def show_board_c(taken):

    print("\n     0  1  2  3  4  5  6  7  8  9 \n")

    place = 0
    for i in range(10):
        row = ""
        for j in range(10):
            ch = " - "
            if place in taken:
                ch = " o "
            row = row + ch
            place = place + 1
        print(i, " ", row)

#! Prints the Battleship board on the screen


def show_board(hit, miss, comp):

    print("\n     0  1  2  3  4  5  6  7  8  9 \n")

    place = 0
    for i in range(10):
        row = ""
        for j in range(10):
            ch = " - "
            if place in miss:
                ch = " x "
            elif place in hit:
                ch = " o "
            elif place in comp:
                ch = " 0 "
            row = row + ch
            place = place + 1
        print(i, " ", row)

#! Checks whether the shots hit, miss or sink the boat


def check_shot(shot, ships, hit, miss, comp):
    missed = 0
    stat = ""
    for i in range(len(ships)):

        if shot in ships[i]:
            ships[i].remove(shot)
            if len(ships[i]) > 0:
                hit.append(shot)
                missed = 1
                stat = "Hit!"
            else:
                comp.append(shot)
                missed = 2
                stat = "destroyed the ship"
    if missed == 0:
        miss.append(shot)
        stat = "Missed!"

    return ships, hit, miss, comp, missed, stat

#! Create valid computer boats in the board


# @profile
def create_boats(taken):
    ships = []
    boats = [4, 3, 2, 2]
    for b in boats:
        boat = [-1]
        while boat[0] == -1:
            boat_start = randrange(99)
            boat_direction = randrange(1, 4)
            boat = check_boat(b, boat_start, boat_direction, taken)
        ships.append(boat)
        taken = taken + boat
    return ships, taken

#! Ask user to input ship lenght


def get_playerships(long, taken):
    ok = True
    while ok:
        ship = []
        print("==> Enter your ship of ", long,
              " blocks lenght in the board <==")
        for i in range(long):
            try:
                boat_num = input("Enter a number: ")
                ship.append(int(boat_num))
            except:
                print("Kindly handle with care. Invalid Input. Going to Sleep.\n")
                sys.exit()

        ship = check_boatinboard(ship, taken)

        if ship[0] != [-1]:
            taken = taken + ship
            break
        else:
            print("Error. Please try again.")
    return ship, taken

#! Create valid player boats in the board


def create_playerboats(taken):
    ships = []
    boats = [4, 3, 2, 2]
    for boat in boats:
        ship, taken = get_playerships(boat, taken)
        ships.append(ship)

    return ships, taken

#! Computer makes guesses


def get_shot_c(guesses, tactics):

    ok = None
    while ok is None:
        try:
            if len(tactics) > 0:
                shot = tactics[0]
            else:
                shot = randrange(99)
            if shot not in guesses:
                ok = "y"
                guesses.append(shot)
                break
        except:
            print("Incorrect shot. Kindly enter btw 0-99\n")
    return shot, guesses

#! Calculate Tactics for the computer to play tactically


def cal_tactics(shot, tactics, guesses, hit):
    temp = []
    if len(tactics) < 1:
        temp = [shot-1, shot+1, shot-10, shot+10]
    else:
        if shot-1 in hit:
            temp = [shot + 1]
            for i in [2, 3, 4, 5, 6, 7]:
                if shot-i not in hit:
                    temp.append(shot-i)
                    break
        elif shot+1 in hit:
            temp = [shot - 1]
            for i in [2, 3, 4, 5, 6, 7]:
                if shot+i not in hit:
                    temp.append(shot+i)
                    break
        elif shot-10 in hit:
            temp = [shot + 10]
            for i in [20, 30, 40, 50, 60, 70]:
                if shot-i not in hit:
                    temp.append(shot-i)
                    break
        elif shot+10 in hit:
            temp = [shot - 10]
            for i in [20, 30, 40, 50, 60, 70]:
                if shot+i not in hit:
                    temp.append(shot+i)
                    break

    candidate = []
    for i in range(len(temp)):
        if temp[i] not in guesses and i < 100 and temp[i] > -1:
            candidate.append(temp[i])
    random.shuffle(candidate)
    return candidate


#! To check if ships are sunk
def check_ifempty(ships):
    return all([not elem for elem in ships])

#! Main Program


print("\n==> THE MIGHTY BATTLE SHIP GAME <==\n")

print("==> Instructions! Read Carefully.<==\n")
print("1)The game consist of 4 ships of sizes 4,3,2,2")
print("2)If you enter an Invalid ship, it will not be added to your board.")
print("3)The game will end when either computer or player wins.\n")

print("On the board \n ==> x = Missed the shot \n ==> o = Hit the shot \n ==> 0 = Ship destroyed/sank/completed\n")


# ? Before the Game Starts
#! Computer(1) Lists
hit1 = []
miss1 = []
comp1 = []
guesses1 = []
missed1 = 0
tactics1 = []
taken1 = []
stat1 = ""
#! Player(2) Lists
hit2 = []
miss2 = []
comp2 = []
guesses2 = []
missed2 = 0
tactics2 = []
taken2 = []
stat2 = ""

# ? Player Enter his Ship

# ? Computer Creates Board 1
ships1, taken1 = create_boats(taken1)

# ? Platey Creates its Board 2
ships2, taken2 = create_playerboats(taken2)
print("\n==> Your Board <==\n")
show_board_c(taken2)


# ?loop
for i in range(200):

    #! Player Shoots
    guesses1 = hit1 + miss1 + comp1
    shot1 = get_shot(guesses1)
    ships1, hit1, miss1, comp1, missed1, stat1 = check_shot(
        shot1, ships1, hit1, miss1, comp1)
    #!Show Board After Player Turn
    print("\n==>Computer's Board After Player Shoot <==\n")
    show_board(hit1, miss1, comp1)
    print("\n   ==> You " + stat1)

    #! Repeats until ship sinks
    if check_ifempty(ships1):
        print("\n\n End of the game - You won! Total Moves Taken = ", i)
        break

    #! Computer Shoot
    shot2, guesses2 = get_shot_c(guesses2, tactics2)
    ships2, hit2, miss2, comp2, missed2, stat2 = check_shot(
        shot2, ships2, hit2, miss2, comp2)

    #!Show Board After Computer Turn
    print("\n==>Player's Board After Computer Shoots <==\n")

    show_board(hit2, miss2, comp2)
    print("\n   ==> Computer " + stat2)

    if missed2 == 1:
        tactics2 = cal_tactics(shot2, tactics2, guesses2, hit2)
    elif missed2 == 2:
        tactics2 = []
    elif len(tactics2) > 0:
        tactics2.pop(0)

    #! Repeats until ship sinks
    if check_ifempty(ships2):
        print("\n\n End of the game - Computer won! Total Moves Taken =", i)
        break


#! Total Heap Usage
#h = hpy()
# print(h.heap())
