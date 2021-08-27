#Author: Brett Peters <bsp8649>
#HW2-P for class Intro to AI
import sys
import math
import random
from PIL import Image

class Node:
    def __init__(self, xValue = None, yValue = None, zValue = None, terrain = None):
        self.x = xValue
        self.y = yValue
        self.z = zValue
        self.terrain = terrain
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None
        self.flagpath = False
    def getX(self):
        return self.x
    def getY(self):
        return self.y

def getNeighbors(node, nodes):
    x = node.x
    y = node.y
    neighbors = []
    if node.x > 0:
        neighbors.append(nodes[x-1, y])
    if node.y > 0:
        neighbors.append(nodes[x, y-1])
    if node.x < (394):
        neighbors.append(nodes[x+1, y])
    if node.y < (499):
        neighbors.append(nodes[x, y+1])
    random.shuffle(neighbors)
    return neighbors

def createNodes(terrainImg, elevationLines):
    img = Image.open(terrainImg)
    rgb = img.convert("RGB")
    nodes = {}
    for y in range(500):
        elevations = elevationLines[y].split()
        for x in range(395):
            z = float(elevations[x])
            terrain = rgb.getpixel((x, y))
            node = Node(x, y, z, terrain)
            nodes[x,y] = node
    return nodes



def drawMap(nodes, outputImg):
    img = Image.new('RGB', (395, 500), "black")
    pixels = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            node = nodes[x,y]
            pixels[x, y] = node.terrain
    img.show()
    img.save(outputImg)

def getDistance(node1, node2):
    x1 = float(node1.x) * 10.29
    x2 = float(node2.x) * 10.29
    y1 = float(node1.y) * 7.55
    y2 = float(node2.y) * 7.55
    z1 = float(node1.z)
    z2 = float(node2.z)
    dist = math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
    return dist

def detectWater(nodes):
    edges = []
    for y in range(500):
        for x in range(395):
            if nodes[x, y].terrain == (0, 0, 255):
                shore = False
                for neighbor in getNeighbors(nodes[x,y], nodes):
                    if neighbor.terrain != (0, 0, 255) and neighbor.terrain != (130, 130, 255):
                        shore = True
                if shore == True:
                    nodes[x,y].terrain = (130, 130, 255)
                    edges.append(nodes[x,y])
    while edges:
        edge = edges.pop(0)
        icing(edge, nodes, 0)

def icing(node, nodes, count):
    if count > 6:
        return
    else:
        node.terrain = (130, 130, 255)
        for neighbor in getNeighbors(node, nodes):
            if neighbor.terrain == (0, 0, 255):
                icing(neighbor, nodes, count + 1)

def detectMud(nodes):
    water = []
    for y in range(500):
        for x in range(395):
            if nodes[x, y].terrain == (0, 0, 255):
                water.append(nodes[x,y])
    while water:
        pixel = water.pop(0)
        well = pixel.z
        drown(pixel, nodes, 0, well)
    return

def drown(node, nodes, count, well):
    if count > 3:
        return
    else:
        for neighbor in getNeighbors(node, nodes):
            if neighbor.terrain == (0,0,255):
                drown(neighbor, nodes, count+1, neighbor.z)
            else:
                if (neighbor.z - node.z) < 1:
                    neighbor.terrain = (140, 140, 20)
                drown(neighbor, nodes, count+1, well)



def aStar(startX, startY, endX, endY, nodes, season):
    startNode = nodes[startX, startY]
    endNode = nodes[endX,endY]
    visited = set()
    startNode.h = getDistance(startNode, endNode)
    startNode.f = startNode.h
    startNode.parent = None
    unvisited = set()
    unvisited.add(startNode)
    while unvisited:
        currentNode = sorted(unvisited, key=lambda inst:inst.f)[0]
        if (currentNode == endNode):
            drawPath(currentNode, nodes)
            break
        unvisited.remove(currentNode)
        visited.add(currentNode)
        for neighbor in getNeighbors(currentNode, nodes):
            if neighbor not in visited:
                cost = (getDistance(currentNode, neighbor) * terrainFactor(currentNode.terrain, season))
                g = currentNode.g + cost
                if (neighbor.g > g or neighbor.g == 0):
                    neighbor.g = g
                neighbor.h = getDistance(neighbor, endNode)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = currentNode
                if neighbor not in unvisited:
                    unvisited.add(neighbor)

def drawPoints(x1, y1, nodes):
    lowx = x1-3
    lowy = y1-3
    highx = x1+3
    highy = y1+3
    for i in range(lowx, highx):
        for j in range(lowy, highy):
            nodes[i, j].terrain = (120,0,200)



def drawPath(endNode,nodes):
    node = endNode
    while (node.parent != None):
        for i in range(node.x - 1, node.x + 1):
            for j in range(node.y - 1, node.y + 1):
                nodes[i,j].flagpath = True
        node = node.parent
    return

def terrainFactor(terrain, season):
    if (terrain == (71,51,3)):
        return 1
    if (terrain == (0,0,0)):
        return 1.1
    elif (terrain == (248,148,18)):
        return 1.5
    elif (terrain == (255,255,255)):
        if (season == 'fall'):
            return 4
        return 2
    elif (terrain == (2,208,60)):
        return 2.6
    elif (terrain == (255,192,0)):
        return 3
    elif (terrain == (2,136,40)):
        return 4
    elif (terrain == (5,73,24)):
        return 50
    elif (terrain == (0,0,255)):
        return 100
    elif (terrain == (130,130,255)):
        return 2
    elif (terrain == (140,140,20)):
        return 30
    else:
        return 100000

def flagPath(nodes):
    for i in range(0, 395):
            for j in range(0, 500):
                node = nodes[i,j] 
                if node.flagpath == True:
                    node.terrain = (40, 25, 120)

if __name__ == '__main__':
    terrainImg = sys.argv[1]
    elevationFile = sys.argv[2]
    pathFile = sys.argv[3]
    season = sys.argv[4]
    outputImg = sys.argv[5]
    with open(elevationFile, 'r') as f:
        elevationLines = f.read().splitlines()
        f.close()
    with open (pathFile, 'r') as p:
        pathLines = p.read().splitlines()
        p.close
    nodes = createNodes(terrainImg, elevationLines)
    if(season == 'winter'):
        detectWater(nodes)
    if(season == 'spring'):
        detectMud(nodes)
    for r in range(0, len(pathLines) - 1):
        (x1, y1) = pathLines[r].split()
        (x2, y2) = pathLines[r+1].split()
        aStar(int(x1), int(y1), int(x2), int(y2), nodes, season)
    flagPath(nodes)
    for r in range(0, len(pathLines) - 1):
        (x1, y1) = pathLines[r].split()
        (x2, y2) = pathLines[r+1].split()
        drawPoints(int(x1), int(y1), nodes)
    drawMap(nodes, outputImg)
