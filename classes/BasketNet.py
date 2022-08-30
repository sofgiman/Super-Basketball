import pymunk
import pygame
import Images
from classes.Line import Line
from classes.BasketballRing import BasketallRing
from classes.Rectangale import Rectangale
pygame.init()


class BasketNet:
    """
    A class used to represent the whole basketball net, It consists six parts:
    A net - the visual net the user sees
    A large basketball line - a long line that connected to the floor and to the net from it's right
    A small basketball 2 line - a  line that connected just to net from it's left; made to make the scoring technique easier
    A left sensor - it's a rectangle that is inside the net on her lefter side; it's check if the ball comes from
     the left or not( written in the game)
    An upper sensor - it's a rectangle that is inside the net on her upper side; it's check if the ball comes from
     above or not( written in the game)
    Aa lower sensor - it's a rectangle that is inside the net on her lower side; it's check if the ball comes from
     below or not( written in the game)
    """
    def __init__(self, space, win, collision_types):
        """
        :param space: pymunk.space
            the space the whole basket net will be on
        :param win: pygame.display
            the display the whole basket net will visual on
        :param collision_types: direction of ints
            all the collision types of the parts that build the whole basket net
        """

        self.win = win
        self.space = space

        # creating an instances that connected to each other part in order to make the basket net connected
        net_startX = 450  # the starting x of the net; where it should start to be drawn from the x axis
        net_startY = 330  # the starting y of the net; where it should start to be drawn from the y axis
        width_of_net = 50  # the net width
        height_of_net = 30  # the net height
        difference_between_netY_to_LargeLineY = 30  # difference between the starting y of the large line to the net's starting y
        basket_large_lineY = net_startY - difference_between_netY_to_LargeLineY
        floor_y = 550

        difference_between_netX_to_left_sensor = 4  # how close the left sensor will be to the net x from the left
        left_sensorX = net_startX + difference_between_netX_to_left_sensor
        upper_and_lower_sensorX = left_sensorX + 1  # these sensors need to be on the right from the left sensor
        differnce_between_netY_to_upper_sensorY = 2  # how close the upper sensor will be to the net y from up
        differnce_between_LowerSensorTop_to_netBottom = 5  # how close the starting y of the lower sensor will be to the net bottom from below
        upper_sensorY = net_startY + differnce_between_netY_to_upper_sensorY
        lower_sensorY = net_startY + height_of_net - differnce_between_LowerSensorTop_to_netBottom
        upper_and_lower_width = 40  # these sensors width
        upper_and_lower_height = 3  # these sensors heigt
        left_sensorY = net_startY + 10

        self.baketLine = Line(self.space, self.win, (net_startX + width_of_net, basket_large_lineY), (net_startX + width_of_net, floor_y), 4,
                              collision_type=collision_types["basket_lines"])  # creating the small line using the data above to create it's two points
        self.basket2Line = Line(self.space, self.win, (net_startX, net_startY), (net_startX, net_startY + height_of_net)
                                , 3, (255, 0, 0), collision_types["basket_lines"])  # creating the large line using the data above to create it's two points
        self.basketball_ring = BasketallRing(self.space, self.win, net_startX, net_startY, width_of_net, height_of_net, collision_types["basket_ring"])
        # creating the basketball ring(net)
        self.upper_rect_temp = Rectangale(self.space, self.win, upper_and_lower_sensorX, upper_sensorY,
                                          upper_and_lower_width, upper_and_lower_height, collision_types["upper_rect"])
        self.lower_rect_temp = Rectangale(self.space, self.win, upper_and_lower_sensorX, lower_sensorY,
                                          upper_and_lower_width, upper_and_lower_height, collision_types["lower_rect"])
        self.left_sided_rect_temp = Rectangale(self.space, self.win, left_sensorX, left_sensorY,
                                               2, 15, collision_types["left_rect"])
        # creating the sensors using data above

    def draw(self):
        """
        A function whose purpose is to draw the whole basket net on the window; only the large line and the net are
        seen because the sensors shouldn't be seen and the 2nd line is a helper object and also shouldn't be seen
        and the ones above are the only visual you see even in real court
        """
        self.baketLine.draw()  # draw the large line that's connected to the floor
        # self.basket2Line.draw()
        self.basketball_ring.draw()  # draw the net
        # self.upper_rect_temp.draw()
        # self.lower_rect_temp.draw()
        # self.left_sided_rect_temp.draw()

    def move_basket(self):
        """
        A function whose purpose is to move the basket net right and left; that way it will be harder to score
        """
        max_width = 80  # creating maximum width the basket net can reach
        vel = 100  # creating velocity the net will have

        # moving all parts together
        self.baketLine.move_right_and_left(vel, max_width)
        self.basket2Line.move_right_and_left(vel, max_width)
        self.basketball_ring.move_right_and_left(vel, max_width)
        self.upper_rect_temp.move_right_and_left(vel, max_width)
        self.lower_rect_temp.move_right_and_left(vel, max_width)
        self.left_sided_rect_temp.move_right_and_left(vel, max_width)

    def stop_move_basket(self):
        """
        A function whose purpose is to stop the basket net when it moving right and left and reset it to it's original
        location
        """

        # stopping and resetting all parts
        self.baketLine.stop_and_reset()
        self.basket2Line.stop_and_reset()
        self.basketball_ring.stop_and_reset()
        self.upper_rect_temp.stop_and_reset()
        self.lower_rect_temp.stop_and_reset()
        self.left_sided_rect_temp.stop_and_reset()
