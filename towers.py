#! /usr/bin/env python3

# can solve some of the puzzles (easy, hard) from
# https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/towers.html

def initBoard(bs):
    global board,board_size
    board_size=bs
    board=list()
    for i in range(board_size*board_size):
        s = set()
        for j in range(board_size):
            s.add(j+1)
        board.append(s)

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

def getcount():
    s=0
    for b in board:
        s = s + len(b)
    return s

def solve(lh,rh,to,bo):
    solved=False
    last=0
    loops=0
    cur = getcount()
    while not solved and last != cur:
        #print("cur size=" + str(cur))
        last = cur
        runboard(lh,rh,to,bo)
        loops = loops+1
        cur = getcount()
        solved = (cur == board_size*board_size)
    return solved,loops

def setpiece(r,c,v):
    global board,board_size
    board[(r-1)*board_size+(c-1)]={v}


# create board size 6x6
initBoard(6)

#init some pieces
setpiece(1,3,2)
setpiece(4,2,2)

#set constraints
lh=[0,4,0,4,0,0]
rh=[4,2,3,0,4,0]
to=[0,2,0,2,0,0]
bo=[3,1,0,3,0,0]

#solve
solved,loops=solve(lh,rh,to,bo)

# print the board
print("stopped after " + str(loops) + " loops")
print("not solved :(") if not solved else print("solved!")
for r in range(board_size):
    print(row(r))