import math
class MathAuxiliary(object):
    @staticmethod
    def AddVector3(vec1, vec2):
        return [vec1[0]+vec2[0], vec1[1]+vec2[1], vec1[2]+vec2[2]]

    @staticmethod
    def Distance(vec1, vec2):
        return math.sqrt((vec1[0]-vec2[0])**2+(vec1[1]-vec2[1])**2+(vec1[2]-vec2[2])**2)
