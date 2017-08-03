import math
import random


def vector3_normalize(v):
    s = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    return [x / s for x in v]


def vector3_inner_product(v, num):
    if len(v) != 3:
        print "vector3_inner_product error"
        return None
    return [num * x for x in v]


def vector3_add(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print "vector3_add error"
        return None
    return [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]


def vector2_distance(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        print "vector2_distance error"
        return None
    s = (v1[0] - v2[0])**2 * (v1[1] - v2[1])**2
    return math.sqrt(s)


def vector3_distance(v1, v2):
    if len(v1) != 3 or len(v2) != 3:
        print "vector3_distance error"
        return None
    s = 0
    for i in xrange(0, 3):
        s += (v1[i] - v2[i])**2
    return math.sqrt(s)


def vector3_equal(v1, v2):
    if math.fabs(v1[0] - v2[0]) > 1e-5:
        return False
    if math.fabs(v1[1] - v2[1]) > 1e-5:
        return False
    if math.fabs(v1[2] - v2[2]) > 1e-5:
        return False
    return True


def get_random_index_with_distribution(distribution):
    x = random.random()
    cnt = 0.0
    for i, d in enumerate(distribution):
        cnt += d
        if x < cnt:
            return i
