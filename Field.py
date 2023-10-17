import pygame
import time

class Field:
    def __init__(self, x, y, w, l):
        self.width = w
        self.length = l
        self.x = x
        self.y = y

        self.objects = {}

    def addObject(self, obj, name):
        self.objects[name] = obj

    def getObject(self, name):
        return self.objects[name]

    def getObjects(self):
        return self.objects

class FieldObject:
    def __init__(self, x, y, w, l, alliance):
        self.width = w
        self.length = l
        self.x = x
        self.y = y

        self.alliance = alliance

    def check(self, x, y, screenX, screenY, xShift):
        i = int(self.x * 4 + (screenX / 2 - 288) - xShift)
        j = int(-self.y * 4 + (screenY / 2 + 288))
        w = self.width * 4
        h = self.length * 4
        if i <= x <= i + w:
            if j - h <= y <= j:
                return True
        return False

    def getColor(self):
        if self.alliance == "red":
            return (255, 0, 0)
        elif self.alliance == "blue":
            return (0, 0, 255)
        else:
            return (255, 255, 0)

class Move:
    def __init__(self, x, y, theta, speed):
        self.x = x
        self.y = y
        self.theta = theta
        self.speed = speed

class CoordMove(Move):
    def __init__(self, x, y, theta, speed):
        super(CoordMove, self).__init__(x, y, theta, speed)

class TargetMove(Move):
    def __init__(self, target, name, xoffset, yoffset, theta, speed):
        super(TargetMove, self).__init__(target.x+(target.width/2) + xoffset, target.y+(target.length/2) + yoffset, theta, speed)
        self.xoffset = xoffset
        self.yoffset = yoffset
        self.target = target
        self.name = name
        self.speed = speed

class Button:
    def __init__(self, x, y, text, surface, font="couriernew", size=15, color=(255, 255, 255), visibility=True):
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, color)
        self.color = color
        self.x = x
        self.y = y
        self.w = self.text.get_width() + 10
        self.h = self.text.get_height() + 10

        self.surface = surface
        self.visibility = visibility

    def draw(self, thickness=2):
        if self.visibility:
            w, h = self.text.get_width() + 10, self.text.get_height() + 10
            pygame.draw.polygon(self.surface, self.color, [(self.x, self.y), (self.x + w, self.y),
                                                      (self.x + w, self.y + h), (self.x, self.y + h)], thickness)

            self.surface.blit(self.text, (self.x + 5, self.y + 5))

    def check(self, x, y):
        if self.x <= x <= self.x + self.text.get_width() + 10:
            if self.y <= y <= self.y + self.text.get_height() + 10:
                return True
        return False

class Entry:
    def __init__(self, x, y, surface, width=100, height=20, numonly=True, hint="", font="couriernew", size=15, focuscolor=(255, 255, 0), default="", color=(0, 255, 255), visibility=True):
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(hint, True, color)
        self.default = default
        self.data = ""
        self.focus = False
        self.color = color
        self.focuscolor = focuscolor
        self.surface = surface
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.visibility = visibility

        self.numonly = numonly

    def draw(self, thickness=2):
        if self.visibility:
            w, h = self.width, self.height
            if self.focus:
                pygame.draw.polygon(self.surface, self.focuscolor, [(self.x, self.y), (self.x + w, self.y),
                                                        (self.x + w, self.y + h), (self.x, self.y + h)], thickness)
            else:
                pygame.draw.polygon(self.surface, self.color, [(self.x, self.y), (self.x + w, self.y),
                                                        (self.x + w, self.y + h), (self.x, self.y + h)], thickness)
            if self.data == "" and not self.focus:
                self.surface.blit(self.text, (self.x + 5, self.y + 5))
            else:
                if self.focus:
                    text = self.font.render(self.data, True, self.focuscolor)
                    self.surface.blit(text, (self.x + 5, self.y + 5))
                else:
                    text = self.font.render(self.data, True, self.color)
                    self.surface.blit(text, (self.x + 5, self.y + 5))

    def check(self, x, y):
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.height:
                return True
        return False

    def addData(self, data):
        self.data += str(data)

    def getData(self):
        if self.data == "":
            return self.default
        else:
            return self.data

class Timer:
    def __init__(self, milliseconds):
        self.milliseconds = milliseconds
        self.time = time.time()*1000 + milliseconds

    def check(self):
        if time.time()*1000 >= self.time:
            return True
        return False

    def reset(self):
        self.time = time.time()*1000 + self.milliseconds
