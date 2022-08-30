import pygame
from classes.Button import button
from classes.Label import label


class CreditsScreen:
    """
   A class used to represent the credits screen
   """
    def __init__(self):
        self.win = pygame.display.set_mode((600, 600))   # creating the window
        self.running = True  # make the main loop run
        self.quit_game = False
        self.display_menu = False  # bool that checks if to go to the menu screen after leaving screen
        self.clock = pygame.time.Clock()
        self.FPS = 80

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (33, 32, 200)
        self.CYAN = (40, 255, 250)


    def redraw_window(self, credits_label1, credits_label2, credits_label3, menu_button):
        """
        A function whose purpose is to draw all buttons and labels on the screen
        ------
        :param credits_label1: label
            first label
        :param credits_label2: label
            second label
        :param credits_label3: label
            third label
        :param menu_button: button
            menu button
        """
        self.win.fill(self.BLACK)
        credits_label1.draw(self.win)
        credits_label2.draw(self.win)
        credits_label3.draw(self.win)
        menu_button.draw(self.win)


    def main_loop(self):
        """
        A function whose purpose is to show the credits screen; this is the main loop of these screen
        """
        self.running = True
        startY = 100
        # creating labels and buttons
        credits_label1 = label(self.BLACK, self.WHITE, 100, startY, 400, 50, "This game created by Idan Yafe,", 50)
        credits_label2 = label(self.BLACK, self.WHITE, 100, startY + 50, 400, 50, "in Quarter 2 of 11th grade", 50)
        credits_label3 = label(self.BLACK, self.WHITE, 100, startY + 100, 400, 20, "2020 - 2020", 20)
        menu_button = button(self.BLUE, 200, 320, 200, 100, "Menu", 55)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # check if needed to quit the whole app
                    self.running = False
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed
                    if menu_button.isOver(pygame.mouse.get_pos()):  # go to menu
                        self.running = False
                        self.display_menu = True
                elif event.type == pygame.MOUSEMOTION:  # if was a mouse motion
                    if menu_button.isOver(pygame.mouse.get_pos()):  # change menu button background color
                        menu_button.bg_color = self.CYAN
                    else:
                        menu_button.bg_color = self.BLUE

            self.redraw_window(credits_label1, credits_label2, credits_label3, menu_button)  # redraw window
            pygame.display.update()
            self.clock.tick(self.FPS)
