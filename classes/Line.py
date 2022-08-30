import pymunk
import pygame

pygame.init()


class Line:
    """
    A class used to represent a line
    """

    def __init__(self, space, win, p1, p2, stroke, color=(0, 0, 0), collision_type=0):
        """

        :param space: pymunk.space
            the space the line will be on
        :param win: pygame.display
            the display the line will visual on
        :param p1: (float, float)
            the starting position of the line
        :param p2: (float, float)
            the ending position of the line
        :param stroke: int
            the stroke of the line
        :param color: (int, int, int)
            the color of the line; default = (0, 0, 0) (white)
        :param collision_type:
            the collision type of the line shape; default = 0
        """
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.stroke = stroke
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)  # creating the body of the line
        self.shape = pymunk.Segment(self.body, p1, p2, stroke)  # creating the shape of the line
        self.shape.elasticity = 1
        self.shape.collision_type = collision_type
        self.win = win
        self.space = space
        self.space.add(self.body, self.shape)  # adding the line to the space

        self.firstX = 0  # making it easier if needed to reset the line place after moving
        self.direction = "right"  # making that if the basket net trap will trigger the line will move right

    def draw(self):
        """
        A function whose purpose is to to draw the line on the window
        """
        pygame.draw.line(self.win, self.color, (self.shape.a.x + self.body.position[0], self.shape.a.y),
                         (self.shape.b.x + + self.body.position[0], self.shape.b.y), self.stroke)  # drawing the line on the screen
        # with the line parameters

    def move_right_and_left(self, val=20, max_width=50):
        """
        A function whose purpose is to move the line right and left; that way it will be harder to score
        ------
        :param val: (float)
            the x velocity the line will move through; default - 20
        :param max_width: (float)
            the maximum width the line can reach when moving right or left through the x axis; default - 50
        """

        # if direction is right the line x velocity will be positive to make the line move with the x axis(right), else
        # it will be negative to make the line go against with the x axis(left)
        if self.direction == "right":
            self.body.velocity = (val, 0)
        else:
            self.body.velocity = (-val, 0)

        # checking if the line passed the maximus width he can reach, if so the direction will change
        if self.body.position[0] < self.firstX - max_width:
            self.body.velocity = (val, 0)
            self.direction = "right"
        elif self.body.position[0] > self.firstX + max_width:
            self.body.velocity = (-val, 0)
            self.direction = "left"

    def stop_and_reset(self):
        """
        A function whose purpose is to stop the line when moving and reset his position to her original
        """
        self.body.position = (self.firstX, self.body.position[1])
        self.body.velocity = (0, 0)
        self.direction = "right"
