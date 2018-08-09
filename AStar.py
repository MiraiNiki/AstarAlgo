#Created by MiraiNiki 201820683

import numpy as np
import copy
board = np.zeros((4,3),dtype=int)
root = np.zeros((4,3),dtype=int)
collect_board = np.zeros((4,3),dtype=int)
number = [0,1,2,3,4,5,6,7,8,9,10,11]
test_number = [6,1,5,0,2,3,9,8,4,10,7,11]
openList = {}
closeList = {}
h = 0
#Goal status
def collect_board_init(board):
    collect_queue = copy.deepcopy(number)
    i = 0
    j = 0
    for i in range(4):
        for j in range(3):
            board[i][j] = collect_queue[0]
            collect_queue = np.delete(collect_queue,0)
    return board
#Start status
def board_init(board):
    rand_queue = np.random.permutation(number)
    i = 0
    j = 0
    for i in range(4):
        for j in range(3):
            board[i][j] = rand_queue[0]
            rand_queue = np.delete(rand_queue,0)
    return board
#リストtest_numberから盤面を作成する
def test_board_init(board):
    collect_queue = copy.deepcopy(test_number)
    i = 0
    j = 0
    for i in range(4):
        for j in range(3):
            board[i][j] = collect_queue[0]
            collect_queue = np.delete(collect_queue,0)
    return board

#h(board), 現在の盤面からゴール状態までの推定コスト　manhatan distanceを採用
def h(board):
    distance = 0
    i = 0
    for i in range(12):
            currentPos = np.where(board == i)
            collectPos = np.where(collect_board == i)
            distance = np.abs(currentPos[0][0] - collectPos[0][0]) + np.abs(currentPos[1][0] - collectPos[1][0]) + distance
    return distance

#make a copy of current board
def tempBoard(board):
    temp = copy.deepcopy(board)
    return temp

#OpenListから行列として盤面を取り出す時に使う行列生成関数
def boardToString(board):
    s = str(int(board[0][0])) + " " + str(int(board[0][1])) + " " + str(int(board[0][2])) \
        + " " + str(int(board[1][0])) + " " + str(int(board[1][1])) + " " + str(int(board[1][2])) \
        + " " + str(int(board[2][0])) + " " + str(int(board[2][1])) + " " + str(int(board[2][2]))\
        + " " + str(int(board[3][0])) + " " + str(int(board[3][1])) + " " + str(int(board[3][2]))
    return s

#OpenListに保存するためのkeyとして、盤面の状態を表す文字列生成関数
def stringToBoard(s):
    cList = s.split()
    nList = [int(c) for c in cList]
    b = np.zeros((4, 3),dtype=int)
    for i in range(4):
        for j in range(3):
            b[i][j] = nList[0]
            nList = np.delete(nList, 0)
    return b
#stringToBoardのテスト
def testStringToBoard():
    s = "0 1 2 3 4 5 6 7 8 9 10 11"
    print(stringToBoard(s))

#boardをopenlistに入れ、closelistに合った場合は削除する
def addBoardToOpenList(board,preboard):
    opCandidate = boardToString(board)
    openList[opCandidate] = boardToString(preboard)
    deleteBoardFromCloseList(board)

#openlistからcloselistにboard情報を伝え、openlistから削除する
def copyBoardToCloseList(board):
    clCandidate = boardToString(board)
    if clCandidate not in closeList:
        closeList[clCandidate] = openList[clCandidate]
    deleteBoardFromOpenList(board)

#openListから盤面を削除
def deleteBoardFromOpenList(board):
    delBoard = boardToString(board)
    if delBoard in openList:
        del openList[delBoard]

#closeListから盤面を削除
def deleteBoardFromCloseList(board):
    delBoard = boardToString(board)
    if delBoard in closeList:
        del closeList[delBoard]

#f(board) = g(board) + h(board), f(board)は最短経路コスト
def func(board):
    return g(board) + h(board)

#g(board),スタートから現在の盤面までの経路コスト
def g(board):
    count = -1
    # print(board)
    b = tempBoard(board)
    s = boardToString(b)
    # print(s)
    while s != boardToString(root):
        count = count + 1
        if s in openList:
            preS = openList[s]
            b = stringToBoard(preS)
            s = boardToString(b)
        elif s in closeList:
            preS = closeList[s]
            b = stringToBoard(preS)
            s = boardToString(b)
    return count

