
allNodes = {}


class Node:
    def __init__(self):
        self.connectedNode = {}
        self.order = 0
        self.distance = 0
        self.previous = None
        self.tempDis = 999999999
        self.tempPrev = None
        self.testedNode = []
        self.finished = False

    def addConnectedNode(self, node, dis):
        self.connectedNode[node] = dis

    def updateTempDis(self, nodeFrom, newDis):
        if newDis < self.tempDis:
            self.tempPrev = nodeFrom
        self.tempDis = min(newDis, self.tempDis)
        self.testedNode.append(nodeFrom)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


def findNode(node, order):
    node.distance = node.tempDis
    node.previous = node.tempPrev
    for connectedStr, nodeDis in node.connectedNode.items():
        connectedNode = allNodes[connectedStr]
        if connectedNode not in node.testedNode:
            connectedNode.updateTempDis(node, node.distance + nodeDis)
            node.testedNode.append(connectedNode)
    node.order = order
    node.finished = True


def findLowestNode():
    lowestNode = None
    lowestDis = 999999999999
    for nodeStr, node in allNodes.items():
        if node.finished:
            continue
        if node.tempDis < lowestDis:
            lowestNode = node
            lowestDis = node.tempDis
    return lowestNode


def findNodeStr(nodeFind):
    if nodeFind is None:
        return ""
    for nodeStr, node in allNodes.items():
        if node == nodeFind:
            return nodeStr
    return ""



while True:
    infoIn = input("Connection: ")
    if infoIn == "0":
        break
    try:
        nodeS, nodeE, dis = infoIn.split(" ")
        if nodeS not in allNodes:
            allNodes[nodeS] = Node()
        if nodeE not in allNodes:
            allNodes[nodeE] = Node()
        allNodes[nodeS].addConnectedNode(nodeE, int(dis))
        allNodes[nodeE].addConnectedNode(nodeS, int(dis))
    except:
        print("no")
        continue

allOrder = 1
nodeStart = input("Starting node: ")
allNodes[nodeStart].tempDis = 0
nodeEnd = input("End node: ")
while True:
    nodeSearch = findLowestNode()
    if nodeSearch is None:
        break
    findNode(nodeSearch, allOrder)
    allOrder += 1
totalDis = allNodes[nodeEnd].distance
path = [nodeEnd]
nodeLook = allNodes[nodeEnd]
while True:
    nStr = findNodeStr(nodeLook.previous)
    if nStr == "":
        break
    path.append(nStr)
    nodeLook = allNodes[nStr]
path.reverse()
print("Path: %s" % "".join(path))
print("Distance: %d" % totalDis)


