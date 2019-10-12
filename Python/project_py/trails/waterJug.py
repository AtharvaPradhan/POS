jug1 = 4 # 4 ltrs jug without water 
jug2 = 3 # 3 ltrs jug without water
t = 2 #t is target of getting 2 liters filled in any jug

def jugSolver(amt1, amt2):

    print(amt1, amt2)

    if (amt1 == t and amt2 == 0) or (amt1 == 0 and amt2 == t):
        return

    elif amt2 == jug2:
        jugSolver(amt1, 0)

    elif amt1 != 0:
        if amt1 <= jug2-amt2:
            jugSolver(0, amt1+amt2)
        elif amt1 > jug2-amt2: 
            jugSolver(amt1-(jug2-amt2),amt2+(jug2-amt2)) #4-(3-1)=2 1+(3-1)=3

    else:
        jugSolver(jug1, amt2)

jugSolver(0,0)