import math
import sys

from Field import *


class VirtualField:
    def __init__(self):
        self.tabs = True
        self.mode = True
        self.xShift = 200
        self.start = CoordMove(0, 0, 0, 0)
        self.lastMove = self.start
        self.pressed = False
        self.startSelected = False
        self.doneTimer = Timer(0)
        self.keyTimer = Timer(500)
        self.selected = FieldObject(0, 0, 0, 0, "")
        self.entries = []
        self.buttons = []
        self.lines = []
        self.moves = []
        self.textList = []
        self.mouseLine = (-1, -1)

        self.caption = "3D Test"
        self.screenX = 1400
        self.screenY = 800
        self.fov = 90
        self.origin = (0, 0, 0)

        self.preInit()
        self.init()
        self.postInit()

        self.mainLoop()

    def preInit(self):
        print("preinit")
        pygame.init()
        pygame.font.init()

        pygame.mouse.set_visible(False)
        self.font = pygame.font.SysFont("couriernew", 15)
        self.xtext = self.font.render("X: 0", True, (255, 255, 255))
        self.ytext = self.font.render("Y: 0", True, (255, 255, 255))
        self.display = pygame.display.set_mode((self.screenX, self.screenY))
        pygame.display.set_caption("Instruction Builder")

    def init(self):
        print("init")
        blue = (128, 128, 255)
        red = (255, 0, 0)
        self.field = Field((self.screenX / 2) - 288, (self.screenY / 2) + 288, 576, 576)

        self.buttons += [Button(20, self.screenY - 55, "Export", self.display)]
        self.buttons[0].run = self.export
        self.buttons += [Button(20, self.screenY - 145, "Target Mode", self.display)]
        self.buttons[1].run = self.switchMode

        # Game specific buttons
        self.buttons += [Button(20, self.screenY - 595, "Close Tabs", self.display)]
        self.buttons[2].run = self.switchTabs
        self.buttons += [Button(20, self.screenY - 370, "Sky Stones Red", self.display, color=red)]
        self.buttons[3].run = self.skyStonesRed
        self.buttons += [Button(20, self.screenY - 325, "Sky Stones Blue", self.display, color=blue)]
        self.buttons[4].run = self.skyStonesBlue
        self.buttons += [Button(20, self.screenY - 550, "Park Red 1", self.display, color=red)]
        self.buttons[5].run = self.parkR1
        self.buttons += [Button(20, self.screenY - 505, "Park Red 2", self.display, color=red)]
        self.buttons[6].run = self.parkR2
        self.buttons += [Button(20, self.screenY - 460, "Park Blue 1", self.display, color=blue)]
        self.buttons[7].run = self.parkB1
        self.buttons += [Button(20, self.screenY - 415, "Park Blue 2", self.display, color=blue)]
        self.buttons[8].run = self.parkB2
        # End game specific buttons

        self.entries += [Entry(20, self.screenY - 100, self.display, hint="Theta", height=28, width=150, default="0")]
        self.entries += [Entry(20, self.screenY - 235, self.display, hint="X-Offset", height=28, width=150, default="0",
                               visibility=False)]
        self.entries += [Entry(20, self.screenY - 190, self.display, hint="Y-Offset", height=28, width=150, default="0",
                               visibility=False)]
        self.entries += [Entry(self.buttons[0].x + self.buttons[0].w + 20, self.screenY - 55, self.display,
                               hint="Filename", height=28, width=150, default="output", numonly=False)]
        self.entries += [Entry(self.entries[0].x + self.entries[0].width + 20, self.entries[0].y, self.display,
                               hint="Speed", height=28, width=150, default=0.7, numonly=True)]

    def postInit(self):
        print("post init")
        self.field.addObject(FieldObject(0, 0, 24, 24, "red"), "r depot")
        self.field.addObject(FieldObject(120, 0, 24, 24, "blue"), "b depot")
        self.field.addObject(FieldObject(92, 0, 4, 48, "red"), "r sky stones")
        self.field.addObject(FieldObject(48, 0, 4, 48, "blue"), "b sky stones")
        self.field.addObject(FieldObject(78.25, 105.5, 18.5, 34.5, "red"), "r foundation")
        self.field.addObject(FieldObject(47.25, 105.5, 18.5, 34.5, "blue"), "b foundation")
        self.field.addObject(FieldObject(120, 120, 24, 24, "red"), "r build site")
        self.field.addObject(FieldObject(0, 120, 24, 24, "blue"), "b build site")
        self.field.addObject(FieldObject(96, 69.6, 48, 4.8, "red"), "r bridge")
        self.field.addObject(FieldObject(0, 69.6, 48, 4.8, "blue"), "b bridge")
        self.field.addObject(FieldObject(48, 67.2, 48, 9.6, "neutral"), "n bridge")

    def start(self):
        self.mainLoop()

    def draw(self):
        self.display.fill((0, 0, 0))

        white = (255, 255, 255)
        gray = (200, 200, 200)
        field = self.field

        for key in field.objects.keys():
            obj = field.objects[key]
            x, y = self.toScreenCoord(obj.x, obj.y)
            width = obj.width * 4
            length = obj.length * 4
            pygame.draw.polygon(self.display, obj.getColor(),
                                [(x, y), (x + width, y), (x + width, y - length), (x, y - length)])

        shift = self.xShift
        pygame.draw.line(self.display, gray, (field.x - shift + field.width / 6, field.y),
                         (field.x - shift + field.width / 6, field.y - field.length), 1)
        pygame.draw.line(self.display, gray, (field.x - shift + field.width / 3, field.y),
                         (field.x - shift + field.width / 3, field.y - field.length), 1)
        pygame.draw.line(self.display, gray, (field.x - shift + field.width / 2, field.y),
                         (field.x - shift + field.width / 2, field.y - field.length), 1)
        pygame.draw.line(self.display, gray, (field.x - shift - field.width / 3 + field.width, field.y),
                         (field.x - shift - field.width / 3 + field.width, field.y - field.length), 1)
        pygame.draw.line(self.display, gray, (field.x - shift - field.width / 6 + field.width, field.y),
                         (field.x - shift - field.width / 6 + field.width, field.y - field.length), 1)

        pygame.draw.line(self.display, gray, (field.x - shift, field.y - field.length / 6),
                         (field.x - shift + field.width, field.y - field.length / 6), 1)
        pygame.draw.line(self.display, gray, (field.x - shift, field.y - field.length / 3),
                         (field.x - shift + field.width, field.y - field.length / 3), 1)
        pygame.draw.line(self.display, gray, (field.x - shift, field.y - field.length / 2),
                         (field.x - shift + field.width, field.y - field.length / 2), 1)
        pygame.draw.line(self.display, gray, (field.x - shift, field.y + field.length / 3 - field.length),
                         (field.x - shift + field.width, field.y + field.length / 3 - field.length), 1)
        pygame.draw.line(self.display, gray, (field.x - shift, field.y + field.length / 6 - field.length),
                         (field.x - shift + field.width, field.y + field.length / 6 - field.length), 1)

        pygame.draw.polygon(self.display, white, [(field.x - shift, field.y), (field.x - shift + field.width, field.y),
                                                  (field.x - shift + field.width, field.y - field.length),
                                                  (field.x - shift, field.y - field.length)], 2)

        if not self.mouseLine[0] == -1:
            x = self.mouseLine[0]
            y = self.mouseLine[1]
            try:
                theta = math.radians(int(self.entries[0].getData()))
            except:
                theta = 0
            x1 = (36 * math.cos(theta)) + x
            y1 = y - (36 * math.sin(theta))
            pygame.draw.line(self.display, (255, 255, 255), (self.mouseLine[0], 0), (self.mouseLine[0], self.screenY),
                             1)
            pygame.draw.line(self.display, (255, 255, 255), (0, self.mouseLine[1]), (self.screenX, self.mouseLine[1]),
                             1)

            if self.startSelected:
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y - 36), (x - 30, y - 36))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y - 36), (x - 36, y - 30))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y + 36), (x - 30, y + 36))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y + 36), (x - 36, y + 30))
                pygame.draw.line(self.display, (255, 255, 255), (x + 36, y - 36), (x + 30, y - 36))
                pygame.draw.line(self.display, (255, 255, 255), (x + 36, y - 36), (x + 36, y - 30))
                pygame.draw.line(self.display, (255, 255, 255), (x + 36, y + 36), (x + 30, y + 36))
                pygame.draw.line(self.display, (255, 255, 255), (x + 36, y + 36), (x + 36, y + 30))
            else:
                pygame.draw.polygon(self.display, (255, 255, 128),
                                    [(x - 36, y - 36), (x + 36, y - 36), (x + 36, y + 36), (x - 36, y + 36)], 1)

            pygame.draw.line(self.display, (255, 0, 255), (x, y), (x1, y1), 1)
            pygame.draw.circle(self.display, (255, 0, 255), (int(x1), int(y1)), 3)

        if self.startSelected:
            x, y = self.toScreenCoord(self.start.x, self.start.y)
            pygame.draw.circle(self.display, (255, 255, 128), (x, y), 5)
            pygame.draw.polygon(self.display, (255, 255, 128),
                                [(x - 36, y - 36), (x + 36, y - 36), (x + 36, y + 36), (x - 36, y + 36)], 1)

        for line in self.lines:
            x, y = self.toScreenCoord(line[0][0], line[0][1])
            x1, y1 = self.toScreenCoord(line[1][0], line[1][1])
            pygame.draw.line(self.display, white, (x, y), (x1, y1), 1)

        for point in self.moves:
            if point == "closed" or point == "opened" or point == "redStones" or point == "blueStones":
                continue
            if point == self.moves[-1]:
                xy = self.toScreenCoord(point.x, point.y)
                pygame.draw.circle(self.display, (0, 128, 255), xy, 5)
            else:
                xy = self.toScreenCoord(point.x, point.y)
                pygame.draw.circle(self.display, white, xy, 5)

            # theta = math.radians(point.theta)
            # x1 = (36 * math.cos(theta)) + x
            # y1 = y - (36 * math.sin(theta))
            #
            # pygame.draw.line(self.display, (255, 0, 255), (x, y), (x1, y1), 1)
            # pygame.draw.circle(self.display, (255, 0, 255), (int(x1), int(y1)), 3)

        self.display.blit(self.xtext, (20, 20))
        self.display.blit(self.ytext, (20, 25 + self.xtext.get_height()))

        if self.doneTimer.check():
            self.buttons[0].text = self.font.render("Export", True, self.buttons[0].color)

        for button in self.buttons:
            button.draw()

        for entry in self.entries:
            entry.draw()

        i = 0
        for text in self.textList:
            self.display.blit(text, (self.screenX / 2 + 100, 20 * i))
            i += 1

        if not self.mode:
            s = self.selected
            if not s.alliance == "":
                x = s.x
                y = s.y
                w = s.width
                l = s.length

                x, y = self.toScreenCoord(x, y)
                w = w * 4
                l = l * 4

                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y - l - 36), (x - 30, y - l - 36))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y - l - 36), (x - 36, y - l - 30))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y + 36), (x - 30, y + 36))
                pygame.draw.line(self.display, (255, 255, 255), (x - 36, y + 36), (x - 36, y + 30))
                pygame.draw.line(self.display, (255, 255, 255), (x + w + 36, y - l - 36), (x + w + 30, y - l - 36))
                pygame.draw.line(self.display, (255, 255, 255), (x + w + 36, y - l - 36), (x + w + 36, y - l - 30))
                pygame.draw.line(self.display, (255, 255, 255), (x + w + 36, y + 36), (x + w + 30, y + 36))
                pygame.draw.line(self.display, (255, 255, 255), (x + w + 36, y + 36), (x + w + 36, y + 30))

    def mainLoop(self, stop=False):
        while not stop:
            down = pygame.key.get_pressed()
            if down[pygame.K_ESCAPE]:
                stop = True
            if not self.pressed:
                for entry in self.entries:
                    if entry.focus:
                        if down[pygame.K_BACKSPACE]:
                            self.pressed = True
                            entry.data = entry.data[:-1]
                        if down[pygame.K_0] or down[pygame.K_KP0]:
                            self.pressed = True
                            entry.data += "0"
                        if down[pygame.K_1] or down[pygame.K_KP1]:
                            self.pressed = True
                            entry.data += "1"
                        if down[pygame.K_2] or down[pygame.K_KP2]:
                            self.pressed = True
                            entry.data += "2"
                        if down[pygame.K_3] or down[pygame.K_KP3]:
                            self.pressed = True
                            entry.data += "3"
                        if down[pygame.K_4] or down[pygame.K_KP4]:
                            self.pressed = True
                            entry.data += "4"
                        if down[pygame.K_5] or down[pygame.K_KP5]:
                            self.pressed = True
                            entry.data += "5"
                        if down[pygame.K_6] or down[pygame.K_KP6]:
                            self.pressed = True
                            entry.data += "6"
                        if down[pygame.K_7] or down[pygame.K_KP7]:
                            self.pressed = True
                            entry.data += "7"
                        if down[pygame.K_8] or down[pygame.K_KP8]:
                            self.pressed = True
                            entry.data += "8"
                        if down[pygame.K_9] or down[pygame.K_KP9]:
                            self.pressed = True
                            entry.data += "9"

                if down[pygame.K_UP]:
                    pos = pygame.mouse.get_pos()
                    pygame.mouse.set_pos(pos[0], pos[1] - 1)
                    self.pressed = True
                if down[pygame.K_LEFT]:
                    pos = pygame.mouse.get_pos()
                    pygame.mouse.set_pos(pos[0] - 1, pos[1])
                    self.pressed = True
                if down[pygame.K_DOWN]:
                    pos = pygame.mouse.get_pos()
                    pygame.mouse.set_pos(pos[0], pos[1] + 1)
                    self.pressed = True
                if down[pygame.K_RIGHT]:
                    pos = pygame.mouse.get_pos()
                    pygame.mouse.set_pos(pos[0] + 1, pos[1])
                    self.pressed = True
                if down[pygame.K_z]:
                    self.textList = self.textList[:-1]
                    if len(self.moves) > 0:
                        move = self.moves[-1]
                        if not (move == "closed" or move == "opened" or move == "blueStones" or move == "redStones"):
                            self.lines = self.lines[:-1]
                        self.moves = self.moves[:-1]
                        self.pressed = True
                        if len(self.moves) > 0:
                            try:
                                i = 1
                                while (type(self.moves[-i]) == type("")):
                                    i += 1
                                self.lastMove = self.moves[-i]
                            except:
                                self.lastMove = self.start
                        else:
                            self.lastMove = self.start
                    elif self.startSelected:
                        self.startSelected = False
                        self.start = CoordMove(0, 0, 0, 0)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop = True
                elif event.type == pygame.KEYDOWN:
                    for entry in self.entries:
                        if entry.focus:
                            if event.key == pygame.K_BACKSPACE:
                                self.pressed = True
                                entry.data = entry.data[:-1]
                            else:
                                if entry.numonly:
                                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                                        self.pressed = True
                                        entry.data += "0"
                                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                                        self.pressed = True
                                        entry.data += "1"
                                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                                        self.pressed = True
                                        entry.data += "2"
                                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                                        self.pressed = True
                                        entry.data += "3"
                                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                                        self.pressed = True
                                        entry.data += "4"
                                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                                        self.pressed = True
                                        entry.data += "5"
                                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                                        self.pressed = True
                                        entry.data += "6"
                                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                                        self.pressed = True
                                        entry.data += "7"
                                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                                        self.pressed = True
                                        entry.data += "8"
                                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                                        self.pressed = True
                                        entry.data += "9"
                                    if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                                        self.pressed = True
                                        entry.data += "-"
                                    if event.key == pygame.K_PERIOD or event.key == pygame.K_KP_PERIOD:
                                        self.pressed = True
                                        entry.data += "."
                                else:
                                    self.pressed = True
                                    entry.data += event.unicode

                    if event.key == pygame.K_UP:
                        pos = pygame.mouse.get_pos()
                        pygame.mouse.set_pos(pos[0], pos[1] - 1)
                        self.pressed = True
                    if event.key == pygame.K_LEFT:
                        pos = pygame.mouse.get_pos()
                        pygame.mouse.set_pos(pos[0] - 1, pos[1])
                        self.pressed = True
                    if event.key == pygame.K_DOWN:
                        pos = pygame.mouse.get_pos()
                        pygame.mouse.set_pos(pos[0], pos[1] + 1)
                        self.pressed = True
                    if event.key == pygame.K_RIGHT:
                        pos = pygame.mouse.get_pos()
                        pygame.mouse.set_pos(pos[0] + 1, pos[1])
                        self.pressed = True
                    if event.key == pygame.K_z:
                        self.textList = self.textList[:-1]
                        if len(self.moves) > 0:
                            self.lastMove = self.moves[-1]
                            move = self.moves[-1]
                            if not (move == "closed" or move == "opened" or move == "blueStones" or move == "redStones"):
                                self.lines = self.lines[:-1]
                            self.moves = self.moves[:-1]
                            self.pressed = True
                            if len(self.moves) > 0:
                                try:
                                    i = 1
                                    while (type(self.moves[-i]) == type("")):
                                        i += 1
                                    self.lastMove = self.moves[-i]
                                except:
                                    self.lastMove = self.start
                            else:
                                self.lastMove = self.start
                        elif self.startSelected:
                            self.startSelected = False
                            self.start = CoordMove(0, 0, 0, 0)
                    self.keyTimer.reset()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        for button in self.buttons:
                            if button.check(x, y):
                                button.run()

                        for entry in self.entries:
                            if entry.check(x, y):
                                entry.focus = True
                            else:
                                entry.focus = False

                        if not self.mode:
                            for key in self.field.getObjects().keys():
                                obj = self.field.getObjects()[key]
                                if obj.check(x, y, self.screenX, self.screenY, self.xShift):
                                    self.selected = obj
                                    if self.startSelected:
                                        self.textList += [self.font.render(
                                            f"Target {len(self.moves) + 1}: ({key}, XOff: {self.entries[1].getData()}, YOff: {self.entries[2].getData()}, Theta: {self.entries[0].getData()}",
                                            True, (255, 255, 255))]
                                        try:
                                            centerX = obj.x + (obj.width // 2) + int(self.entries[1].getData())
                                            centerY = obj.y + (obj.length // 2) + int(self.entries[2].getData())
                                            if len(self.moves) != 0:
                                                x1 = self.lastMove.x
                                                y1 = self.lastMove.y
                                                self.lines += [[(centerX, centerY), (x1, y1)]]
                                            else:
                                                x1 = self.start.x
                                                y1 = self.start.y
                                                self.lines += [[(centerX, centerY), (x1, y1)]]
                                            self.moves += [TargetMove(obj, key, int(self.entries[1].getData()),
                                                                      int(self.entries[2].getData()),
                                                                      int(self.entries[0].getData()),
                                                                      float(self.entries[4].getData()))]

                                            self.lastMove = TargetMove(obj, key, int(self.entries[1].getData()),
                                                                       int(self.entries[2].getData()),
                                                                       int(self.entries[0].getData()),
                                                                       float(self.entries[4].getData()))
                                        except:
                                            print("error")

                        if self.mode:
                            x, y = self.toFieldCoord(x, y)

                            if 9 <= x <= 135 and 9 <= y <= 135:
                                if self.startSelected:
                                    self.textList += [self.font.render(
                                        f"Move {len(self.moves) + 1}: ({x}, {y}), Theta: {self.entries[0].getData()}", True,
                                        (255, 255, 255))]
                                    if self.countMoves() != 0:
                                        x1 = self.lastMove.x
                                        y1 = self.lastMove.y
                                        self.lines += [[(x, y), (x1, y1)]]
                                    else:
                                        x1 = self.start.x
                                        y1 = self.start.y
                                        self.lines += [[(x, y), (x1, y1)]]
                                    self.moves += [CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))]
                                    self.lastMove = CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))
                                else:
                                    self.start = CoordMove(x, y, int(self.entries[0].getData()), self.entries[4].getData())
                                    self.startSelected = True
                                    self.textList += [
                                        self.font.render(f"Robot Start: ({x}, {y}), Theta: {self.entries[0].getData()}",
                                                         True, (255, 255, 255))]
                                    self.lastMove = self.start

                elif event.type == pygame.MOUSEMOTION:
                    x, y = pygame.mouse.get_pos()
                    self.mouseLine = (x, y)
                    x, y = self.toFieldCoord(x, y)
                    if 0 <= x <= 144 and 0 <= y <= 144:
                        self.xtext = self.font.render(f"X: {x} inches", True, (255, 255, 255))
                        self.ytext = self.font.render(f"Y: {y} inches", True, (255, 255, 255))
                    else:
                        self.xtext = self.font.render(f"X: UNDEFINED", True, (255, 255, 255))
                        self.ytext = self.font.render(f"Y: UNDEFINED", True, (255, 255, 255))

            if self.keyTimer.check():
                self.pressed = False

            self.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def export(self):
        name = self.entries[3].getData()
        data = [f"s:{self.start.x},{self.start.y},{self.start.theta}"]
        prevMove = Move(self.start.x, self.start.y, self.start.theta, 0)
        for move in self.moves:

            # Check game specific stuff
            if move == "closed":
                data += ["tabs:0"]
                continue
            elif move == "opened":
                data += ["tabs:1"]
                continue
            elif move == "blueStones":
                data += ["stones:blue"]
                continue
            elif move == "redStones":
                data += ["stones:red"]
                continue

            if type(move) == type(CoordMove(0, 0, 0, 0)):
                x = prevMove.x - move.x
                y = prevMove.y - move.y
                t = prevMove.theta - move.theta
                d = (math.sqrt(math.pow(x, 2) + math.pow(y, 2)) / 24)
                time = d * 1/move.speed
                time += abs(t // 90)
                data += [f"c:{move.x},{move.y},{move.theta},{int(time * 1000)},{move.speed}"]
                prevMove = move
            else:
                x = prevMove.x - move.target.x
                y = prevMove.y - move.target.y
                t = prevMove.theta - move.theta
                time = math.sqrt(math.pow(x, 2) + math.pow(y, 2)) // 24
                time += (t // 90)
                if time == 0 and not(x == 0 or y == 0):
                    time = 1
                data += [f"t:{move.name},{move.xoffset},{move.yoffset},{move.theta},{int(time * 1000)},{move.speed}"]
                prevMove = move

        f = open("./outputs/" + name + ".field", "w")
        i = 0
        for str in data:
            i += 1
            if i == len(data):
                f.write(str)
                break
            f.write(str + "\n")

        self.buttons[0].text = self.font.render("Done!", True, self.buttons[0].color)
        self.doneTimer = Timer(1000)

    def switchMode(self):
        if self.mode:
            self.entries[1].visibility = True
            self.entries[2].visibility = True
            self.mode = not self.mode

            self.selected = FieldObject(0, 0, 0, 0, "")

            self.buttons[1].text = self.font.render("Coord Mode", True, self.buttons[1].color)
        else:
            self.entries[1].visibility = False
            self.entries[2].visibility = False
            self.mode = not self.mode

            self.buttons[1].text = self.font.render("Target Mode", True, self.buttons[1].color)

    def switchTabs(self):
        if self.tabs:
            self.buttons[2].text = self.font.render("Open Tabs", True, self.buttons[2].color)
            self.textList += [self.font.render(f"Tabs Closed", True, (255, 255, 255))]
            self.moves += ["closed"]
        else:
            self.buttons[2].text = self.font.render("Close Tabs", True, self.buttons[2].color)
            self.textList += [self.font.render(f"Tabs Opened", True, (255, 255, 255))]
            self.moves += ["opened"]

        self.tabs = not self.tabs

    def toScreenCoord(self, x, y):
        x = int(x * 4 + (self.screenX / 2 - 288) - self.xShift)
        y = int(-y * 4 + (self.screenY / 2 + 288))
        return x, y

    def toFieldCoord(self, x, y):
        x = (x - (self.screenX / 2 - 288) + self.xShift) / 4
        y = ((self.screenY / 2 + 288) - y) / 4
        return x, y

    def countMoves(self):
        t0 = 0
        for move in self.moves:
            if type(move) == type(CoordMove(0, 0, 0, 0)) or type(move) == type(TargetMove(FieldObject(0, 0, 0, 0, ""), "", 0, 0, 0, 0)):
                t0 += 1

        return t0

    # Game specific methods Below Here
    def skyStonesRed(self):
        print("red")
        self.textList += [self.font.render(f"Red SkyStones", True, (255, 255, 255))]
        self.moves += ["redStones"]

    def skyStonesBlue(self):
        print("blue")
        self.textList += [self.font.render(f"Blue SkyStones", True, (255, 255, 255))]
        self.moves += ["blueStones"]

    def parkR1(self):
        x, y = 132, 72
        if self.startSelected:
            self.textList += [self.font.render(
                f"Move {len(self.moves) + 1}: ({x}, {y}), Theta: {self.entries[0].getData()}", True,
                (255, 255, 255))]
            if self.countMoves() != 0:
                x1 = self.lastMove.x
                y1 = self.lastMove.y
                self.lines += [[(x, y), (x1, y1)]]
            else:
                x1 = self.start.x
                y1 = self.start.y
                self.lines += [[(x, y), (x1, y1)]]
            self.moves += [CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))]
            self.lastMove = CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))

    def parkR2(self):
        x, y = 108, 72
        if self.startSelected:
            self.textList += [self.font.render(
                f"Move {len(self.moves) + 1}: ({x}, {y}), Theta: {self.entries[0].getData()}", True,
                (255, 255, 255))]
            if self.countMoves() != 0:
                x1 = self.lastMove.x
                y1 = self.lastMove.y
                self.lines += [[(x, y), (x1, y1)]]
            else:
                x1 = self.start.x
                y1 = self.start.y
                self.lines += [[(x, y), (x1, y1)]]
            self.moves += [CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))]
            self.lastMove = CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))

    def parkB1(self):
        x, y = 12, 72
        if self.startSelected:
            self.textList += [self.font.render(
                f"Move {len(self.moves) + 1}: ({x}, {y}), Theta: {self.entries[0].getData()}", True,
                (255, 255, 255))]
            if self.countMoves() != 0:
                x1 = self.lastMove.x
                y1 = self.lastMove.y
                self.lines += [[(x, y), (x1, y1)]]
            else:
                x1 = self.start.x
                y1 = self.start.y
                self.lines += [[(x, y), (x1, y1)]]
            self.moves += [CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))]
            self.lastMove = CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))

    def parkB2(self):
        x, y = 36, 72
        if self.startSelected:
            self.textList += [self.font.render(
                f"Move {len(self.moves) + 1}: ({x}, {y}), Theta: {self.entries[0].getData()}", True,
                (255, 255, 255))]
            if self.countMoves() != 0:
                x1 = self.lastMove.x
                y1 = self.lastMove.y
                self.lines += [[(x, y), (x1, y1)]]
            else:
                x1 = self.start.x
                y1 = self.start.y
                self.lines += [[(x, y), (x1, y1)]]
            self.moves += [CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))]
            self.lastMove = CoordMove(x, y, int(self.entries[0].getData()), float(self.entries[4].getData()))
