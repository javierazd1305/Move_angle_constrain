import cv2
import imutils
import numpy as np
import math
from math import atan2, degrees, pi, sin, cos, radians

img = np.zeros((600, 600, 3), np.uint8)
center = []
top = None
bot = None

# class circle


class IterRegistry(type):
    def __iter__(cls):
        return iter(cls.registry)


class Circle:
    next_id = 0
    __metaclass__ = IterRegistry
    registry = []

    def __init__(self, x, y):
        self.ident = Circle.next_id
        self.x = x
        self.y = y
        self.degrees = None
        self.registry.append(self)
        Circle.next_id += 1

    def setDegree(self, degree):
        self.degrees = degree


def getDegree(degree):
    return degree % 360


def radsDegree(dx, dy):
    rads = atan2(-dy, dx)
    rads %= 2 * pi
    degs = degrees(rads)
    return degs


def obtener_punto(event, x, y, flags, param):
    if event == 4:
        center = [x, y]
        if len(Circle.registry) < 2:
            print 'me'
            cv2.circle(img, (x, y), 5, (255, 0, 255), -1)
            Circle(x, y)
            if len(Circle.registry) == 2:
                dx = Circle.registry[-2].x - Circle.registry[-1].x
                dy = Circle.registry[-2].y - Circle.registry[-1].y
                degs = radsDegree(dx, dy)
                output = None
                if 180 <= degs < 360:
                    output = degs - 180
                elif 0 < degs < 180:
                    output = degs + 180
                elif degs == 360:
                    output = 180
                # print output
                Circle.registry[-1].setDegree(output)
        else:
            dx = (center[0] - Circle.registry[-1].x)
            dy = (center[1] - Circle.registry[-1].y)
            degs = radsDegree(dx, dy)
            # NEW CIRCLE (actual)
            Circle(x, y)
            Circle.registry[-1].setDegree(degs)

            # draw the circle and the link
            cv2.circle(img, (x, y), 7, (0, 255, 0), 1)
            cv2.line(img, (Circle.registry[-2].x, Circle.registry[-2].y),
                     (Circle.registry[-1].x, Circle.registry[-1].y), (0, 255, 255), 1)

            # get the last circle
            eval_degre = Circle.registry[-2].degrees

            # set delimiters
            abertura = 60
            top = eval_degre + abertura
            bot = eval_degre - abertura
            top = getDegree(top)
            bot = getDegree(bot)
            print bot, degs, top

            if (bot < top):
                if bot <= degs and degs <= top:
                    print 'correcto'
                    cv2.circle(img, (x, y), 7, (255, 255, 255), 1)
                else:
                    print 'eliminar'
                    Circle.registry.pop(-1)

            elif bot <= degs or degs <= top:
                print 'correcto'
                cv2.circle(img, (x, y), 7, (255, 255, 255), 1)
            else:
                print 'eliminar'
                Circle.registry.pop(-1)


while True:
    cv2.setMouseCallback('Frame', obtener_punto)
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
