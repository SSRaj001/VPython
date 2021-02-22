from vpython import *
import sys
MAX_INT = sys.maxsize

class graph:
    def __init__(self,vert):
        self.verList = []
        self.vertices = vert
        self.matrix = [[0 for column in range(self.vertices)] for row in range(self.vertices)]
        self.matrixDir = [[0 for column in range(self.vertices)] for row in range(self.vertices)]
        self.arrows = {}
        self.cylinder = {}
        self.directed = True

    def addVertices(self):
        ev = scene.waitfor('click')
        temp = sphere(pos = ev.pos, radius = 0.1,color = color.blue)
        self.verList.append(temp)
        print(ev.pos)
        
    def lengthbtwn(self,X,Y):
        return ((X.x-Y.x)**2 + (X.y-Y.y)**2)**(1/2)
    
    def addEdges(self):
        ev = scene.waitfor('click')
        hit1 = scene.mouse.pick
        hit1.color = color.green
        ev = scene.waitfor('click')
        hit2 = scene.mouse.pick
        hit2.color = color.green
        for i in range(self.vertices):
            if self.verList[i] == hit1:
                src = i
            if self.verList[i] == hit2:
                dest = i
        len = self.lengthbtwn(hit1.pos,hit2.pos)
        self.matrix[src][dest] = len
        self.matrixDir[src][dest], self.matrixDir[dest][src]  = len, len
        arrowTarget = arrow(pos=hit1.pos,axis=vector(-(hit1.pos.x-hit2.pos.x),-(hit1.pos.y-hit2.pos.y),0),color = color.yellow,shaftwidth = 0.04)
        cylinderTarget = cylinder(pos=hit1.pos,axis=vector(-(hit1.pos.x-hit2.pos.x),-(hit1.pos.y-hit2.pos.y),0),color = color.yellow,radius = 0.03,visible=False)
        self.arrows[(src,dest)] = arrowTarget
        self.cylinder[(src,dest)] = cylinderTarget
        print(len)
        hit1.color, hit2.color = color.blue,color.blue
    
    def selectVert(self):
        ev = scene.waitfor('click')
        hit1 = scene.mouse.pick
        hit1.color = color.green
        ev = scene.waitfor('click')
        hit2 = scene.mouse.pick
        hit2.color = color.green
        for i in range(self.vertices):
            if self.verList[i] == hit1:
                src = i
            if self.verList[i] == hit2:
                dest = i
        hit1.color = color.blue
        hit2.color = color.blue
        return src,dest

    def getAdjMatrix(self):
        return self.matrix
        
    def findArrow(self,src,dst):
        self.arrows[(src,dst)].color = color.blue
    
    def backtrackPath(self,a,dst):
        self.resetColors(color.yellow)
        pathArr = []
        current = dst
        while(current != -1):
            pathArr.append(current)
            current = a[current]
        self.verList[pathArr[0]].color = color.red
        for i in range(len(pathArr)-1):
            if(pathArr[i]!=pathArr[0]):
                self.verList[pathArr[i]].color = color.green
            sleep(1)
            self.findArrow(pathArr[i+1],pathArr[i])
            sleep(1)
        sleep(1)        
        self.verList[pathArr[-1]].color = color.blue
        scene.title = "<h2>Select the respective buttons for mst and shortest path</h2>"
        pathArr = pathArr[::-1]
        print(pathArr)
    
    def minDistance(self, dist,visited):
        min = MAX_INT
        min_index = -1
        for ver in range(self.vertices):
            if dist[ver] < min and visited[ver] == False:
                min = dist[ver]
                min_index = ver
        return min_index
    
    def dijkstra(self,src,dst):
        parentArr = [-1]*self.vertices        
        dist = [MAX_INT]*self.vertices
        dist[src] = 0
        visited = [False]*self.vertices
        
        for _ in range(self.vertices):
            u = self.minDistance(dist,visited)
            if( u != -1 ):
                self.verList[u].color = color.white
                visited[u] = True
                for ver in range(self.vertices):
                    if(visited[ver] == False):
                        self.verList[ver].color = color.white
                    sleep(1)
                    if(self.matrix[u][ver] > 0 and visited[ver] == False and dist[ver] > dist[u]+self.matrix[u][ver]):
                        dist[ver] = dist[u]+self.matrix[u][ver]
                        parentArr[ver] = u
                    if(visited[ver] == False):
                        self.verList[ver].color = color.blue
                sleep(1)
                self.verList[u].color = color.yellow
        print(dist)
        print(parentArr)
        self.backtrackPath(parentArr,dst)
        
    def findEdges(self,edges):
        self.resetColors(color.yellow)
        sleep(1)
        for elem in edges:
            sleep(1)
            if elem in self.cylinder.keys():
                self.cylinder[elem].color = color.blue
            else:
                self.cylinder[(elem[1],elem[0])].color = color.blue
        scene.title = "<h2>Select the respective buttons for mst and shortest path</h2>"
    
    def backtrackMST(self,a):
        edgeList = []
        sum = 0
        print("Edges are : ",end="")
        for i in range(1,self.vertices):
            edgeList.append((a[i],i))
            print(a[i],i,sep="<->",end=" ")
            sum += self.matrixDir[i][a[i]]
        print("Total Length :",sum)
        self.findEdges(edgeList)
            
    
    def prims(self):
        parentArr = [None]*self.vertices    
        dist = [MAX_INT]*self.vertices
        dist[0],parentArr[0] = 0,-1
        visited = [False]*self.vertices
        
        for _ in range(self.vertices):
            u = self.minDistance(dist,visited)
            if( u != -1 ):
                self.verList[u].color = color.white
                visited[u] = True
                for ver in range(self.vertices):
                    if(visited[ver] == False):
                        self.verList[ver].color = color.white
                    sleep(1)
                    if(self.matrixDir[u][ver] > 0 and visited[ver] == False and dist[ver] > self.matrixDir[u][ver]):
                        dist[ver] = self.matrixDir[u][ver]
                        parentArr[ver] = u
                    if(visited[ver] == False):
                        self.verList[ver].color = color.blue
                sleep(1)
                self.verList[u].color = color.yellow
        print(dist)
        print(parentArr)
        self.backtrackMST(parentArr)
        
    def resetColors(self,col = color.blue):
        if(self.directed):
            for elem in list(self.arrows.keys()):
                self.arrows[elem].color = color.yellow
        else:
            for elem in list(self.cylinder.keys()):
                self.cylinder[elem].color = color.yellow
        for elem in self.verList:
            elem.color = col

    def changeGraph(self):
        self.resetColors()
        if(self.directed):
            for elem in list(self.arrows.keys()):
                self.arrows[elem].visible = False
                self.cylinder[elem].visible = True
        else:
            for elem in list(self.arrows.keys()):
                self.arrows[elem].visible = True
                self.cylinder[elem].visible = False

        self.directed = not self.directed

    def primsHelper(self):
        buttonDij.visible = False
        buttonPrim.visible = False
        self.resetColors()
        if(self.directed):
            self.changeGraph()
        self.prims()
        buttonDij.visible = True
        buttonPrim.visible = True

    def dijkstraHelper(self):
        buttonDij.visible = False
        buttonPrim.visible = False
        scene.title = "<h2> select source and destination</h2>"
        self.resetColors()
        if(not self.directed):
            self.changeGraph()
        src,dst = self.selectVert()
        self.dijkstra(src,dst)
        buttonDij.visible = True
        buttonPrim.visible = True


if __name__ == "__main__":
    sp1 = sphere(pos = vector(1,0,0),radius = 0, color = color.blue)
    n = int(input("Enter the No of Vertices : "))
    scene.title="<h2>Select the vertices in the scene</h2>"
    g = graph(n)
    for _ in range(n):
        g.addVertices()
    m = n*n 
    sleep(0.1)
    scene.title="<h2>Select the source and destination nodes to form an edge</h2>"
    while(m > n*(n-1)):
        m = int(input("Enter the No of Edges (Less Than Or Equal To {}) : ".format((n*(n-1))//1)))
    for _ in range(m):
        g.addEdges()
    print(g.getAdjMatrix())  
    buttonDij = button(bind=g.dijkstraHelper, text='Shortest Path')
    scene.title="<h2>Select the respective buttons for mst and shortest path</h2>"
    buttonPrim = button(bind=g.primsHelper, text='Min Span Tree')