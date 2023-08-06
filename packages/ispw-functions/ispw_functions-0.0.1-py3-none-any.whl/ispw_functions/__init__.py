import tkinter
# from turtle import Screen, Turtle, _Screen
import turtle

# import functions from turtle module and prefix them with t_
# from turtle import forward as t_forward, right as t_right, left as t_left, exitonclick, hideturtle, setup  # pylint: disable=no-name-in-module

old_init = turtle.Turtle.__init__


def __new_init__(self, *k, **kw) -> turtle.Turtle:
    old_init(self, *k, **kw)


old_turtle_screen = turtle.Turtle.getscreen


def __new_turtle_screen__(self) -> turtle._Screen:
    old_turtle_screen(self)

old_screen_init = turtle.Screen.__init__


def __new_screen_init__(self, *k, **kw) -> turtle._Screen:
    old_screen_init(self, *k, **kw)


turtle.Screen.__init__ = __new_screen_init__


def __done(self):
    '''hides the turtle and aits until the resulting window is clicked'''
    self.hideturtle()
    self.screen.exitonclick()


def __found(self):
    '''draws a star and calls done()'''
    self.left(108)
    for _i in range(5):
        self.forward(10)
        self.right(144)
    self.right(18)
    self.done()


turtle.Turtle.done = __done
turtle.Turtle.found = __found


def Turtle(shape=turtle._CFG["shape"],
           undobuffersize=turtle._CFG["undobuffersize"],
           visible=turtle._CFG["visible"]) -> turtle.Turtle:
    return turtle.Turtle(shape=shape, undobuffersize=undobuffersize, visible=visible)


__turtle: turtle.Turtle = None


def __SingletonTurtle() -> turtle.Turtle:
    global __turtle
    if (__turtle is None):
        __turtle = Turtle()
    return __turtle


def Screen() -> turtle._Screen:
    return turtle.Screen()


Screen().setup(500, 500, None, None)


def right(angle: int = 90):
    '''turns the pen direction to the right

    Parameters
    ----------
            angle : int, optional (default: 90)
            degrees to turn right
    '''
    __SingletonTurtle().right(angle)


def left(angle: int = 90):
    '''turns the pen direction to the left

    Parameters
    ----------
            angle : int, optional (default: 90)
            degrees to turn left
    '''
    __SingletonTurtle().left(angle)


def forward(step: int = 10):
    '''Moves the pen forward

    Parameters
    ----------
            step : int, optional
            pixels to go forward
    '''
    __SingletonTurtle().forward(step)


def step_down():
    '''draws a step down on a stair'''
    right()
    forward()
    left()
    forward()


def step_up():
    '''draws a step up on a stair'''
    left()
    forward()
    right()
    forward()


def done():
    '''hides the turtle and waits until the resulting window is clicked'''
    __SingletonTurtle().done()


def home():
    """
    Move turtle to the origin - coordinates (0,0).

    No arguments.

    Move turtle to the origin - coordinates (0,0) and set its
    heading to its start-orientation (which depends on mode).

    Example (for a Turtle instance named turtle):
    >>> turtle.home()
    """
    __SingletonTurtle().home()


def goto(x: int, y: int = None):
    """Move turtle to an absolute position.

    Aliases: setpos | setposition | goto:

    Arguments:
    x -- a number      or     a pair/vector of numbers
    y -- a number             None

    call: `goto(x, y)`        # two coordinates
    --or: `goto((x, y))`      # a pair (tuple) of coordinates
    --or: `goto(vec)`         # e.g. as returned by pos()

    Move turtle to an absolute position. If the pen is down,
    a line will be drawn. The turtle's orientation does not change.

    Example (for a Turtle instance named turtle):
    >>> tp = turtle.pos()
    >>> tp
    (0.00, 0.00)
    >>> turtle.setpos(60,30)
    >>> turtle.pos()
    (60.00,30.00)
    >>> turtle.setpos((20,80))
    >>> turtle.pos()
    (20.00,80.00)
    >>> turtle.setpos(tp)
    >>> turtle.pos()
    (0.00,0.00)
    """
    __SingletonTurtle().goto(x, y=y)


def pos() -> turtle.Vec2D:
    """Return the turtle's current location (x,y), as a Vec2D-vector.

    Aliases: pos | position

    No arguments.

    Example (for a Turtle instance named turtle):
    >>> turtle.pos()
    (0.00, 240.00)
    """
    __SingletonTurtle().pos()


def setpos(x: int, y: int = None):
    """Move turtle to an absolute position.

    Aliases: setpos | setposition | goto:

    Arguments:
    x -- a number      or     a pair/vector of numbers
    y -- a number             None

    call: goto(x, y)         # two coordinates
    --or: goto((x, y))       # a pair (tuple) of coordinates
    --or: goto(vec)          # e.g. as returned by pos()

    Move turtle to an absolute position. If the pen is down,
    a line will be drawn. The turtle's orientation does not change.

    Example (for a Turtle instance named turtle):
    >>> tp = turtle.pos()
    >>> tp
    (0.00, 0.00)
    >>> turtle.setpos(60,30)
    >>> turtle.pos()
    (60.00,30.00)
    >>> turtle.setpos((20,80))
    >>> turtle.pos()
    (20.00,80.00)
    >>> turtle.setpos(tp)
    >>> turtle.pos()
    (0.00,0.00)
    """
    __SingletonTurtle().setpos(x, y)


def position() -> turtle.Vec2D:
    """Return the turtle's current location (x,y), as a Vec2D-vector.

    Aliases: pos | position

    No arguments.

    Example (for a Turtle instance named turtle):
    >>> turtle.pos()
    (0.00, 240.00)
    """
    __SingletonTurtle().pos()


def heading() -> float:
    '''
    Return the turtle's current heading.
    '''
    return __SingletonTurtle().heading()

def setheading(to_angle) -> float:
    """Set the orientation of the turtle to to_angle.

    Parameters
    ----------
    to_angle -- a number (integer or float)

    Set the orientation of the turtle to to_angle.
    Here are some common directions in degrees:

    |    standard - mode:|          logo-mode:|
    |:-------------------|:-------------------|
    |    0 - east         |       0 - north   |
    |    90 - north       |       90 - east   |
    |    180 - west       |       180 - south |
    |    270 - south      |       270 - west  |

    Example (for a Turtle instance named turtle):
    >>> turtle.setheading(90)
    >>> turtle.heading()
    90
    """
    return __SingletonTurtle().setheading(to_angle=to_angle)


def found():
    '''draws a star and calls done()'''
    __SingletonTurtle().found()


if __name__ == '__main__':
    forward(10)
    left(90)
    forward(20)
    found()
    # print(turtle.Turtle().__name__)
    # turtle.Turtle().forward(100)
    # turtle.Turtle().found()
    # turtle.Turtle().done()
