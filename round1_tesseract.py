import copy

#values obtained after traversing the arena
rfid_tag = [[1,1,1,1,0],
[2,3,3,2,1],
[3,4,4,3,1],
[3,4,4,3,1],
[2,3,3,2,1]]

#sum matrix
s = [[0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0],
    [0,0,0,0,0]]

#Mines(Ambush Points) matrix
Mines =[[None,None,None,None,None],
        [None,None,None,None,None],
        [None,None,None,None,None],
        [None,None,None,None,None],
        [None,None,None,None,None]]

#function that returns a list of all possible neighbours of the given coordinate
def FindNeighbours(i,j):
    n = [[i-1,j],
        [i+1,j],
        [i,j-1],
        [i,j+1]]
    if i == 0:
        n.remove([i-1,j])
    if i == 4:
        n.remove([i+1,j])
    if j == 0:
        n.remove([i,j-1])
    if j == 4:
        n.remove([i,j+1])  
    return n

#marks all the given coordinates as Mines
def MarkMine(n,m):
    for i in n:
        if m[i[0]][i[1]] == None:
            m[i[0]][i[1]] = 'M '
        else:
            continue

#marks all the given coordinates as NOT Mines
def MarkNotMine(n,m):
    for i in n:
        if m[i[0]][i[1]] == None:
            m[i[0]][i[1]] = 'NM'
        else:
            pass

#reduces the value of list coordinates by one in the rfid values
def reduceNumbers(r,n):
    for i in n:
        if r[i[0]][i[1]] == 0:
            pass
        else:
            r[i[0]][i[1]] = r[i[0]][i[1]]-1

#checks if we have found the solutuion
def checkSolution(r):
    for i in range(len(r)):
        for j in range(len(r[i])):
            if r[i][j] != 0:
                return False
    return True

#returns a matrix with each value equal to the sum of its neighbours
def sumOfNeighbours(r):
    for i in range(len(r)):
        for j in range(len(r[i])):
            n = FindNeighbours(i,j)
            for a in n:
                s[i][j] += r[a[0]][a[1]]
    return s

#returns the list of all numbers in a summation matrix in descending order
def listofMaxNumbers(s):
    l = []
    for i in range(len(s)):
        for j in range(len(s[i])):
            if s[i][j] not in l:
                l.append(int(s[i][j]))
            else:
                pass
    return sorted(l)[::-1]

#returns all the coordinates of edited matrix
def MarkMineonNumber(r,m,v):
    l=[]
    for i in range(len(r)):
        for j in range(len(r[i])):
            if r[i][j] == v:
                if m[i][j] == None:
                    m[i][j] = 'M '
                else:
                    pass
                l.append([i,j])
    return l


######################
#Ambush Point Finding#
######################

#iteration reducing logic
for i in range(len(rfid_tag)):
    for j in range(len(rfid_tag[i])):
        n = FindNeighbours(i,j)
        if rfid_tag[i][j] == len(n):
            MarkMine(n,Mines)
        if rfid_tag[i][j] == 0:
            n = FindNeighbours(i,j)
            MarkNotMine(n,Mines)
        
for i in range(len(Mines)):
    for j in range(len(Mines[i])):
        if Mines[i][j] == 'M ':
            n = FindNeighbours(i,j)
            reduceNumbers(rfid_tag,n)

#main logic
r = copy.deepcopy(rfid_tag)
while True:
    if checkSolution(r):
        break
    else:
        s = sumOfNeighbours(r)
        maxList = listofMaxNumbers(s)
        m = maxList.pop(0)
        l = MarkMineonNumber(s,Mines,m)
        c= []
        for i in l:
            c += FindNeighbours(i[0],i[1])
        reduceNumbers(r,c)
        s = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]

#removing None from Mines matrix
for i in range(len(Mines)):
    for j in range(len(Mines[i])):
        if Mines[i][j] == None:
            Mines[i][j] = 'NM'

print(Mines)    

#######################
#Shortest Path Finding#
#######################

class Node:
    def __init__(self, parent, action, state):
        self.parent = parent
        self.action = action
        self.state = state

class QueueFrontier:
    def __init__(self):
        self.frontier = []

    def add(self ,node):
        self.frontier.append(node)

    def isEmpty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.isEmpty():
            print("error")
        else:
            return self.frontier.pop(0)

height = len(Mines)
width = len(Mines[0])
explored_states = []
    # print(height , width)
walls = []
start = (4,4)
goal = (0,0)
for i in range(height):
    row = []
    for j in range(width):
        #print(i,j)
        if Mines[i][j] == "NM":
            row.append(False)
        else:
            row.append(True)
    walls.append(row)

#print(walls)

def solve():
    start_node = Node(state = start, parent =None, action=[start])
    frontier = QueueFrontier()
    frontier.add(start_node)
    num_explored = 0
    explored_states = []
    all_nodes = []
    while True:
        if frontier.isEmpty():
            print("No solution")
            break

        node = frontier.remove()
        explored_states.append(node.state)

        if node.state == goal:
            print("hurrahhh")
            s = node
            #print(node.action[1:])
            markWay(node.action[1:])
            break

        else:
            for state in neighbours(node.state):
                if state not in explored_states:
                    frontier.add(Node(state =state , parent=node.state, action = node.action+[node.state]))
                    all_nodes.append(Node(state =state , parent=node.state, action = None))

def neighbours(state):
        r, c = state
        #print(r,c)
        l = [(r + 1, c),(r - 1, c),(r, c + 1),(r, c - 1)]
        r = []
        #print(l)
        for k in range(4):
            i = l[k][0]
            j = l[k][1]
            #print(i,j)
            if j >=0 and i<len(Mines) and i>=0 and j<len(Mines[0]):
                if walls[i][j] == False:
                    r.append(l[k])
            else:
                pass
        #print(r)
        return r

def markWay(l):
    Mines[0][0] = '* '
    for i in l:
        Mines[i[0]][i[1]] = '* '
    print(Mines)
solve()