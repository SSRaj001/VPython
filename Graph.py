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
        arrowTarget = arrow(pos=hit1.pos,axis=vector(-(hit1.pos.x-hit2.pos.x),-(hit1.pos.y-hit2.pos.y),0),color = color.orange,shaftwidth = 0.04)
        cylinderTarget = cylinder(pos=hit1.pos,axis=vector(-(hit1.pos.x-hit2.pos.x),-(hit1.pos.y-hit2.pos.y),0),color = color.orange,radius = 0.03,visible=False)
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
        print(src,dst)
        self.arrows[(src,dst)].color = color.red
    
    def backtrackPath(self,a,dst):
        pathArr = []
        current = dst
        while(current != -1):
            pathArr.append(current)
            current = a[current]
        pathArr = pathArr[::-1]
        print(pathArr)
        self.verList[pathArr[0]].color = color.cyan
        for i in range(len(pathArr)-1):
            sleep(0.1)
            self.findArrow(pathArr[i],pathArr[i+1])
            sleep(0.1)
            if(pathArr[i]!=pathArr[0]):
                self.verList[pathArr[i]].color = color.green
        sleep(0.1)        
        self.verList[pathArr[-1]].color = color.cyan
        
    
    def minDistance(self, dist,visited):
        min = MAX_INT
        min_index = -1
        for ver in range(self.vertices):
            if dist[ver] < min and visited[ver] == False:
                min = dist[ver]
                min_index = ver
        return min_index
    
    def dijkstra(self,src,dst):
        if(not self.directed):
            self.changeGraph()
        parentArr = [-1]*self.vertices        
        dist = [MAX_INT]*self.vertices
        dist[src] = 0
        visited = [False]*self.vertices
        
        for _ in range(self.vertices):
            u = self.minDistance(dist,visited)
            if( u != -1 ):
                visited[u] = True
                for ver in range(self.vertices):
                    if(self.matrix[u][ver] > 0 and visited[ver] == False and dist[ver] > dist[u]+self.matrix[u][ver]):
                        dist[ver] = dist[u]+self.matrix[u][ver]
                        parentArr[ver] = u 
        print(dist)
        print(parentArr)
        self.backtrackPath(parentArr,dst)
        
    def findEdges(self,edges):
        self.resetColors()
        for elem in edges:
            if elem in self.cylinder.keys():
                self.cylinder[elem].color = color.red
            else:
                self.cylinder[(elem[1],elem[2])].color = color.red
            sleep(0.1)

    
    def backtrackMST(self,a):
        edgeList = []
        sum = 0
        print("Edges are : ",end="")
        for i in range(1,self.vertices):
            edgeList.append((a[i],i))
            print(a[i],i,sep="<->")
            sum += self.matrixDir[i][a[i]]
        print("Total Length :",sum)
        self.findEdges(edgeList)
            
    
    def prims(self):
        if(self.directed):
            self.changeGraph()
        parentArr = [None]*self.vertices    
        parentArr[0] = -1
        dist = [MAX_INT]*self.vertices
        dist[0] = 0
        visited = [False]*self.vertices
        
        for _ in range(self.vertices):
            u = self.minDistance(dist,visited)
            if( u != -1 ):
                visited[u] = True
                for ver in range(self.vertices):
                    if(self.matrixDir[u][ver] > 0 and visited[ver] == False and dist[ver] > self.matrixDir[u][ver]):
                        dist[ver] = self.matrixDir[u][ver]
                        parentArr[ver] = u
                    
        print(dist)
        print(parentArr)
        self.backtrackMST(parentArr)
        
    def resetColors(self):
        if(self.directed):
            for elem in list(self.arrows.keys()):
                self.arrows[elem].color = color.orange
        else:
            for elem in list(self.cylinder.keys()):
                self.cylinder[elem].color = color.orange
        for elem in verList:
            elem.color = color.blue

        

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

    def dijkstraHelper(self):
        src,dst = self.selectVert()
        self.dijkstra(src,dst)

        
if __name__ == "__main__":
    sp1 = sphere(pos = vector(1,0,0),radius = 0, color = color.blue)
    n = int(input("Enter the No of Vertices : "))
    g = graph(n)
    for _ in range(n):
        g.addVertices()
    m = n*n 
    sleep(0.1)
    while(m > n*(n-1)/2):
        m = int(input("Enter the No of Edges (Less Than n*(n-1)/2) : "))
    for _ in range(m):
        g.addEdges()
    print(g.getAdjMatrix())  
    g.dijkstraHelper()
    g.prims()