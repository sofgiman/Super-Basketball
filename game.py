import pymunk
import pygame
from pygame import mixer
from classes.Ball import Ball
from classes.Line import Line
from classes.BasketNet import BasketNet
from classes.Block import Block
from classes.TimeBar import TimeBar
import random
from classes.ThrowingAimer import ThrowingAimer
from classes.BasketballRing import BasketallRing
from classes.Rectangale import Rectangale
from classes.Button import button
from datetime import datetime
import threading

import Images
import sounds

pygame.init()


class Game:
    """
    A class used to represent the whole game
    """

    def __init__(self):
        self.running, self.quit_game = True, False  # running - checks if the game still runs, quit_game - checks is app should quit
        self.display_menu = False  # bool that checks if to go to the menu screen after leaving game
        self.display_losing_screen = False  # bool that checks if to go to the losing screen after leaving game
        self.display_winning_screen = False  # bool that checks if to go to the winning screen after leaving game

        self.win = pygame.display.set_mode((600, 600))  # creating the game window
        pygame.display.set_caption("Basketball Game")
        self.font_name = 'freesansbold.ttf'  # setting the basic font
        self.clock = pygame.time.Clock()  # creating the clock of the game
        self.space = pymunk.Space()  # creating the space of the game using pymunk
        self.space.gravity = 0, 1000  # creating gravity of the space - that way dynamic objects will drawn down
        self.FPS = 80  # creating fps of the game

        self.defiently_not_scored = False  # a bool that check if the player definitely didn't scored
        self.scored = False  # a bool that check if the player scored
        self.basketball_collosions_with_floor = 0  # a counter that counter the collisions the ball have with the floor
        self.score = 0  # the score the player earned
        self.new_level = True  # check if new level need to be shawn
        self.mouse_click = False  # checks if mouse clicked - with it it's you can know when to throw the ball
        # self.start_bird_sound_flag = False
        self.update_scoreboared = True  # flag that tells if the scoreboard need to be updated

        self.start_timer = False
        self.timer = 0

        self.ball_throwed = False  # check if the ball has been throw; if he is on the air
        # self.start_bird_sound_timer = threading.Timer(3, self.start_bird_sound)
        # self.start_bird_sound_timer.daemon = True
        # self.start_bird_sound_timer.start()

        self.collosions_with_basket_sensors = {
            # a direction that contains 3 booleans that checks if there wah collision
            # between the ball and the sensors
            "upper_rect": False,
            "lower_rect": False,
            "left_rect": False
        }

        self.BLUE = (33, 32, 200)
        self.CYAN = (40, 255, 250)
        self.exit_button = button(self.BLUE, 10, 10, 50, 25, 'Home', 20)  # creating the exit button

        self.swish_sound_file = 'Sounds/Swish.wav'  # the sound when the player scores a shot
        self.bounce_sound_file = 'Sounds/BOUNCE1.wav'  # the sound when the ball collide with floor and the basket net
        self.timer_started = False

        self.ball_moving_trap_timer_started = False
        self.start_the_ball_trap = False
        # self.birds_sound = threading.Timer(1, self.play_sound,args=(self.swish_sound_file))
        # self.birds_sound= threading.Timer(1, self.play_sound, args=(self.swish_sound_file,))
        # self.birds_sound.start()
        self.welcome_to_the_game_message = False  # a bool that checks if the welcome message had been shown
        self.was_welcome_to_the_game_message_timer = False  # a bool that checks if the timer to stop the welcome message started

        self.traps = {  # a direction that contains a specific int the traps have
            "moving_ball": 1,
            "moving_basket_net": 2,
            "moving_block": 3
        }

        self.traps_state = {  # a direction that contains the traps stats; true if they are triggered
            "moving_ball": False,
            "moving_basket_net": False,
            "moving_block": False
        }

        self.time_for_each_level = {  # a direction that contains how much time each level have( in seconds)
            "0-1": 15,
            "1-2": 10,
            "2-3": 15,
            "3-4": 15,
            "4-5": 10,
            "5-6": 15,
            "6-7": 10,
            "7-8": 15,
            "8-9": 10,
            "9-10": 15
        }

        self.current_level_time = self.time_for_each_level["0-1"]  # contains the current time a level has
        self.star_date_level = None  # the starting date the game had a moment after the game start
        self.passed_level = False  # check if level passes
        self.player_won = False  # check if player won
        self.player_lost = False  # check if player lost

    def redraw_window(self, basketball, floor, basket_net, aimer, block, time_bar, background_surface, background_rect,
                      basketball_throwed=False):
        """
        A function whose purpose is to draw all the game objects, buttons, texts on the screen
        ------
        :param basketball: Ball
            the basketball that need to be drawn
        :param floor: Line
            the floor of the game
        :param basket_net: BasketNet
            the basket net of the game
        :param aimer: ThrowingAimer
            the intention of the ball
        :param block: Block
            the block
        :param time_bar: TimeBar
            the time bar
        :param background_surface: pygame.image.load
            the background image surface
        :param background_rect: image.rect
            the background image rect
        :param basketball_throwed: bool
            check if the aimer need to be drawn
        """
        self.win.fill((255, 255, 255))  # clear the win
        # draw background
        self.win.blit(background_surface, background_rect)  # displaying the image
        self.display_score()  # displaying the score
        time_bar.draw(self.current_level_time - self.timer_counter)  # displaying the time bar

        if self.welcome_to_the_game_message == False:  # check if need to draw the welcome message
            self.display_welcome_stage()
        # print("asa")

        basketball.draw()  # draw ball
        floor.draw()  # draw floor
        basket_net.draw()  # draw basket net
        if self.traps_state["moving_block"] == True:  # check if the block trap is triggered, if so drawing the block
            block.draw()
            block.move_up_and_down(250, 80)  # move the block

        if self.traps_state["moving_basket_net"]:  # check if the basket net trap is triggered, if so trigger her
            basket_net.move_basket()
        else:
            basket_net.stop_move_basket()
        self.exit_button.draw(self.win)  # displaying exit button
        #  upper_rect_temp.draw()
        # lower_rect_temp.draw()
        # left_sided_rect_temp.draw()
        if not basketball_throwed:  # check if the need to be drawn, if so drawing it
            aimer.set_p1(basketball.body.position)
            aimer.set_p2(pygame.mouse.get_pos())
            aimer.draw()

    def start_game(self):
        """
        A function whose purpose is to start the game; this is the main loop of the game
        """
        self.running = True

        background_surface = pygame.image.load('Images/park_background_1.png')  # loading the image
        background_surface = pygame.transform.scale(background_surface, (600, 600))
        background_rect = background_surface.get_rect(center=(300, 300))

        collosion_types = {  # All of the collision types
            "floor": 0,
            "basketball": 1,
            "basket_ring": 2,
            "upper_rect": 3,
            "lower_rect": 4,
            "left_rect": 5,
            "basket_lines": 6,
            "block_trap": 7
        }

        basketball = Ball(self.space, self.win, 100, 400, 10, collosion_types["basketball"])  # creating the basketball
        aimer = ThrowingAimer(self.win, basketball.get_pos(), pygame.mouse.get_pos(), 4)  # creating the aimer
        floor = Line(self.space, self.win, (0, 550), (800, 550), 5,
                     collision_type=collosion_types["floor"])  # creating the floor
        basket_net = BasketNet(self.space, self.win, collosion_types)  # creating the basket net
        block = Block(self.space, self.win, 350, 240, 10, 100, collosion_types["block_trap"],
                      (0, 0, 0))  # creating the block
        time_bar = TimeBar(self.win)  # creating the time bar

        handler = self.space.add_collision_handler(collosion_types["basketball"], collosion_types[
            "basket_ring"])  # creating a handler for basketball and the net collision
        upper_rect_handler = self.space.add_collision_handler(collosion_types["basketball"], collosion_types[
            "upper_rect"])  # creating a handler for basketball and the upper sensor collision
        lower_rect_handler = self.space.add_collision_handler(collosion_types["basketball"], collosion_types[
            "lower_rect"])  # creating a handler for basketball and the lower sensor collision
        left_rect_handler = self.space.add_collision_handler(collosion_types["basketball"], collosion_types[
            "left_rect"])  # creating a handler for basketball and the left sensor collision
        basketball_floor_handler = self.space.add_collision_handler(collosion_types["basketball"], collosion_types[
            "floor"])  # creating a handler for basketball and the floor collision
        basketball_basket_line_handler = self.space.add_collision_handler(collosion_types["basketball"],
                                                                          collosion_types[
                                                                              "basket_lines"])  # creating a handler for basketball and the lines collision

        handler.begin = self.begin  # making that when the ball first collide with net it will go to these function
        # making that when the ball collide with the sensors it will go to these functions
        upper_rect_handler.begin = self.upper_rect_begin
        lower_rect_handler.begin = self.lower_rect_begin
        left_rect_handler.begin = self.left_rect_begin

        basketball_floor_handler.post_solve = self.basketball_floor_post_solve  # making that when the ball stops colliding with floor it will go to these function
        # making that when the ball first collide with floor or lines it will go to these function
        basketball_floor_handler.begin = self.basketball_collision_with_floor_begin
        basketball_basket_line_handler.begin = self.basketball_collision_with_floor_begin

        self.ball_moving_trap_timer_started = False
        # swish_sound_file = 'Sounds/Swish.wav'
        # bounce_sound_file = 'Sounds/BOUNCE1.wav'

        time_bar.current_level_time = self.current_level_time  # setting the current level time of the time bar
        self.reset_traps_state(block, basketball)  # checking if traps should be triggered
        self.new_level = False  # it's not a new level
        self.start_date_time = datetime.now()  # setting the start date date
        self.timer_counter = 0
        while self.running:
            self.timer_counter = (datetime.now() - self.start_date_time).total_seconds()

            if self.passed_level == False:  # checks if player won
                self.check_player_losing_state()
                if self.score == 10:
                    self.player_won = True

            if self.player_won:  # if player won - leaving game to the winning screen
                self.running = False
                self.display_winning_screen = True
            if self.player_lost:  # if player lost - leaving game to the losing screen
                self.running = False
                self.display_losing_screen = True

            for event in pygame.event.get():  # checking events
                if event.type == pygame.QUIT:  # if player want to quit app - quit app
                    self.running = False
                    self.quit_game = True
                elif event.type == pygame.MOUSEBUTTONDOWN:  # if the player pressed
                    if self.exit_button.isOver(
                            pygame.mouse.get_pos()):  # check if is on the exit button or on the screen
                        self.running = False  # stop loop
                        self.display_menu = True  # go to menu
                    else:
                        self.mouse_click = True  # making mouse click true - the ball will be thrown
                elif event.type == pygame.MOUSEMOTION:  # if the mouse have move
                    if self.exit_button.isOver(
                            pygame.mouse.get_pos()):  # if the mouse on exit button change his color, else reset it
                        self.exit_button.bg_color = self.CYAN
                    else:
                        self.exit_button.bg_color = self.BLUE

            if self.welcome_to_the_game_message == False:  # if the welcome message hadn't been shown
                if self.was_welcome_to_the_game_message_timer == False:  # if it's time hasn't started
                    threading.Timer(4,
                                    self.stop_display_welcome_Stage).start()  # start it's timer to make the welcome message become true
                    self.was_welcome_to_the_game_message_timer = True

            if self.start_moving_ball_trap():  # if the moving ball trap started - delay if for 0.5 sec than deploy it
                threading.Timer(0.5, self.trigger_moving_ball_trap).start()
                self.ball_moving_trap_timer_started = True

            if not self.mouse_click:  # if the ball shouldn't thrown
                if (self.start_the_ball_trap):  # check if the moving trap should be on
                    basketball.continue_move()
                    basketball.move_ball_up_and_down()
                else:
                    basketball.stop()
            else:
                if not self.ball_throwed:  # if the ball hasn't thrown yet - throw the ball
                    basketball.continue_move()  # let the ball move
                    basketball.set_velocity(0, 0)
                    self.ball_throwed = True
                    # basketball.body.velocity =400,-550
                    aimer.throw_ball(basketball)  # throw the ball

            if self.start_timer:  # check if the timer for reset all variables needs to start, if so start it
                if self.timer_started == False:
                    threading.Timer(0.6, self.reset_all_varibales, args=(
                        basketball, aimer, block, time_bar)).start()  # after 0.6 seconds the function will be triggered
                    self.timer_started = True
            else:
                self.start_timer = self.start_new_round(basketball)  # check if need to start a new round

            if self.scored and self.update_scoreboared == True:  # if the scoreboard need to be updated and the score increased
                self.score += 1
                self.new_level = True  # a new level needs to be
                self.passed_level = True  # the player passed the current level
                self.update_scoreboared = False  # no needs to update scoreboard anymore
                self.play_sound(self.swish_sound_file)  # play the shot score sound

            # print(self.basketball_collosions_with_floor)
            # self.redraw_window(basketball, floor, baketLine, basketball_ring, aimer, background_surface, background_rect
            #                   , self.mouse_click)

            self.redraw_window(basketball, floor, basket_net, aimer, block, time_bar, background_surface,
                               background_rect, self.mouse_click)  # re draw the window
            pygame.display.update()  # update the window
            self.clock.tick(self.FPS)  # slow the clock
            self.space.step(1 / self.FPS)

    pygame.quit()  # quit pygame

    def check_player_losing_state(self):
        """
        A function whose purpose is to check if the player lost the game
        """
        time_left = self.current_level_time - int(self.timer_counter)  # calculating the time left for these level
        if time_left < 0 and self.ball_throwed == False:  # checking if player lost
            self.player_lost = True

    def update_current_level(self):
        """
        A function whose purpose is to update current level state
        """
        if self.score == 0:
            self.current_level_time = self.time_for_each_level["0-1"]
        elif self.score == 1:
            self.current_level_time = self.time_for_each_level["1-2"]
        elif self.score == 2:
            self.current_level_time = self.time_for_each_level["2-3"]
        elif self.score == 3:
            self.current_level_time = self.time_for_each_level["3-4"]
        elif self.score == 4:
            self.current_level_time = self.time_for_each_level["4-5"]
        elif self.score == 5:
            self.current_level_time = self.time_for_each_level["5-6"]
        elif self.score == 6:
            self.current_level_time = self.time_for_each_level["6-7"]
        elif self.score == 7:
            self.current_level_time = self.time_for_each_level["7-8"]
        elif self.score == 8:
            self.current_level_time = self.time_for_each_level["8-9"]
        elif self.score == 9:
            self.current_level_time = self.time_for_each_level["9-10"]

    def reset_traps_state(self, block, basketball):
        """
        A function whose purpose is to reset the traps state; mainly used after passing a new level
        ------
        :param block: Block
            the block
        :param basketball: Ball
            the basketball
        """
        # resetting all variables related to the traps
        self.ball_moving_trap_timer_started = False
        self.start_the_ball_trap = False
        self.traps_state["moving_basket_net"] = False
        self.traps_state["moving_ball"] = False
        self.traps_state["moving_block"] = False

        rand_trap = random.randint(self.traps["moving_ball"], self.traps["moving_block"])  # creating a random int that the trap will be
        # print(rand_trap)

        if 0 <= self.score <= 1:  # if true than no traps should be triggered
            self.traps_state["moving_basket_net"] = False
            self.traps_state["moving_ball"] = False
            self.traps_state["moving_block"] = False

        rand_trap = random.randint(self.traps["moving_basket_net"], self.traps["moving_block"])
        if 2 <= self.score <= 4:  # if true than one random trap that it is the basket net or the block trap should be triggered
            if rand_trap == self.traps["moving_basket_net"]:
                self.traps_state["moving_basket_net"] = True
            elif rand_trap == self.traps["moving_block"]:
                self.traps_state["moving_block"] = True

        rand = [1, 2, 3]
        random.shuffle(rand)
        if 5 <= self.score <= 6:  # if true than the basket net and the block trap should be triggered
            self.traps_state["moving_basket_net"] = True
            self.traps_state["moving_block"] = True

        if 7 <= self.score <= 8:  # if true than the basket net and the block trap should be triggered, and the block will be closer to the ball
            self.traps_state["moving_basket_net"] = True
            self.traps_state["moving_block"] = True

        if self.score == 9:  # if true than all traps should be triggered
            self.traps_state["moving_ball"] = True
            self.traps_state["moving_basket_net"] = True
            self.traps_state["moving_block"] = True

        if self.traps_state["moving_block"] == True:  # making that if the score >= 7 and block trap is triggered than the block will be close to the ball
            if block.on_space == False:  # display block on space if needed
                block.display_block()
                block.on_space = True
            if self.score >= 7:
                block.set_pos(basketball.body.position)
        else:
            if block.on_space == True: # remove block from space if needed
                block.remove_and_reset()
                block.on_space = False

    def trigger_moving_ball_trap(self):
        """
        A function whose purpose is to start moving the ball trap
        """
        self.start_the_ball_trap = True

    def start_moving_ball_trap(self):
        """
        A function whose purpose is to let the main loop know the moving trap hasn't started when it needs to
        :return: bool
            true if the moving ball trap should start
        """
        if self.traps_state["moving_ball"] and self.ball_moving_trap_timer_started == False:
            return True
        else:
            return False

    def draw_text(self, text, size, x, y):
        """
        A function whose purpose is to display text on pygame window
        ------
        :param text: string
            the text need to be drawn
        :param size: int
            the font size
        :param x: float
            the starting x of where the text will drawn
        :param y: float
            the starting x of where the text will drawn
        """
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, (0, 0, 0))
        self.win.blit(text_surface, (x, y))

    def display_score(self):
        """
        A function whose purpose is to display the score on the screen
        """
        self.draw_text("Score: " + str(self.score), 25, 420, 40)

    def display_welcome_stage(self):
        """
        A function whose purpose is to display the welcome message on the screen
        """
        if self.score == 0:
            self.draw_text("Score 10 shots to win", 24, 130, 40)

    def stop_display_welcome_Stage(self):
        """
        A function whose purpose is to stop display the welcome message on the screen
        """
        self.welcome_to_the_game_message = True  # making that the welcome message had been shown will stop displaying it

    def basketball_crosssed_edege(self, basketball):
        """
        A function whose purpose is to check if the ball crossed the edges
        ------
        :param basketball: Ball
            the ball
        :return: bool
            true if basketball crossed edges
        """
        if basketball.body.position.x > 600 + 10 or basketball.body.position.x < 0 - 10:
            return True
        else:
            return False

    def basketball_on_floor(self):
        """
        A function whose purpose is to check if the ball collide a lot with the floor
        ------
        :return: bool
            true if the basketball collide too much with the floor
        """
        if self.basketball_collosions_with_floor > 2:
            return True
        else:
            return False

    def start_new_round(self, basketball):
        """
        A function whose purpose is to check if player's shot didn't scored and a new round should start
        ------
        :param basketball: Ball
            the ball
        :return: bool
            if a new round should start - return true
        """
        if self.basketball_crosssed_edege(basketball):
            return True
        elif self.basketball_on_floor():  # if ball is on the floor
            return True
        return False

    def reset_all_varibales(self, basketball, aimer, block, time_bar):
        """
        A function whose purpose is to reset all the variable after a new round or a new level
        ------
        :param basketball: Ball
            the ball
        :param aimer: ThrowingAimer
            the aimer
        :param block: Block
            the block
        :param time_bar: TimeBar
            the time bar
        """
        basketball.body.velocity = 0, 0
        basketball.body.position = basketball.get_first_pos()  # setting ball position to it's original
        aimer.set_p1(basketball.body.position)  # setting aimer p1 to basketball center
        self.update_scoreboared = True  # the scoreboard can be be updated now
        self.defiently_not_scored = False  # because there's a new round
        self.scored = False  # because there's a new round
        self.basketball_collosions_with_floor = 0  # because there's a new round
        self.mouse_click = False  # because there's a new round
        self.timer = 0  # the new round reset the timer to 0
        self.start_timer = False  # there is no need to start the reset variables timer because the new roung
        self.timer_started = False  # timer hasn't started
        self.ball_throwed = False  # ball didn't thrown because of the new round

        for key, value in self.collosions_with_basket_sensors.items():  # resetting the collision with sensor to false because there's a new round
            self.collosions_with_basket_sensors[key] = False

        if self.new_level:  # if a new level should be
            x, y = random.randint(20, 200), random.randint(50, 420)  # make a random position for the basketball
            basketball.body.position = (x, y)  # change ball position
            basketball.x = x  # resetting the ball original position
            basketball.y = y  # resetting the ball original position
            self.reset_traps_state(block, basketball)  # check for new traps
            self.new_level = False  # there is no new level now
            self.start_date_time = datetime.now()  # update start date time
            self.passed_level = False  # level hasn't passed
            self.update_current_level()
            time_bar.current_level_time = self.current_level_time  # update the current level time of the time bar

    def begin(self, arbiter, space, data):
        """
        A function whose purpose is to let the ball go through the net
        ------
        :return: bool
            always false - because on pymunk when returning false on these handler function between the pymunk objects
            won't be a collision and we need these to make the ball go through the net
        """
        return False

    def upper_rect_begin(self, arbiter, space, data):
        """
        A function whose purpose is to let the ball go through the upper sensor and update that there was a
        collision between the ball and the upper sensor
        ------
       :return: bool
           always false - because on pymunk when returning false on these handler function - between the pymunk objects
           won't be a collision and we need these to make the ball go through these sensor
       """
        self.collosions_with_basket_sensors["upper_rect"] = True  # update that the ball went through the sensor
        return False

    def lower_rect_begin(self, arbiter, space, data):
        """
        A function whose purpose is to let the ball go through the lower sensor and also checks if the player scored his shot
        ------
        :return: bool
           always false - because on pymunk when returning false on these handler function - between the pymunk objects
           won't be a collision and we need these to make the ball go through these sensor
        """
        if self.collosions_with_basket_sensors["upper_rect"] == False:  # if there wasn't a collision with the upper rect
            # than that means the ball went from the bottom - which means the player definitely didn't scored
            self.defiently_not_scored = True
        elif self.defiently_not_scored == False:  # if definitely not scored = false - means that the ball came from above
            # and the player scored
            self.scored = True
        return False

    def left_rect_begin(self, arbiter, space, data):
        """
        A function whose purpose is to let the ball go through the left sensor
        ------
        :return: bool
           always false - because on pymunk when returning false on these handler function - between the pymunk objects
           won't be a collision and we need these to make the ball go through these sensor
        """
        if self.collosions_with_basket_sensors["upper_rect"] == False:  # if the ball collide with these sensor before the upper
            # means that definitely there wasn't a score
            self.defiently_not_scored = True
        return False

    def basketball_collision_with_floor_begin(self, arbiter, space, data):
        """
        A function whose purpose is to play the bounce sound when the ball collides with the floor or the basket lines
        ------
        :return: bool
            always true to make a collision between the handler object
        """
        self.play_sound(self.bounce_sound_file)
        return True

    def basketball_floor_post_solve(self, arbiter, space, data):
        """
        A function whose purpose is to increase by one collision with the floor
        """
        self.basketball_collosions_with_floor += 1
        # self.play_sound('sounds/BOUNCE1.wav')
        # self.play_sound('sounds/BBOUNCE2.wav')

    def play_sound(self, sound_file):
        """
        A function whose purpose is to play a sound
        ------
        :param sound_file: sound file
            the sound that should be played
        """
        sound = mixer.Sound(sound_file)
        sound.play()  # playing the sound

