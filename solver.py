# Mohammad Sheva Almeyda Sofjan | 13519018
# Deterministic 2048 Solver with Backtracking Algo
# https://github.com/moshval/2k28solver
# Game design inspired by https://www.youtube.com/watch?v=b4XP2IcI-Bg


from time import time 

MAX_TILE = 8
SQUARE = 4
ADDED = 2
def initGame():
    tile = [[0 for i in range(SQUARE)] for j in range(SQUARE)]
    tile = add(tile)
    tile = add(tile)
    return tile


def printGame(tile):
    for i in range(SQUARE):
        print("[", end=" ")
        for j in range(SQUARE):
            if len(str(tile[i][j])) == 1:
                print(" "+str(tile[i][j]), end=" ")
            else:
                print(tile[i][j], end=" ")
        print(" ]")


def add(tile):
    found = False
    for i in range(len(tile)):
        for j in range(len(tile)):
            if(tile[i][j] == 0):
                a = i
                b = j
                found = True
                break
        if(found):
            tile[a][b] = ADDED
            break

    return tile


def merge(tile, valid):
    for i in range(len(tile)):
        for j in range(len(tile) - 1):
            if(tile[i][j] != 0 and tile[i][j] == tile[i][j+1]):
                tile[i][j] *= 2
                tile[i][j+1] = 0
                valid = True
    return tile, valid


def rev(tile):
    temp = [[0 for i in range(SQUARE)] for j in range(SQUARE)]
    for i in range(len(tile)):
        for j in range(len(tile[0])):
            temp[i][j] = (tile[i][len(tile[0]) - 1 - j])
    return temp


def tpose(tile):
    temp = [[0 for i in range(SQUARE)] for j in range(SQUARE)]
    for i in range(len(tile[0])):
        for j in range(len(tile)):
            temp[i][j] = (tile[j][i])
    return temp


def stack(tile):
    temp = [[0 for i in range(SQUARE)] for j in range(SQUARE)]
    valid = False
    for i in range(SQUARE):
        idx = 0
        for j in range(SQUARE):
            if(tile[i][j] != 0):
                temp[i][idx] = tile[i][j]
                if(j != idx):
                    valid = True
                idx += 1
    return temp, valid


def right(tile):
    # print("RIGHT")
    tile = rev(tile)
    tile, valid = stack(tile)
    tile, valid = merge(tile, valid)
    tile = rev(stack(tile)[0])
    return tile, valid


def left(tile):
    # print("LEFT")
    tile, valid = stack(tile)
    tile, valid = merge(tile, valid)
    tile = stack(tile)[0]
    return tile, valid


def up(tile):
    # print("UP")
    tile = tpose(tile)
    tile, valid = stack(tile)
    tile, valid = merge(tile, valid)
    tile = tpose(stack(tile)[0])
    return tile, valid


def down(tile):
    # print("DOWN")
    tile = rev(tpose(tile))
    tile, valid = stack(tile)
    tile, valid = merge(tile, valid)
    tile = tpose(rev(stack(tile)[0]))
    return tile, valid


def state(tile):
    for i in range(SQUARE):
        for j in range(SQUARE):
            if(tile[i][j] == MAX_TILE):
                return "W"

    for i in range(SQUARE):
        for j in range(SQUARE):
            if(tile[i][j] == 0):
                return "OG"
    # Mergeable
    for i in range(SQUARE - 1):
        for j in range(SQUARE - 1):
            if(tile[i][j] == tile[i+1][j] or tile[i][j] == tile[i][j+1]):
                return "OG"
    for i in range(SQUARE - 1):
        if(tile[i][SQUARE - 1] == tile[i+1][SQUARE - 1]):
            return "OG"
    for i in range(SQUARE - 1):
        if(tile[SQUARE - 1][i] == tile[SQUARE - 1][i+1]):
            return "OG"
    return "L"


def Game(game, cmd):
    printGame(game)
    if(cmd == 'w'):
        game, valid = up(game)
    elif(cmd == 's'):
        game, valid = down(game)
    elif(cmd == 'a'):
        game, valid = left(game)
    elif(cmd == 'd'):
        game, valid = right(game)
    else:
        print("Invalid")
        valid = False

    if(state(game) == "OG" and valid == True):
        game = add(game)
    elif(state(game) == "W"):
        print("Win")
        printGame(game)
    elif(state(game) == "L"):
        print("Lose")
        printGame(game)

    return game


