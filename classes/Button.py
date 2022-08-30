import pygame


class button:
    """
    A class used to represent a button in pygame
    """
    def __init__(self, bg_color, x, y, width, height, text='', font_size=60):
        """
        :param bg_color: (int, int, int)
            the background color of the button
        :param x: float
            the x that the button will start at
        :param y: float
            the y that the button will start at
        :param width: float
            the button's width
        :param height: float
            the button's height
        :param text: string
            the text the button will have
        :param font_size: int
            the font size
        """
        self.bg_color = bg_color
        self.font_size = font_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        """
        Call this method to draw the button on the screen
        ------
        :param win: pygame.display
            the display the button will visual on
        :param outline: bool
            if an outline needed
        """
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)  # drawing outline

        pygame.draw.rect(win, self.bg_color, (self.x, self.y, self.width, self.height), 0)  # drawing a rect on the screen which represent the button's background

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)  # defining the text font
            text = font.render(self.text, True, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
            # drawing the button's text on the screen

    def isOver(self, pos):
        """
        A function whose purpose is to check if the point given is on the button
        :param pos: (tuple, tuple)
            # Pos is the usually the mouse position or a tuple of (x,y) coordinates
        :return: bool
            true if the pos is inside the button
        """

        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False
