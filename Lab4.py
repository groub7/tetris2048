from StdDraw import stddraw as StdDraw
import random
from Circle import Circle


def canvas():
    canvas_width = 900
    canvas_height = 900
    StdDraw.setCanvasSize(canvas_width, canvas_height)
    StdDraw.setXscale(0, 1)
    StdDraw.setYscale(0, 1)


class Lab4:
    def __init__(self):
        pass

    def main(self):
        canvas()
        StdDraw.clear()
        circle_number = 250
        circles = list()
        rMin = 0.01
        rMax = 0.2
        while len(circles) != circle_number:
            r = rMin + (rMax - rMin) * random.random()
            x = r + (1 - 2 * r) * random.random()
            y = r + (1 - 2 * r) * random.random()
            new_circle = Circle(x, y, r)

            overlap = False

            for i in range(0, len(circles)):
                if new_circle.distance(circles[i]) < (new_circle.r + circles[i].r):
                    overlap = True
                    break

            if overlap:
                continue

            circles.append(new_circle)
            new_circle.draw()
        StdDraw.show()

    if __name__ == '__main__':
        main()
