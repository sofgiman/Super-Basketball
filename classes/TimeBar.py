import pygame

pygame.init()


class TimeBar:
    """
    A class used to represent a time bar on pygame display
    """

    def __init__(self, win):
        """
        :param win: pygame.display
            the display the time bar will visual on
        """
        self.win = win
        self.current_level_time = None  # current level time in seconds; this is the maximum time that can be given
        self.time_left = None  # the time left in seconds; this is how much time left to time bar, if it will equal
        # to the current level time than the time bar will be at it's maximum, if it will equal 0 that mean that there is no time
        # left and the time bar will be at it's minimum(empty)
        self.rectX = 240  # the time bar rect starting x
        self.rectY = 100  # the time bar rect starting y
        self.rect_width = 80  # the time bar rect width; this is the maximum width the rect will have
        self.rect_height = 20  # the time bar rect height; this is the maximum height the rect will have

        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.LIGHT_DARK = (60, 60, 0)

    def draw(self, time_left):
        """
        Call this method to draw the time bar on the screen
        ------
        :param time_left: float
            the time left for the time bar to be filled
        """
        color = self.LIGHT_DARK  # time bar color
        outline_color = self.BLACK  # time bar outlines color

        self.time_left = time_left
        if self.time_left < 0:
            self.time_left = 0
            outline_color = self.RED

        part_time_left = self.time_left / self.current_level_time  # this is the part of the time left; that way it's possible
        # to know how much filled the time bar need to be

        if part_time_left < 0.33:  # if a long time passes than the time bar color will be red
            color = self.RED
        pygame.draw.rect(self.win, color,
                         pygame.Rect(self.rectX, self.rectY, self.rect_width * part_time_left, self.rect_height))  # draw the time bar
        self.draw_outlines(outline_color)  # draw outlines

    def draw_outlines(self, color):
        """
        A function that meant to draw the outlines of the time_bar; get a color that the outlines will have
        :param color: (int, int, int)
            the outlines color
        """
        # draw upper horizontal outline
        pygame.draw.rect(self.win, color, pygame.Rect(self.rectX - 2, self.rectY - 2, self.rect_width + 4, 2))
        # draw lower horizontal outline
        pygame.draw.rect(self.win, color,
                         pygame.Rect(self.rectX - 2, self.rectY + self.rect_height, self.rect_width + 4, 2))
        # draw righter vertical outline
        pygame.draw.rect(self.win, color, pygame.Rect(self.rectX - 2, self.rectY - 2, 2, self.rect_height + 4))
        # draw lefter vertical outline
        pygame.draw.rect(self.win, color, pygame.Rect(self.rectX + self.rect_width, self.rectY, 2, self.rect_height))
