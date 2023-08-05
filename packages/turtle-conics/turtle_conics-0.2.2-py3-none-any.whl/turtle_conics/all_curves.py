import turtle
import math


def ellipse(a, b, h=None, k=None, angle=None, angle_unit=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0
    # Angle unit can be degree or radian

    if angle is None:
        angle = 360
        converted_angle = angle*0.875

    if angle_unit == 'd' or angle_unit is None:
        converted_angle = angle * 0.875

    # We are multiplying by 0.875 because for making a complete ellipse we are plotting 315 pts according
    # to our parametric angle value

    elif angle_unit == "r":
        converted_angle = (angle * 0.875 * (180/math.pi))
    # Converting radian to degrees.

    for i in range(int(converted_angle)+1):
        if i == 0:
            myturtle.up()
        else:
            myturtle.down()
        myturtle.setposition(h+a*math.cos(i/50), k+b*math.sin(i/50))


def parabola(a, t, orientation, h=None, k=None):
    myturtle = turtle.Turtle()
    myturtle.speed(20)
    if h is None:
        h = 0
    if k is None:
        k = 0
    if orientation == 'x':
        i = -t
        while i <= t:
            if i == -t:
                myturtle.up()
                myturtle.hideturtle()
            else:
                myturtle.showturtle()
                myturtle.down()
            myturtle.setposition(h+a*math.pow(i, 2), k+2*a*i)
            i += 1/8

    elif orientation == 'y':
        i = -t
        while i <= t:
            if i == -t:
                myturtle.up()
                myturtle.hideturtle()
            else:
                myturtle.showturtle()
                myturtle.down()
            myturtle.setposition(h + 2*a*i, k + a * math.pow(i, 2))
            i += 1/8


def hyperbola(a, b, h=None, k=None):
    myturtle = turtle.Turtle()
    if h is None:
        h = 0
    if k is None:
        k = 0

    if a > b:
        for i in range(64):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+a*(1/math.cos(i/10)), k+b*math.tan(i/10))

    elif a == b:
        for i in range(64):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+a*(1/math.cos(i/10)), k+a*math.tan(i/10))

    elif b > a:
        for i in range(64):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+b*math.tan(i/10), k+a*(1/math.cos(i/10)))


def cardioid(a, orientation, h=None, k=None, angle=None, angle_unit=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0
    # Angle unit can be degree or radian

    if angle is None:
        angle = 360
        converted_angle = angle * 0.875

    if angle_unit == 'd' or angle_unit is None:
        converted_angle = angle * 0.875

    # We are multiplying by 0.875 because for making a complete cardioid we are plotting 315 pts according
    # to our parametric angle value

    elif angle_unit == "r":
        converted_angle = (angle * 0.875 * (180/math.pi))
    # Converting radian to degrees.

    if orientation == 'x':
        for i in range(int(converted_angle)+1):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+a*math.cos(i/50)*(1-math.cos(i/50)), k+a*math.sin(i/50)*(1-math.cos(i/50)))

    elif orientation == 'y':
        for i in range(int(converted_angle)+1):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+a*math.sin(i/50)*(1-math.cos(i/50)), k+a*math.cos(i/50)*(1-math.cos(i/50)))


def heart(a, b, orientation, h=None, k=None, angle=None, angle_unit=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0
    # Angle unit can be degree or radian

    if angle is None:
        angle = 360
        converted_angle = angle * 0.875

    if angle_unit == 'd' or angle_unit is None:
        converted_angle = angle * 0.875

    # We are multiplying by 0.875 because for making a complete cardioid we are plotting 315 pts according
    # to our parametric angle value

    elif angle_unit == "r":
        converted_angle = (angle * 0.875 * (180/math.pi))
    # Converting radian to degrees.

    if orientation == 'y':
        i = 0
        while i <= converted_angle:
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h+a*(16*math.pow(math.sin(i/50), 3)), k+b*(13*math.cos(i/50)-5*math.cos(2*(i/50))-2*math.cos(3*(i/50))
                                 - math.cos(4*(i/50))))
            i += 1

    elif orientation == 'x':
        i = 0
        while i <= converted_angle:
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(k+b*(13*math.cos(i/50)-5*math.cos(2*(i/50))-2*math.cos(3*(i/50))
                                 - math.cos(4*(i/50))), h+a*(16*math.pow(math.sin(i/50), 3)))
            i += 1


