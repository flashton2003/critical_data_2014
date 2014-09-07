import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


a = [1, 2, 3, 4]
b = [5, 6, 7, 8]
c = [1, 2, 3, 4, 5]

ans = angle(a, c)
print ans