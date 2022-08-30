import pymunk
import pygame
from game import Game
from Menu import Menu
from losing_screen import losingScreen
from WinningScreen import WinningScreen
from CreditsScreen import CreditsScreen

pygame.init()

game = Game()  # creating the game
menu = Menu()  # creating the menu
losing_screen = losingScreen()  # creating the losing screen
winning_screen = WinningScreen()  # creating the winning screen
credits_screen = CreditsScreen()  # creating the credits screen

on_winning_screen = False  # app state - currently false
on_losing_screen = False  # app state - currently false
on_credits = False  # app state - currently false
on_game = False  # app state - currently false
on_menu = True  # app state - currently true

# app_state : {
#    "game": 1,
#    "menu" : 2
# }



while not game.quit_game and not menu.quit_game and not losing_screen.quit_game and not winning_screen.quit_game and not credits_screen.quit_game:
    """
    This is the main loop of the whole and it continues until the player quit the app
    """
    if on_menu:  # if on menu state
        # state = app_state.menu;
        menu.main_loop()  # start menu main loop
        on_menu = False
        if menu.display_game:  # check if player want to go to the game
            on_game = True  # go to the game
            menu.display_game = False
        elif menu.display_credits:  # check if player want to go to the credits
            on_credits = True  # go to credits
            menu.display_credits = False

    if on_game:  # if on game state
        game.start_game()  # start game main loop
        on_game = False
        if game.display_menu:  # if player want to go to the menu
            game = Game()  # create new game
            on_menu = True  # go to menu
            game.display_menu = False
        elif game.display_losing_screen:   # if player lost
            on_losing_screen = True  # go to losing screen
            game = Game()  # create new game
        elif game.display_winning_screen:  # if player won
            on_winning_screen = True  # go to winning screen
            game = Game()  # create new game

    if on_losing_screen:  # if on losing screen state
        losing_screen.main_loop()  # start losing screen main loop
        on_losing_screen = False
        if losing_screen.display_menu:  # if player want to go to the menu
            on_menu = True  # go to menu
            losing_screen.display_menu = False
        elif losing_screen.display_game:  # if player want to go again to game
            on_game = True  # go to game
            losing_screen.display_game = False

    if on_winning_screen:  # if on winning screen state
        winning_screen.main_loop()  # start winning screen main loop
        on_winning_screen = False
        if winning_screen.display_menu:  # if player want to go to the menu
            on_menu = True  # go to menu
            winning_screen.display_menu = False
        elif winning_screen.display_game:  # if player want to go again to game
            on_game = True  # go to game
            winning_screen.display_game = False

    if on_credits:  # if on credits screen state
        credits_screen.main_loop()  # start credits screen main loop
        on_credits = False
        if credits_screen.display_menu:  # if player want to go to the menu
            on_menu = True  # go to menu
            credits_screen.display_menu = False



pygame.quit()
