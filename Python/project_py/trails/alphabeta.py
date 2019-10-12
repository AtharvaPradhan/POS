tree = [[[5,9,2],[8,8,2]],
        [[4,5,1],[3,3,3]]]
##declaring tree##
root = 0 ## the roots##
pruned = 0 ## number of cuts##

def children(branch,depth,alpha,beta):
    ##declaring these as globals##
    global tree
    global root
    global pruned
    i = 0  ##defining i as int for increamenting##
    for child in branch:  ##finding node ##
        if type(child) is list:  ##setting condition##
            (nalpha,nbeta) = children(child,depth + 1,alpha,beta)##tuple of the returned variables##
            if depth % 2 == 1: ##condition for Max##
                beta = nalpha if alpha < beta else beta  ##compring the values of children
            else:
                alpha = nbeta if nbeta > alpha else alpha  ##comparing values of children

            branch[i] = alpha if depth % 2 == 0 else beta   ##i = 0 the zeroth branch value decided##
            i += 1 ## increament i##
        ##similarly the opposite condition
        else:
            if depth % 2 == 0 and alpha < child:
                alpha = child
            if depth % 2 != 0 and beta > child:
                beta = child

            if alpha >= beta:
                pruned += 1
                break

        if depth == root:
            tree = alpha if root == 0 else beta
        return (alpha,beta)

def alphabeta(in_tree=tree, start = root,upper = -15,lower = 15):
    global tree
    global pruned
    global root
    (alpha,beta) = children(tree,start,upper,lower) ##taking values as alpha beta##

    if __name__ == "__main__":  ##if you dont know this shit then go to hell##
        print("(alpha,beta):",alpha,beta)  ##values of alpha beta##
        print("Result:",tree)    ##resultuts of the algorithm##
        print("Times pruned: ",pruned) ##no of c
    return (alpha,beta,tree,pruned)

if __name__ == '__main__':
    alphabeta(None)