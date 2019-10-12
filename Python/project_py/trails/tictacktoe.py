import sys

l1 = ["-","-","-","-","-","-","-","-","-","-"]
Game = 1
player = None
def choose(pla):
    choice = int(input("Enter the position:  "))
    if l1[choice] == "-":
        l1[choice] = pla
    elif l1[choice] != "-":
        print("This position is occupied please enter some other position")
        choose(pla)
    elif choice > 9:
        print("This position does not exists.Please enter something meaningful")
        choose(pla)
    else:
        print("Please reenter choice")


def CheckWin():
    if l1[1] == l1[2] == l1[3]==player or l1[4] == l1[5] == l1[6] == player or l1[7] == l1[8] == l1[9]==player or l1[1] == l1[4] == l1[7]==player or l1[2] == l1[5] == l1[8]==player or l1[3] == l1[6] == l1[9]==player or l1[1] == l1[5] == l1[9]==player or l1[3] == l1[5] == l1[7] == player:
        print("Player {} wins".format(player))
        Game = 0
        sys.exit(0)
    else:
        Game = 1
        
def Board():
    print("_____________")
    print(" {}| {}| {}|".format(l1[1],l1[2],l1[3]))
    print("  |  |  ")
    print("_____________")
    print(" {}| {}| {}|".format(l1[4], l1[5], l1[6]))
    print("  |  |  ")
    print("_____________")
    print(" {}| {}| {}|".format(l1[7], l1[8], l1[9]))
    print("  |  |  ")
    print("_____________")


def main():
    counter = 0
    global player
    while Game:
        if counter <= 9:
            if counter %2 == 0:
                player = 'x'
                Board()
                choose(player)
                CheckWin()
                counter += 1
            else:
                player = 'o'
                Board()
                choose(player)
                CheckWin()
                counter += 1

        else:
            print("It is a TIe")

main()