import pymunk
import pygame
import Images

pygame.init()


# A file whose purpose is to represent the ball class

class Ball:
    """
    A class used to represent a basketball
    """

    def __init__(self, space, win, x, y, radius, collosion_type=1):
        """
        Parameters
        ------
        :param space: pymunk.space
            the space the ball will be on
        :param win: pygame.display
            the display the ball will visual on
        :param x: float
            the x position the ball center will be on
        :param y: float
            the y position the ball center will be be on
        :param radius: float
            the radius of the ball
        :param collosion_type: int
            the collision type of the ball shape; default = 1
        """

        self.x = x
        self.y = y
        self.space = space
        self.win = win
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = x, y  # the ball body center position
        self.shape = pymunk.Circle(self.body, radius)  # creating the shape of the ball
        self.shape.density = 1  # the ball shape density
        self.shape.elasticity = 0.8  # the elasticity of the ball - made to make the ball drawn to the floor
        self.shape.filter = pymunk.ShapeFilter(categories=0b1)
        self.shape.collision_type = collosion_type  # ball shape will have a different collision type
        self.space.add(self.body, self.shape)  # adding the ball to the pymunk space

        self.basketball_surface = pygame.image.load('Images/basketballQ.png')  # creating the ball image surface
        self.basketball_surface = pygame.transform.scale(self.basketball_surface, (self.radius * 2, self.radius * 2))
        # transforming the image into the right size; the width and the height need to be 2 times bigger then the radius

        self.direction = "up"  # making that when the ball trap will trigger the ball will move up

    def draw(self):
        """
        A function whose purpose is to to draw the ball on the window
        """
        x, y = self.body.position

        basketball_rect = self.basketball_surface.get_rect(center=(int(x), int(y)))  # placing the center of the ball
        # on the image center
        self.win.blit(self.basketball_surface, basketball_rect)  # draw the ball on the screen

    def stop(self):
        """
        A function whose purpose is to to enable the ball from moving
        """
        self.body.body_type = pymunk.Body.STATIC  # with making the ball body type static the ball will be no able to move

    def continue_move(self):
        """
        A function whose purpose is to able the ball move around
        """
        self.body.body_type = pymunk.Body.DYNAMIC  # with making the ball body type dynamic the ball will be able to move

    # A function whose purpose is to se the velocity of the ball
    def set_velocity(self, vX=0, vY=0):
        """
        A function whose purpose is to se the velocity of the ball
        ------
        :param vX : float
            the x velocity the ball will have; default = 0
        :param vY: float
            the y velocity the ball will have; default = 0
        """

        self.body.velocity = vX, vY  # setting the ball velocity

    def throw_ball(self, moues_pos):
        """
        A function whose purpose is to throw the ball with a specific calculation using the mouse position
        ------
        :param moues_pos: (float, float)
            the position of the mouse 
        """
        x = 4.5 * (moues_pos[0] - self.body.position.x)
        # subtraction the mouse x pos with the ball x pos and multiply it to get the vX the ball will have
        y = 5.3 * (moues_pos[1] - self.body.position.y)
        # subtraction the mouse y pos with the ball y pos and multiply it to get the vY the ball will have
        self.set_velocity(x, y)

    def get_pos(self):
        """
        A function whose purpose is to let externals to get the ball canter position
        ------
        :return: (float, float)
            the ball center
        """
        return self.body.position

    def get_first_pos(self):
        """
        A function whose purpose is to let externals to get an saved position the ball had, that way when a ball need
        to reset the externals will take this position and place the ball there
        ------
        :return: (float, float)
            the ball center saved position
        """
        return self.x, self.y

    def move_ball_up_and_down(self, vel=100, max_height=80):
        """
        A function whose purpose is to move the ball up and down; that way it will be harder to score
        ------
        :param vel: (float)
            the y velocity the ball will move through; default - 100
        :param max_height: (float)
            the maximum height the ball can reach when moving up or down through the y axis; default - 80
        """

        # if direction is up the ball y velocity will be negative to make the ball move against the y axis(up), else
        # it will be positive to make the ball go with the y axis(down)
        if self.direction == "up":
            self.body.velocity = (0, -vel)
        else:
            self.body.velocity = (0, vel)

        # checking if the ball passed the maximus height he can reach, if so the direction will change
        if self.body.position[1] > self.y + max_height:
            self.body.velocity = (0, -vel)
            self.direction = "up"
        elif self.body.position[1] < self.y - max_height:
            self.body.velocity = (0, vel)
            self.direction = "down"
