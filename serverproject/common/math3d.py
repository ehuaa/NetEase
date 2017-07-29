import math
class Vector3d(object):
    def __init__(self, vec=[0,0,0]):
        super(Vector3d, self).__init__()
        self.x = vec[0]
        self.y = vec[1]
        self.z = vec[2]

    def __add__(self, other):
        ret = saiVector3d()
        ret.x = other.x + self.x
        ret.y = other.y + self.y
        ret.z = other.z + self.z
        return ret

    def __mul__(self, other):
        sum = 0
        sum += other.x * self.x
        sum += other.y * self.y
        sum += other.z * self.z
        return sum

    def __sub__(self, other):
        ret = saiVector3d()
        ret.x = self.x-other.x
        ret.y = self.y-other.y
        ret.z = self.z-other.z
        return ret

    def Length(self):
        return math.sqrt(self.x**2+self.y**2+self.z**2)

    def Normalize(self):
        length = self.Length()
        self.x = self.x/length
        self.y = self.y / length
        self.z = self.z / length

class MathAuxiliary(object):
    @staticmethod
    def AddVector3(vec1, vec2):
        return [vec1[0]+vec2[0], vec1[1]+vec2[1], vec1[2]+vec2[2]]

    @staticmethod
    def VectorLength(vec):
        return math.sqrt(vec[0]**2+vec[1]**2+vec[2]**2)

    @staticmethod
    def Distance(vec1, vec2):
        return math.sqrt((vec1[0]-vec2[0])**2+(vec1[1]-vec2[1])**2+(vec1[2]-vec2[2])**2)

    @staticmethod
    def LineHitSphere(rayOrigin, rayDirection, spherePosition, sphereRadius):
        tilt = MathAuxiliary.Distance(rayOrigin, spherePosition)
        angle = math.abs(math.asin(sphereRadius/tilt))

        v1 = Vector3d(spherePosition)
        v2 = Vector3d(rayOrigin)

        v = v1-v2
        v.Normalize()
        rv = Vector3d(rayDirection)
        rv.Normalize()

        val = math.abs(math.acos(v*rv))

        if angle > val:
            return True
        else:
            return False



