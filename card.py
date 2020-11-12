from enum import IntEnum
from colored import fg, bg, attr


# enum for card color
class Color(IntEnum):
    NONE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4


# enum for type of cards
class Type(IntEnum):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    SKIP = 10
    REVERSE = 11
    DRAW2 = 12
    WILD = 13
    DRAW4 = 14


class Card:

    def __init__(self, card_type: Type, color: Color = Color.NONE):  # defaults to no color, eg wilds
        self.type = card_type
        self.color = color

    # returns card type
    def get_type(self):
        return self.type

    # returns card color
    def get_color(self):
        return self.color

    def set_wild(self, color: Color):  # sets the color of a card if it is determined to be a wild card.
        if self.get_type() == Type.WILD or self.get_type() == Type.DRAW4:
            self.color = color

    def print(self):  # change with graphics  for some reason a black foreground shows up as white but it works as
        # intended so i'll leave it as is
        reset = attr('reset')
        if self.color == 0:  # wilds
            color = bg('black') + fg('white')
        elif self.color == 1:  # red
            color = bg('red') + fg('white')
        elif self.color == 2:  # green
            color = bg('green_4') + fg('white')
        elif self.color == 3:  # blue
            color = bg('dodger_blue_2') + fg('white')
        else:  # yellow
            color = bg('yellow') + fg('white')
        if self.type <= 12:  # non-wild card printing
            print(color + attr('bold') + str(self.color.name).capitalize() + ' ' + str(self.type.name).capitalize()
                  + reset, end='')
        else:  # wild card printing
            print(color + str(self.type.name).capitalize() + reset, end='')

    def get_path(self):
        path = 'cards/'
        if self.color == Color.RED:
            path += 'red_'
        elif self.color == Color.GREEN:
            path += 'green_'
        elif self.color == Color.BLUE:
            path += 'blue_'
        elif self.color == Color.YELLOW:
            path += 'yellow_'
        else:
            path += 'wild_'
        if self.type.value < 10:
            path += str(self.type.value) + '.png'
        elif self.type.value == 10:
            path += 'skip.png'
        elif self.type.value == 11:
            path += 'reverse.png'
        elif self.type.value == 12:
            path += 'picker.png'
        elif self.type.value == 13:
            path += 'color_changer.png'
        else:
            path += 'pick_four.png'

        return path
