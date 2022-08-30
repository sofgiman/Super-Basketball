import pymunk
import pygame

pygame.init()


class Rectangale:
    """
    A class used to represent a rectangle, pretending more like a sensor which check uf the ball went through the net
    """

    def __init__(self, space, win, x, y, width, height, collision_type=3, color=(255, 100, 255)):
        """

        :param space: pymunk.space
            the space the rect will be on
        :param win: pygame.display
            the display the rect will visual on
        :param x: float
            the x position the rect will be on
        :param y: float
            the y position the rect will be be on
        :param width: float
            the width of the rect
        :param height: float
            the height of the rect
        :param collision_type:
            the collision type of the rect shape; default = 3
        :param color: (int, int, int)
            the color of the line; default = (255, 100, 255) (pink)
        """
        self.color = color
        self.space = space
        self.win = win
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.shape = pymunk.Poly.create_box(None, (self.width, self.height))  # creating rectangle shape which the rect own
        poly_moment = pymunk.moment_for_poly(1, self.shape.get_vertices())
        poly_body = pymunk.Body(1, poly_moment, body_type=pymunk.Body.KINEMATIC)  # creating the body of the rect
        self.shape.body = poly_body
        self.shape.elasticity = 1
        poly_body.position = x + width / 2, y + height/2  # setting the position of the rect body
        self.shape.collision_type = collision_type
        self.space.add(poly_body, self.shape)  # adding the rect to the space

        self.firstX = poly_body.position[0]  # making it easier to reset the rect sensor position after moving
        self.direction = "right"  # making that when the basket net trap will trigger the rect will move right

    def draw(self):
        """
         A function whose purpose is to to draw the rect on the window
        """
        self.x = self.shape.body.position[0] - self.width/2
        pygame.draw.rect(self.win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move_right_and_left(self, val=20, max_width=50):
        """
        A function whose purpose is to move the rect sensor right and left when needed;
        that way it will be easier to find out when scored
        ------
        :param val: (float)
            the x velocity the rect will move through; default - 20
        :param max_width: (float)
            the maximum width the rect can reach when moving right or left through the x axis; default - 50
        """

        # if direction is right the rect x velocity will be positive to make the rect move with the x axis(right), else
        # it will be negative to make the rect go against with the x axis(left)
        if self.direction == "right":
            self.shape.body.velocity = (val, 0)
        else:
            self.shape.body.velocity = (-val, 0)

        # checking if the rect passed the maximus width he can reach, if so the direction will change
        if self.shape.body.position[0] < self.firstX - max_width:
            self.shape.body.velocity = (val, 0)
            self.direction = "right"
        elif self.shape.body.position[0] > self.firstX + max_width:
            self.shape.body.velocity = (- val, 0)
            self.direction = "left"

    def stop_and_reset(self):
        """
        A function whose purpose is to stop the rect when moving and reset her position to her original
        """
        self.shape.body.position = (self.firstX, self.shape.body.position[1])
        self.shape.body.velocity = (0, 0)
        self.direction = "right"
