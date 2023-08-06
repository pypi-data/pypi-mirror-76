import turtle as t

'''Drawing coordinate system'''

def draw_cs():
    # 设置画笔
    t.speed(0)
    t.pensize(2)

    # 画x轴
    t.penup()
    t.goto(-300, 0)
    t.pendown()
    t.goto(300, 0)
    # 画x轴的箭头
    t.penup()
    t.goto(295, 5)
    t.pendown()
    t.goto(300, 0)
    t.goto(295, -5)
    # 画x轴的点
    for i in range(-250, 300, 50):
        # 画点
        t.penup()
        t.goto(i, 10)
        t.pendown()
        t.goto(i, 0)
        # 画字
        t.penup()
        if i == 0:  # 对0的处理
            t.goto(i - 10, -25)
            t.write(i, align='center')
        else:
            t.goto(i, -25)
            t.write(i, align='center')
        t.pendown()
    # 画x轴的X
    t.penup()
    t.goto(290, -30)
    t.pendown()
    t.write('x', font=("Arial", 16))

    # 画y轴
    t.penup()
    t.goto(0, -300)
    t.pendown()
    t.goto(0, 300)
    # 画y轴的箭头
    t.penup()
    t.goto(-5, 295)
    t.pendown()
    t.goto(0, 300)
    t.goto(5, 295)

    # 画y轴的点
    for i in range(-250, 300, 50):
        # 画点
        t.penup()
        t.goto(10, i)
        t.pendown()
        t.goto(0, i)
        # 画字
        t.penup()
        if i == 0:  # 对0的处理
            pass
        else:
            t.goto(-25, i - 5)
            t.write(i, align='center')
        t.pendown()
    # 画y轴的y
    t.penup()
    t.goto(-30, 280)
    t.pendown()
    t.write('y', font=("Arial", 16))

    #恢复初始位置
    t.penup()
    t.goto(0,0)
    t.pendown()
    t.pensize(1)

if __name__ == '__main__':
    draw_cs()
    t.mainloop()
