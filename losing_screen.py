import pygame
from classes.Button import button
from classes.Label import label


class losingScreen:
    """
    A class used to represent the losing screen
    """
    def __init__(self):
        self.win = pygame.display.set_mode((600, 600))  # creating the window
        self.running = True  # make the main loop run
        self.quit_game = False
        self.display_menu = False  # bool that checks if to go to the menu screen after leaving screen
        self.display_game = False  # bool that checks if to go to the game screen after leaving screen
        self.clock = pygame.time.Clock()
        self.FPS = 80

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (33, 32, 200)
        self.CYAN = (40, 255, 250)

    def redraw_window(self, game_over_label, menu_button, play_again_button):
        """
        A function whose purpose is to draw all buttons and labels on the screen
        ------
        :param game_over_label: label
            the game over label
        :param menu_button: button
            menu button
        :param play_again_button: button
            play again button
        """
        self.win.fill(self.BLACK)
        game_over_label.draw(self.win)
        menu_button.draw(self.win)
        play_again_button.draw(self.win)

    def main_loop(self):
        """
        A function whose purpose is to show the losing screen; this is the main loop of these screen
        """
        self.running = True
        # creating labels and buttons
        game_over_label = label(self.BLACK, self.RED, 200, 150, 200, 50, "Game Over", 70)
        menu_button = button(self.BLUE, 50, 320, 200, 100, "Menu", 55)
        play_again_button = button(self.BLUE, 350, 320, 200, 100, "Play Again", 55)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # check if needed to quit the whole app
                    self.running = False
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if mouse pressed
                    if menu_button.isOver(pygame.mouse.get_pos()):  # go to menu
                        self.running = False
                        self.display_menu = True
                    if play_again_button.isOver(pygame.mouse.get_pos()):  # go to game again
                        self.running = False
                        self.display_game = True
                elif event.type == pygame.MOUSEMOTION:  # if was a mouse motion
                    if menu_button.isOver(pygame.mouse.get_pos()):  # change menu button background color
                        menu_button.bg_color = self.CYAN
                    else:
                        menu_button.bg_color = self.BLUE
                    if play_again_button.isOver(pygame.mouse.get_pos()):  # change play again background button color
                        play_again_button.bg_color = self.CYAN
                    else:
                        play_again_button.bg_color = self.BLUE

            self.redraw_window(game_over_label, menu_button, play_again_button)  # redraw window
            pygame.display.update()
            self.clock.tick(self.FPS)