def butterfly(a, b, n=None, h=None, k=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0
    if n is None:
        n = 602

    for i in range(n+1):
        if i == 0:
            myturtle.up()
        else:
            myturtle.down()
        myturtle.setposition(h + a*math.sin(i/30)*(math.exp(math.cos(i/30)) - 2*math.cos((4*i)/30) - math.pow(math.sin(i/360), 5))
                             , k + b*math.cos(i/30)*(math.exp(math.cos(i/30)) - 2*math.cos((4*i)/30) - math.pow(math.sin(i/360), 5)))


def leminiscate(a, orientation, angle=None, angle_unit=None, h=None, k=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0
    # Angle unit can be degree or radian
    if angle is None:
        angle = 360
        converted_angle = angle * 0.875

    if angle_unit == 'd' or angle_unit is None:
        converted_angle = angle * 0.875

    # We are multiplying by 0.875 because for making a complete lemniscate we are plotting 315 pts according
    # to our parametric angle value

    elif angle_unit == "r":
        converted_angle = (angle * 0.875 * (180 / math.pi))
    # Converting radian to degrees.

    if orientation == 'x':
        for i in range(int(converted_angle)+1):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h + (a * math.cos(i/50))/(1 + math.pow(math.sin(i/50), 2)), k + (a * math.sin(i/50) * math.cos(i/50))/(1 + math.pow(math.sin(i/50), 2)))

    elif orientation == 'y':
        for i in range(int(converted_angle)+1):
            if i == 0:
                myturtle.up()
            else:
                myturtle.down()
            myturtle.setposition(h + (a * math.sin(i/50) * math.cos(i/50))/(1 + math.pow(math.sin(i/50), 2)), k + (a * math.cos(i/50))/(1 + math.pow(math.sin(i/50), 2)))


def hypocycloid(a, b, no_of_loops=None, h=None, k=None):
    myturtle = turtle.Turtle()
    if h is None:
        h = 0
    if k is None:
        k = 0

    if a % b == 0:
        no_loops = 189

    elif a % b != 0:
        # If ratio of radius of the outer circle with inner circle forming these set of curves is a fraction
        if b == 3 or b % 3 == 0:
            no_loops = 600

        elif b == 4 or b % 4 == 0:
            no_loops = 800

        elif b == 5 or b % 5 == 0:
            no_loops = 1000

        elif b == 7 or b % 7 == 0:
            no_loops = 1400

        else:
            no_loops = 100

    if no_of_loops is None:
        no_of_loops = no_loops

    for i in range(no_of_loops+1):
        if i == 0:
            myturtle.up()
        else:
            myturtle.down()
        myturtle.setposition(h + b*((a/b-1)*math.cos(i/30)-math.cos((a/b-1)*(i/30))), k + b*((a/b-1)*math.sin(i/30)+math.sin((a/b-1)*(i/30))))


def epitrochoid(a, b, ht, no_of_loops=None, h=None, k=None):
    myturtle = turtle.Turtle()

    if h is None:
        h = 0
    if k is None:
        k = 0

    if a % b == 0:
        no_of_loops = 315

    elif a % b != 0:
        if no_of_loops is None:
            no_of_loops = 315
        # If user has not given no of loops then taking default value for no of loops

    for i in range(no_of_loops+1):
        if i == 0:
            myturtle.up()

        else:
            myturtle.down()
        myturtle.setposition(h+(a+b)*math.cos(i/50)-ht*math.cos((i/50)*((a+b)/b)), k+(a+b)*math.sin(i/50)-ht*math.sin((i/50)*((a+b)/b)))


