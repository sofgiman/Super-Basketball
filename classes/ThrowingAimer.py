import pymunk
import pygame
import math
from pymunk.vec2d import Vec2d


pygame.init()

MAX_DISTANCE = 200  # the maximum length of the aimer


class ThrowingAimer:
    """
    A class used to represent the throwing intention of the ball; with it you can direct where the ball will go
    after throwing him
    """
    def __init__(self, win, p1, p2, stroke, thick_color=(10, 60, 230),
                 middle_color=(26, 145, 223), light_color=(123, 248, 251)):
        """
        :param win: pygame.display
            the display the aimer will visual on
        :param p1: (float, float)
            the starting position of the aimer( where is the ball)
        :param p2: (float, float)
            the ending position of the aimer( where the ball should go)
        :param stroke: int
            the stroke of the aimer line
        :param thick_color: (int, int, int)
            the first color of the aimer line, should be dark; default = (10, 60, 230) (blue)
        :param middle_color: (int, int, int)
            the middle color of the aimer line, should be between the dark and the light color; default =
            (26, 145, 223) (light blue)
        :param light_color: (int, int, int)
            the last color of the aimer line, should be lighter than the others; default = (123, 248, 251) (cyan)
        """

        self.p1 = p1
        if self.DistanceOverllap(p2):  # checking if the line will overlap it's maximum, if so the line will be at it's maximum
            self.p2 = self.fix_overllap_distance(p2)
        else:
            self.p2 = p2
        self.thick_color = thick_color
        self.middle_color = middle_color
        self.light_color = light_color
        self.strokes = []  # creating list of strokes, the first line will be have more stroke than the others
        if stroke < 3:
            self.strokes = [stroke, stroke, stroke]
        else:
            self.strokes = [stroke, stroke-1, stroke-1]

        self.stroke = stroke
        self.points = []  # creating a list of points; that way it's possible to divide to aimer line into 3 parts:
        # one is thicker, second is smaller, and last it the smallest one - to represent a better visual
        self.set_points()  # defining the points list
        self.colors = [thick_color, middle_color, light_color]  # defining the colors list

        self.win = win

    def draw(self):
        """
        A function whose purpose is to to draw the line aimer on the window
        """
        self.set_points()  # setting the points assuming they have been changed
        for index, color in enumerate(self.colors):  # drawing three lines using a loop to create the big line between the 2 points
            pygame.draw.line(self.win, color, self.points[index], self.points[index+1], self.strokes[index])

    def throw_ball(self, ball):
        """
        A function whose purpose is to to throw a ball
        ------
        :param ball: Ball
            take the ball and throw it towards the second point
        """
        ball.throw_ball(self.p2)

    def set_p1(self, p1):
        """
        A function whose purpose is to set p1
        ------
        :param p1: (float, float)
            the point that should p1 have; usually it's the basketball center
        """
        self.p1 = p1

    def set_p2(self, p2):
        """
        A function whose purpose is to set p2
        ------
        :param p2: (float, float)
            the point that should p2 have; usually it's the mouse center
        """
        if self.DistanceOverllap(p2):  # if the line between p1 and p2 is higher than max distance than p2 will
            # be closer to p1
            self.p2 = self.fix_overllap_distance(p2)  # making p2 closer to p1, that way the line between these points will be max
        else:
            self.p2 = p2

    def distance(self, p1, p2):
        """
        A function whose purpose is to return a distance between two points
        ------
        :param p1: (float, float)
            the first points
        :param p2: (float, float)
            the second points
        :return: float
            the distance between the two points
        """
        return math.sqrt(((p2[0] - p1[0]) ** 2) + ((p2[1] - p1[1]) ** 2))

    # return true if distance higher than max distance, else return false
    def DistanceOverllap(self, p2):
        """
        A function whose purpose is to check if the distance between p1 to p2 overlapping max distance, if so return True
        ------
        :param p2:
            the point to check the distance between her to p1
        :return: bool
            if the distance between p1 to p2 higher than max distance - return true
        """
        if self.distance(self.p1, p2) > MAX_DISTANCE:
            return True
        else:
            return False

    def fix_overllap_distance(self, p2):
        """
        A function whose purpose is to make that the distance between p1 to p2 will be a it's maximum;
        returning the x and y p2 needed in order to make the distance maximum.
        ------
        :param p2:
            the point to check that should changed
        :return: (float, float)
            the point that p2 should be to make the distance between her and p1 maximum
        """

        angle = Vec2d(p2[0] - self.p1[0], p2[1] - self.p1[1]).angle_degrees  # calculate the angle between the line that's
        # between the two points to the x positive axis; that way it's possible to calculate what p2 should be

        x = self.p1[0] + math.cos(math.radians(angle)) * MAX_DISTANCE  # calculating the x that p2 should have
        y = self.p1[1] + math.sin(math.radians(angle)) * MAX_DISTANCE  # calculating the y that p2 should have
        return x, y

    def set_points(self):
        """
        A function whose purpose is to set the points list that way:
        first point and fourth points stay the same( these are the one the big line is between)
        second and third point becomes between the others points; that way it's possible to divide the big line into 3 lines
        """
        p1 = self.p1
        p2 = self.p1[0] + (self.p2[0] - self.p1[0])*(2/9), self.p1[1] + (self.p2[1] - self.p1[1])*(2/9)  # calculating p2 on the lines list
        p3 = p2[0] + (self.p2[0] - self.p1[0])*(3/9), p2[1] + (self.p2[1] - self.p1[1])*(3/9)  # # calculating p3 on the lines list
        p4 = self.p2
        self.points = [p1, p2, p3, p4]