def Play(game):
    while(True):
        printGame(game)
        print()
        cmd = input("Enter input : ")
        if(cmd == 'w'):
            game, valid = up(game)
        elif(cmd == 's'):
            game, valid = down(game)
        elif(cmd == 'a'):
            game, valid = left(game)
        elif(cmd == 'd'):
            game, valid = right(game)
        else:
            print("Invalid")
            valid = False

        if(state(game) == "OG" and valid == True):
            game = add(game)
        elif(state(game) == "W"):
            print("Win")
            printGame(game)
            break
        elif(state(game) == "L"):
            print("Lose")
            printGame(game)


result = []
counter = []
movestack = []
prio = ['w','a','s', 'd']


def canMove(tile, cmd):
    if(cmd == 'w'):
        tmp, val = up(tile)
    elif(cmd == 's'):
        tmp, val = down(tile)
    elif(cmd == 'a'):
        tmp, val = left(tile)
    elif(cmd == 'd'):
        tmp, val = right(tile)
    
    tmp = add(tmp)

    return val and state(tmp)!="L"


def move(tile, cmd, mv,pr):
    if(cmd == 'w'):
        mv.append("Up")
        if(pr):
            print("Up")
        tile = up(tile)[0]
        tile = add(tile)
    elif(cmd == 's'):
        mv.append("Down")
        if(pr):
            print("Down")
        tile = down(tile)[0]
        tile = add(tile)
    elif(cmd == 'a'):
        mv.append("Left")
        if(pr):
            print("Left")
        tile = left(tile)[0]
        tile = add(tile)
    elif(cmd == 'd'):
        mv.append("Right")
        if(pr):
            print("Right")
        tile = right(tile)[0]
        tile = add(tile)
    return tile,mv


def simulate():
    result.clear()
    counter.clear()
    movestack.clear()
    tile = initGame()
    moves = []
    print("State Awal : ")
    printGame(tile)
    print("Goal : " + str(MAX_TILE))
    inittime = time()
    solve(tile, 0,moves)
    # search(tile)
    return result,counter,inittime


def solve(tile, count, moves):
    if(state(tile) == "W"):
        result.append(tile)
        counter.append(count)
        movestack.append(moves)
        # printGame(tile)
        return True
    if(state(tile) == "L"):
        # printGame(tile)
        return False
    res = False
    for i in range(len(prio)):
        temp = []
        for x in range(len(tile[0])):
            temp.append([])
            for y in range(len(tile)):
                temp[x].append(tile[x][y])
        mst = []
        for x in range(len(moves)):
            mst.append(moves[x])

        if(canMove(temp, prio[i])):
            # count+=1
            temp,mst = move(temp, prio[i],mst,False)
            # printGame(temp)
            res = solve(temp, count+1,mst)
            # if(res==True):
            #     return True
            temp = []
            for x in range(len(tile[0])):
                temp.append([])
                for y in range(len(tile)):
                    temp[x].append(tile[x][y])
            mst = []
            for x in range(len(moves)):
                mst.append(moves[x])
    return res

def search(tile):
    if(state(tile) != "OG"):
        result.append(tile)
        # printGame(tile)
        return True
    res = False
    for i in range(len(prio)):
        temp = []
        for x in range(len(tile[0])):
            temp.append([])
            for y in range(len(tile)):
                temp[x].append(tile[x][y])
        if(canMove(temp, prio[i])):
            # count+=1
            temp = move(temp, prio[i],False)
            # printGame(temp)
            res = search(temp)
            # if(res==True):
            #     return True
    return res



if __name__ == '__main__':
    # tile = initGame()
    # canMove(tile,'s')
    # tile = move(tile,'s')
    # printGame(tile)

    r,c,inittime = simulate()
    print("Time req : " + str(time() - inittime) + " s")
    print("Banyak Konfigurasi State Akhir : " + str(len(c)))
    print("Minimum Move : " + str(min(c)))
    print("Maximum Move : " + str(max(c)))    
    for i in range(len(r)):
        print("Solusi " + str(i+1) + " , Banyak move = "+str(c[i]))
        print("Moves : ",end ="")
        print(movestack[i])
        print("Hasil Akhir : ")
        printGame(r[i])
        print()
    # r = simulate()
    # print(r)
    # print(len(r))

    # tile = initGame()
    # Play(tile)