#bに隣接するノードを探す（0を動かした時、それが盤面に含まれるか）
#ノードがあればf(m)を計算する
#1 openにもcloseにもない
#2 すでにopenにある（まだ探索していないノードだが、覚えているものよりf(ノード)が小さい）
#3 Closeにある場合よりf(ノード)が小さくなるならばOpenに復活させる
def findNeighbors(board):
    # score = [-1000, -1000, -1000, -1000] #上下左右
    #隣接のノードをさがすため
    zeroPos = np.where(board == 0)

    if zeroPos[0][0] - 1 >= 0: # 上は隣接ノード
        temp = tempBoard(board)
        temp[zeroPos[0][0] - 1][zeroPos[1][0]] = board[zeroPos[0][0]][zeroPos[1][0]]
        temp[zeroPos[0][0]][zeroPos[1][0]] = board[zeroPos[0][0] - 1][zeroPos[1][0]]

        tempS = boardToString(temp)
        if tempS not in openList and tempS not in closeList:
            addBoardToOpenList(temp, board)
        elif tempS in openList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)
        elif tempS in closeList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)


    if zeroPos[0][0] + 1 <= 3: # 下は隣接ノード
        temp = tempBoard(board)
        temp[zeroPos[0][0] + 1][zeroPos[1][0]] = board[zeroPos[0][0]][zeroPos[1][0]]
        temp[zeroPos[0][0]][zeroPos[1][0]] = board[zeroPos[0][0] + 1][zeroPos[1][0]]

        tempS = boardToString(temp)
        if tempS not in openList and boardToString(temp) not in closeList:
            addBoardToOpenList(temp, board)
        elif tempS in openList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)
        elif tempS in closeList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)

    if zeroPos[1][0] - 1 >= 0: # 左は隣接ノード
        temp = tempBoard(board)
        temp[zeroPos[0][0]][zeroPos[1][0] - 1] = board[zeroPos[0][0]][zeroPos[1][0]]
        temp[zeroPos[0][0]][zeroPos[1][0]] = board[zeroPos[0][0]][zeroPos[1][0] - 1]

        tempS = boardToString(temp)
        if tempS not in openList and boardToString(temp) not in closeList:
            addBoardToOpenList(temp, board)
        elif tempS in openList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)
        elif tempS in closeList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)

    if zeroPos[1][0] + 1 <= 2: # 右は隣接ノード
        temp = tempBoard(board)
        temp[zeroPos[0][0]][zeroPos[1][0] + 1] = board[zeroPos[0][0]][zeroPos[1][0]]
        temp[zeroPos[0][0]][zeroPos[1][0]] = board[zeroPos[0][0]][zeroPos[1][0] + 1]

        tempS = boardToString(temp)
        if tempS not in openList and boardToString(temp) not in closeList:
            addBoardToOpenList(temp, board)
        elif tempS in openList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)
        elif tempS in closeList:
            if func(temp) > (g(board) + h(temp) + 1):
                addBoardToOpenList(temp, board)
    return 0

#find min f(n) from Open list
#openlist内の全ての状態にたいしてculcdistanceをして、最小のボードを一つ返す関数
#注意: str->boardをつかう
def findMinfunction():
    min = 100000
    minB = tempBoard(board)
    for open in openList:
        b = stringToBoard(open)
        temp = func(b)
        if min > temp:
            min = temp
            minB = tempBoard(b)
    return minB

cnt = -1
def aStar():
    global cnt
    cnt = cnt + 1
    if len(openList) == 0:
        print("経路はありません")
        return -1
    b = findMinfunction()
    print(b)
    print("g(n) = " + str(g(b)))
    print("h(n) = " + str(h(b)))
    if h(b) == 0:
        print("経路をみつけました")
        print("cnt = " + str(cnt))
        return g(b)
    else:
        copyBoardToCloseList(b)
    findNeighbors(b)
    aStar()


board = test_board_init(board)
collect_board = collect_board_init(collect_board)
addBoardToOpenList(board,root)
aStar()
