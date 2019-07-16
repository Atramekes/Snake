from tkinter import *
from random import randint 

class Grid(object):
#这个对象不是个实体对象，它用来布置所有物体（蛇的身体或者食物等）
    def __init__(self,master=None,window_width=800,window_height=600,grid_width=40,offset=20):
    #window是整个游戏画面的长度和宽度，master=None表示每个物体都是顶层窗口，offset表示窗口边缘留出的空间
        self.height = window_height  
        self.width = window_width  
        self.grid_width = grid_width  
        self.offset = offset  
        self.grid_x = self.width/self.grid_width
        #坐标的单位等于整个游戏画面的宽（长）度/每个物体的宽（长）度
        self.grid_y = self.height/self.grid_width  
        self.bg = "white"
        #背景颜色是白色
        self.canvas = Canvas(
            master, width=self.width+2*self.offset, height=self.height+2*self.offset, bg=self.bg
            )
        #用一个画布来装载所有物体。为了美观，画布的边缘留出一些距离（offset）
        self.canvas.pack()
        #呈现出画布
        self.grid_list()
        #生成坐标系
    def draw(self, pos, color):
        #绘制出某个物体
        x = pos[0]*self.grid_width + self.offset
        #读取x坐标，其值为名义x坐标乘以x坐标单位长度，再加上留空（offset）
        y = pos[1]*self.grid_width + self.offset
        #读取y坐标，其值为名义y坐标乘以y坐标单位长度，再加上留空（offset）
        self.canvas.create_rectangle( 
            x, y, x+self.grid_width, y+self.grid_width,fill=color,outline=self.bg
            )
        #将那个名义坐标（点）对应的实际坐标（一块区域）染色，颜色为对应物体的颜色
    def draw_snake(self, pos, color):
        x = pos[0]*self.grid_width + self.offset
        y = pos[1]*self.grid_width + self.offset
        self.canvas.create_rectangle( 
            x, y, x+self.grid_width, y+self.grid_width,fill=color,outline=self.bg
            )
        self.canvas.create_rectangle( 
            x+self.grid_width/8, y+self.grid_width/8, x+self.grid_width*7/8, y+self.grid_width*7/8,fill=self.bg,outline=color
            )
    def grid_list(self):
        #生成坐标系
        grid_list = []  
        for y in range(0,int(self.grid_y)):  
            for x in range(0,int(self.grid_x)):  
                grid_list.append((x,y))  
        self.grid_list = grid_list

class Wall(object):
    def __init__(self, Grid):
        self.grid = Grid  
        self.color = "black"
        self.tot = int(self.grid.grid_x * self.grid.grid_y)
        self.allpos = []
        self.display()
    def edit(self):
        x = snakegame.snake.body[0][0]
        y = snakegame.snake.body[0][1]
        if (x,y) in self.allpos:
            self.allpos.remove((x,y))
            self.grid.draw_snake((x,y),'#191970')
        else:
            self.allpos.append((x,y))
            self.display()
    def clear_all(self):
        while not self.allpos == []:
            self.grid.draw(self.allpos.pop(),'white')
        x = snakegame.snake.body[0][0]
        y = snakegame.snake.body[0][1]
        self.grid.draw_snake((x,y),'#191970')
    def display(self):
        for position in self.allpos:
            self.grid.draw(position,self.color)
    def save(self):
        output=open('save','w')
        w=str(self.allpos)
        w=w.replace(" ","").replace("[","").replace("]","")
        w=w.replace("),","\n").replace("(","").replace(")","")
        output.write(w)
        message =  messagebox.showinfo("Save", "Success!")

class Snake(object):
    def __init__(self, Grid):  
        self.grid = Grid  
        self.body = [(1,1)]
        self.speed = 200
        self.color = "#191970"
        self.direction = 'Up'
        self.wall = Wall(self.grid)
    def display(self):  
        for (x,y) in self.body:  
            self.grid.draw_snake((x,y),self.color)
        #将身体显示出来
    def available_grid(self):  
        return [i for i in self.grid.grid_list]
    def move(self):
        head = self.body[0]
        #指定小蛇的头
        if self.direction == 'Up':
            new = (head[0], head[1]-1)  
        elif self.direction == 'Down':  
            new = (head[0], head[1]+1)  
        elif self.direction == 'Left':  
            new = (head[0]-1,head[1])  
        else:  
            new = (head[0]+1,head[1])
        if new in self.available_grid():
            pop = self.body.pop()
            self.grid.draw_snake(pop,self.grid.bg)  
            self.body.insert(0,new)
            self.grid.draw_snake(new,color=self.color)
            self.wall.display()

class Game(Frame):  
    def __init__(self,master=None): 
        Frame.__init__(self, master)
        self.master = master
        self.grid = Grid(master=master) 
        self.snake = Snake(self.grid)
        self.bind_all("<KeyRelease>", self.key_release)
        #读取用户键盘的输入，将结果绑定至key_release函数
        self.snake.display()
        self.grid.canvas.create_text(400,10,text='Press Enter to create a Wall. Press s to save your work.',fill='gray')
        self.grid.canvas.create_text(400,630,text='Press shift-c to clear all.',fill='gray')
    def key_release(self, event):
        key = event.keysym
        #获得用户按下的键
        key_dict = ["Up","Down","Left","Right"]
        if key in key_dict:
            self.snake.direction = key
            self.snake.move() 
        if key == 'Return':
            self.snake.wall.edit()
        if key == 'C':
            self.snake.wall.clear_all()
        if key == 's':
            self.snake.wall.save()
        #print(key)
                                

if __name__ == '__main__':
    root = Tk()  
    snakegame = Game(root)
    snakegame.mainloop()
