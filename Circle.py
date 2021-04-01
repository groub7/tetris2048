from StdDraw import stddraw as StdDraw


class Circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        StdDraw.setPenColor(StdDraw.DARK_BLUE)
        StdDraw.setPenRadius(0.001)
        StdDraw.filledCircle(self.x, self.y, self.r)

    def distance(self, circle):
        return (((self.x - circle.x) ** 2) + (self.y - circle.y) ** 2) ** 0.5
