from itertools import permutations

N=int(input("Enter Number Of Queens:"))
sols=0
cols = range(N)
total=0
for combo in permutations(cols):
    if N==len(set(combo[i]+i for i in cols))==len(set(combo[i]-i for i in cols)):
        sols += 1
        print('Solution '+str(sols)+': '+str(combo)+'\n')
        print("\n".join(' o ' *i + ' X ' +' o '*(N-i-1) for i in combo) +"\n\n\n\n")
        total=total+1
print(total)