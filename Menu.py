import pygame
from classes.Button import button
from classes.Label import label


class Menu:
    """
    A class used to represent the menu
    """
    def __init__(self):
        self.win = pygame.display.set_mode((600, 600))  # creating win
        self.running = True  # make the main loop run
        self.quit_game = False
        self.display_game = False  # bool that checks if to go to the game screen after leaving menu
        self.display_credits = False  # bool that checks if to go to the credits screen after leaving menu
        self.clock = pygame.time.Clock()
        self.FPS = 80


        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

    def redraw_window(self, game_name_label, play_button, credits_button):
        """
        A function whose purpose is to draw all the buttons and labels on the screen
        ------
        :param credits_button: button
            the credits button
        :param play_button: button
            the game button
        :param game_name_label: label
            the game name label
       """
        self.win.fill(self.BLACK)
        game_name_label.draw(self.win)
        play_button.draw(self.win)
        credits_button.draw(self.win)


    def main_loop(self):
        """
        A function whose purpose is to show the menu; this is the main loop of the menu
        """
        self.running = True
        # creating labels and button
        game_name_label = label(self.BLACK, (210, 121, 32), 100, 100, 400, 80, 'Super Basketball')
        play_button = button((33, 32, 200), 200, 250, 200, 60, 'Play', 50)
        credits_button = button((33, 32, 200), 200, 350, 200, 60, 'Credits', 50)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # check if needed to quit the whole app
                    self.running = False
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed
                    if play_button.isOver(pygame.mouse.get_pos()):  # go to game
                        self.running = False
                        self.display_game = True
                    if credits_button.isOver(pygame.mouse.get_pos()):  # go to credits
                        self.running = False
                        self.display_credits = True
                elif event.type == pygame.MOUSEMOTION:
                    if play_button.isOver(pygame.mouse.get_pos()):  # change background color
                        play_button.bg_color = (40, 255, 250)
                    else:
                        play_button.bg_color = (33, 32, 200)
                    if credits_button.isOver(pygame.mouse.get_pos()):  # change background color
                        credits_button.bg_color = (40, 255, 250)
                    else:
                        credits_button.bg_color = (33, 32, 200)

            self.redraw_window(game_name_label, play_button, credits_button)  # redraw window
            pygame.display.update()  # update window
            self.clock.tick(self.FPS)
