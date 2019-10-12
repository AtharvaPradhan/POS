a=b=3 # A stands for Man and B for Lion
c=d=0 # C stands for Man and D for Lion

print("Side1:\nMan :",a," Lion :",b)
print("Now On next Side:\nMan :",c," Lion :",d)

Man="Man "
Lion="Lion "

boat=Man+Lion
a-=1
b-=1
print("\nSide1:\n""Man :",a," Lion :",b)
print("In Boat",boat)
d+=1
print("Now On next Side:\nMan :",c," Lion :",d)
boat="Going back with"+Man

while b>0:
    if a==b or a==0:
        boat=Man+Lion
        b-=1
        print("\nSide1:\n""Man :",a," Lion :",b)
        print("In Boat",boat)
        d+=1
        print("Now On next Side:\nMan :",c," Lion :",d)
        boat="Going back with"+Man
        if(b==0):
            print("Man lands from the boat\n")
            c+=1
            print("Now On next Side:\nMan :",c," Lion :",d)

    if(a>b):
        boat=Man+Man
        a-=1
        print("\nSide1:\n""Man :",a," Lion :",b)
        print("In Boat",boat)
        c+=1
        print("Now On next Side:\nMan :",c," Lion :",d)
        d-=1
        boat="Going back with"+Man+Lion
        print(boat+"Now On next Side:\nMan :",c," Lion :",d)
        b+=1
        print("Side1:\n""Man :",a," Lion :",b)

    if b>a and a!=0:
        boat=Man+Man
        a-=1
        print("\nSide1:\n""Man :",a," Lion :",b)
        print("In Boat",boat)
        c+=1
        print("Now On next Side:\nMan :",c," Lion :",d)
        boat="Going back with"+Man
        print(boat)