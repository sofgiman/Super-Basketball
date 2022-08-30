import pymunk
import pygame

pygame.init()


class Block:
    """
    A class used to represent a block
    """
    def __init__(self, space, win, x, y, width, height, collosion_type=3, color=(255, 100, 255)):
        """
        :param space: pymunk.space
            the space the block will be on
        :param win: pygame.display
            the display the block will visual on
        :param x: float
            the x position the block will be on
        :param y: float
            the y position the block will be be on
        :param width: float
            the width of the block
        :param height: float
            the height of the block
        :param collosion_type: int
            the collision type of the block shape; default = 3
        :param color: (int, int, int)
            the color of the block; default = (255, 100, 255)
        """
        self.color = color
        self.space = space
        self.win = win
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.shape = pymunk.Poly.create_box(None, (self.width, self.height))  # creating the block shape
        poly_moment = pymunk.moment_for_poly(1, self.shape.get_vertices())
        poly_body = pymunk.Body(1, poly_moment, body_type=pymunk.Body.KINEMATIC)  # creating the block body
        self.shape.body = poly_body
        self.shape.elasticity = 1
        poly_body.position = x + width / 2, y + height/2
        self.shape.collision_type = collosion_type
        self.space.add(poly_body, self.shape)  # adding the block to the space

        self.firstY = poly_body.position[1]  # making it easier to reset the block position after moving
        self.direction = "up"  # making that when the block trap will trigger the block will move up
        self.on_space = True  # a bool who check if the block is on the space



    def draw(self):
        """
        A function whose purpose is to to draw the block on the window
        """
        self.y = self.shape.body.position[1] - self.height/2
        pygame.draw.rect(self.win, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def move_up_and_down(self, val=20, max_height=50):
        """
        A function whose purpose is to move the block up and down; that way it will be harder to score
        ------
        :param val: (float)
            the y velocity the block will move through; default - 20
        :param max_height: (float)
            the maximum height the block can reach when moving up or down through the y axis; default - 50
        """

        # if direction is up the block y velocity will be negative to make the block move against the y axis(up), else
        # it will be positive to make the block go with the y axis(down)
        max_height = 200
        if self.direction == "up":
            self.shape.body.velocity = (0, -val)
        else:
            self.shape.body.velocity = (0, val)

        # checking if the block passed the maximus height he can reach, if so the direction will change
        if self.shape.body.position[1] > self.firstY + max_height:
            self.shape.body.velocity = (0, -val)
            self.direction = "up"

        elif self.shape.body.position[1] < self.firstY - max_height:
            self.shape.body.velocity = (0, val)
            self.direction = "down"

    def remove_and_reset(self):
        """
        A function whose purpose is to to reset the block position and stop it, than remove it from the space.
        Call this function when you don't want block trap isn't triggered, or you want to reset the block position
        """
        self.shape.body.velocity = (0, 0)
        self.shape.body.position = (self.shape.body.position[0], self.firstY)
        self.space.remove(self.shape.body, self.shape)

    def display_block(self):
        """
        A function whose purpose is to to display the block on the space.
        Call this function when you want block trap to trigger
        """
        self.space.add(self.shape.body, self.shape)

    def set_pos(self, pos):
        """
        A function whose purpose is to move the block to be closer to given pos
        ------
        :param pos: (float, float)
            the pos that the block will be closer to, usually the center of the ball
        """
        self.x = pos[0] + 150
        self.y = pos[1] - 120
        if self.y < 50:
            self.y = 50

        self.firstY = self.y + self.height / 2  # you will use that when you want to reset the block position
        self.shape.body.position = (self.x + self.width / 2, self.y + self.height/2)

