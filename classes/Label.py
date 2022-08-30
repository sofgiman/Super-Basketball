import pygame


class label:
    """
    A class used to represent a label in pygame
    """

    def __init__(self, bg_color, fg_color, x, y, width, height, text='', font_size=60):
        """
        :param bg_color: (int, int, int)
            the background color of the label
        :param fg_color: (int, int, int)
            the color of the text
        :param x: float
            the x that the label will start at
        :param y: float
            the y that the label will start at
        :param width: float
            the label's width
        :param height: float
            the label's height
        :param text: string
            the text the label will have
        :param font_size: int
            the font size
        """
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.font_size = font_size
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        """
        Call this method to draw the label on the screen
        ------
        :param win: pygame.display
            the display the label will visual on
        :param outline: bool
            if an outline needed
        """
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.bg_color, (self.x, self.y, self.width, self.height),
                         0)  # drawing a rect on the screen which represent the label's background

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)  # defining the text font
            text = font.render(self.text, True, self.fg_color)
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))
            # drawing the label's text on the screen
