import pymunk
import pygame
import Images

pygame.init()


class BasketallRing:
    """
    class used to represent the basketball net
    """

    def __init__(self, space, win, x, y, width, height, collision_type=2):
        """

        :param space: pymunk.space
            the space the net will be on
        :param win: pygame.display
            the display the net will visual on
        :param x: float
            the x position the net will be on
        :param y: float
            the y position the net will be be on
        :param width: float
            the width of the net
        :param height: float
            the height of the net
        :param collision_type:
            the collision type of the net shape; default = 2
        """
        self.win = win
        self.space = space
        self.width = width
        self.height = height
        self.x = x
        self.y = y

        self.shape = pymunk.Poly.create_box(None, (
            self.width, self.height))  # creating rectangle shape which the net will be on
        poly_moment = pymunk.moment_for_poly(1, self.shape.get_vertices())
        poly_body = pymunk.Body(1, poly_moment, body_type=pymunk.Body.KINEMATIC)  # creating the body of the net
        self.shape.body = poly_body
        poly_body.position = x + width / 2, y + height / 2  # setting the position of the net body
        self.shape.filter = pymunk.ShapeFilter()
        self.shape.collision_type = collision_type
        self.shape.elasticity = 1
        self.space.add(poly_body, self.shape)  # adding the net to the space
        self.ring_surface = pygame.image.load('Images/basketball_ring.png')  # creating the net image surface
        self.ring_surface = pygame.transform.scale(self.ring_surface, (self.width, self.height))
        # transforming the net image into the right size

        self.firstX = poly_body.position[0]  # making it easier to reset the net position after moving
        self.direction = "right"  # making that when the basket net trap will trigger the net will move right

    def draw(self):
        """
         A function whose purpose is to to draw the net on the window
        """
        ring_rect = self.ring_surface.get_rect(
            center=(int(self.shape.body.position[0]), int(self.shape.body.position[1])))
        # placing the center of the net on the image center
        self.win.blit(self.ring_surface, ring_rect)  # displaying the net image on the screen

    def move_right_and_left(self, val=20, max_width=50):
        """
        A function whose purpose is to move the net right and left; that way it will be harder to score
        ------
        :param val: (float)
            the x velocity the net will move through; default - 20
        :param max_width: (float)
            the maximum width the net can reach when moving right or left through the x axis; default - 50
        """

        # if direction is right the net x velocity will be positive to make the net move with the x axis(right), else
        # it will be negative to make the net go against with the x axis(left)
        if self.direction == "right":
            self.shape.body.velocity = (val, 0)
        else:
            self.shape.body.velocity = (-val, 0)

        # checking if the net passed the maximus width he can reach, if so the direction will change
        if self.shape.body.position[0] < self.firstX - max_width:
            self.shape.body.velocity = (val, 0)
            self.direction = "right"
        elif self.shape.body.position[0] > self.firstX + max_width:
            self.shape.body.velocity = (-val, 0)
            self.direction = "left"

    def stop_and_reset(self):
        """
        A function whose purpose is to stop the net when moving and reset her position to his original
        """
        self.shape.body.position = (self.firstX, self.shape.body.position[1])
        self.shape.body.velocity = (0, 0)
        self.direction = "right"
