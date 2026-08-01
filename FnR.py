import turtle
t = turtle.Turtle()
t.speed(0)

l_list = [120*(2**n) for n in range(0, -8, -1)]
clr_list = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']

#square function
def square(x, y, level):
    l = l_list[level]

    t.color(clr_list[level])

    t.penup()
    t.goto(x, y)

    t.pendown()
    if level < 3:
        t.setheading(20)
    else:
        t.setheading(-20)
    # draw square
    t.begin_fill()
    for _ in range(4):
        t.forward(l)
        t.left(90)
    t.end_fill()

    if level < 5:
        square(x + 9/8*l, y - 3/4*l, level + 1)
        square(x - 5/8*l, y - 3/4*l, level +1)

square(-100, -100, 0)

#clearing an making way for the tree
t.clear()

angle = 25

def branch(sz, level):
    if level > 0:

        if level == 1:
            t.color('green')
        else:
            t.color('brown')
       
        t.pensize(level)
        t.forward(sz)

        if level == 1:
            t.color('red')
            t.dot(5)

        t.right(angle)
        branch(0.8*sz, level - 1)

        t.right(-2*angle)
        branch(0.8*sz, level -1)
        t.right(angle)
        t.penup() #makes sure red doesnt override the other colors!
        t.forward(-sz)
        t.pendown()


t.clear()
t.penup()
t.goto(0, -150)
t.setheading(90)
t.pendown()

branch(100, 8)

turtle.mainloop()
