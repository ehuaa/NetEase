# -*- coding: GBK -*-
from heapq import *

class MapData(object):
    def __init__(self):
        super(MapData, self).__init__()
        self.mapdataFilePath = './database/mapdata.dat'
        self.mapData = []

        self._loadFileData(self.mapdataFilePath)

        return

    def _loadFileData(self, path):
        f = open(path,'r')

        try:
            for line in f:
                lineList = list(line)
                lineList = self._charToInteger(lineList)
                self.mapData.append(lineList)
        except:
            raise

    def _charToInteger(self, lineList):
        data = []
        for c in lineList:
            try:
                data.append(int(c))
            except:
                pass
        return data

    def GetMaskData(self, pos):
        try:
            x,z = self._getMaskPosition(pos)
            msk = self.mapData[x][z]
            return msk
        except:
            return 1

    def _getMaskPosition(self, pos):
        x = int((pos[0] + 100)/1)
        z = int(-(pos[2] - 100)/1)

        x = x
        z = z

        return z,x

    def GetRealWorldPosition(self, x, z):
        rx = float(z + 3)*1-100
        rz = -float(x + 3)*1+100

        return [rx, 0, rz]


    def FindPathToPostion(self,start ,target):
        sx,sz = self._getMaskPosition(start)
        tx,ty = self._getMaskPosition(target)

        data = self._astar(self.mapData, (sx,sz), (tx,ty))

        return data


    def _heuristicfunc(self, a, b):
        return (b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2

    def _astar(self, array, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self._heuristicfunc(start, goal)}
        oheap = []

        heappush(oheap, (fscore[start], start))

        while oheap:

            current = heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + self._heuristicfunc(current, neighbor)
                if 0 <= neighbor[0] < len(array):
                    if 0 <= neighbor[1] < len(array[0]):
                        if array[neighbor[0]][neighbor[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + self._heuristicfunc(neighbor, goal)
                    heappush(oheap, (fscore[neighbor], neighbor))

        return None