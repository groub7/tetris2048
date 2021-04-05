# A class for representing a point as a location in 2D space
class Point:
   # constructor that creates a point at the given (x, y) location
   # default values for the given location are set as x = 0 and y = 0
   def __init__(self, x = 0, y = 0):
      self.x = x
      self.y = y

   # moves this point by dx along the x axis and by dy along the y axis
   def translate(self, dx, dy):
      self.x += dx
      self.y += dy

   # moves this point to a given location (x, y)
   def move(self, x, y):
      self.x = x
      self.y = y
