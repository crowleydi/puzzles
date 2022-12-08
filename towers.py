#! /usr/bin/env python3

# can solve some of the puzzles (easy, hard) from
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html

def initBoard(bs):
    global board,board_size
    board_size=bs
    s = set()
    for j in range(board_size):
        s.add(j+1)
    board=list()
    for i in range(board_size*board_size):
        board.append(s.copy())

def addoption(opts,o):
    for i in range(len(o)):
        opts[i].add(int(o[i]))

def allunique(val):
    s = set()
    for v in val:
        s.add(v)
    return len(s) == len(val)

def checkleft(val, lh):
    v = 1
    cv = val[0]
    for c in val:
        if c > cv:
            v = v + 1
            cv = c

    return lh == 0 or v == lh


def isvalid(val, lh, rh):
    return allunique(val) and checkleft(val,lh) and checkleft(val[::-1],rh)

def nextPos(cur,opts,lh,plist,rh):
    i = len(cur)
    if i < len(plist):
        ps = plist[i]
        for p in ps:
            nextPos(cur + str(p),opts,lh,plist,rh)
    else:
        if isvalid(cur, lh, rh):
            addoption(opts,cur)

def row(rn):
    r=list()
    for i in range(board_size):
        r.append(board[rn*board_size+i])
    return r

def col(cn):
    c=list()
    for i in range(board_size):
        c.append(board[i*board_size+cn])
    return c

def runset(lh, plist, rh):
    opts=[set() for _ in range(len(plist))]
    nextPos("",opts,lh,plist,rh)
    return opts

def setrow(r,s):
    global board
    for i in range(board_size):
        board[r*board_size+i]=s[i]

def setcol(c,s):
    global board
    for i in range(board_size):
        board[i*board_size+c]=s[i]

def runboard(lh,rh,to,bo):
    for r in range(board_size):
        ret=runset(lh[r],row(r),rh[r])
        setrow(r,ret)
    for c in range(board_size):
        ret=runset(to[c],col(c),bo[c])
        setcol(c,ret)

def trim(n,r):
    if n < 0:
        raise ValueError("can't trim a negative value")
    if n == 1:
        r[0].clear()
        r[0].add(board_size)
        for i in range(1,board_size):
            r[i].discard(board_size)
    elif n == 2:
        r[0].discard(board_size)
        r[1].discard(board_size-1)
    elif n == board_size: 
        for i in range(1,board_size+1):
            r[i-1].clear()
            r[i-1].add(i)
    elif n < board_size:
        for i in range(n-1):
            for ii in range(board_size-n+i+2,board_size+1):
                r[i].discard(ii)
    return r

def trim_board(lh,rh,to,bo):
    for i in range(board_size):
        r=row(i)
        trim(lh[i],r)
        r.reverse()
        trim(rh[i],r)

        c=col(i)
        trim(to[i],c)
        c.reverse()
        trim(bo[i],c)

def getcount():
    s=0
    for b in board:
        s += len(b)
    return s

def printboard():
    for r in range(board_size):
        print(row(r))

def solve(lh,rh,to,bo):
    solved=False
    last=0
    loops=0
    cur = getcount()
    trim_board(lh,rh,to,bo)
    while not solved and last != cur:
        last = cur
        runboard(lh,rh,to,bo)
        loops += 1
        print('after loop ' + str(loops))
        printboard()
        cur = getcount()
        solved = (cur == board_size*board_size)
    return solved,loops

def setpiece(r,c,v):
    rw=row(r-1)
    co=col(c-1)
    for i in range(board_size):
        rw[i].discard(v)
        co[i].discard(v)

    board[(r-1)*board_size+(c-1)]={v}

if __name__ == '__main__':
# create board size 6x6
    initBoard(6)

#init some pieces
#setpiece(1,4,2)
#setpiece(5,6,3)
#setpiece(6,1,4)
#lh=[0,2,2,0,1,3]
#rh=[3,0,3,3,3,0]
#to=[0,0,3,2,0,0]
#bo=[0,3,2,2,0,0]

    #initBoard(6)
    #setpiece(6,3,2)
    #lh=[0,4,3,0,0,0]
    #rh=[2,1,0,0,2,3]
    #to=[3,4,0,4,2,0]
    #bo=[0,3,4,0,0,0]

    initBoard(9)
    setpiece(2,8,4)
    setpiece(3,3,3)
    setpiece(3,5,1)
    setpiece(4,2,2)
    setpiece(4,3,6)
    setpiece(5,4,8)
    setpiece(5,6,4)
    setpiece(6,3,4)
    setpiece(6,7,9)
    setpiece(7,2,8)
    setpiece(7,4,2)
    setpiece(8,5,3)
    setpiece(9,6,6)
    lh=[0,3,0,5,3,0,0,0,2]
    rh=[2,5,4,0,3,2,1,0,2]
    to=[0,2,3,0,0,4,3,0,3]
    bo=[0,3,0,0,2,0,4,4,0]

    solved,loops=solve(lh,rh,to,bo)
    print("stopped after " + str(loops) + " loops")
    print("not solved :(") if not solved else print("solved!")
