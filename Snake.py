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
    def drawoval(self, pos, color):
        #绘制出某个圆圆的物体
        x = pos[0]*self.grid_width + self.offset
        y = pos[1]*self.grid_width + self.offset
        self.canvas.create_oval( 
            x, y, x+self.grid_width, y+self.grid_width,fill=color,outline=self.bg
            )
    def grid_list(self):
        #生成坐标系
        grid_list = []  
        for y in range(0,int(self.grid_y)):  
            for x in range(0,int(self.grid_x)):  
                grid_list.append((x,y))  
        self.grid_list = grid_list
        #将生成的坐标系赋值给自己

class Wall(object):
#墙
    def __init__(self, Grid):
        self.grid = Grid  
        self.color = "black"
        self.tot = int(self.grid.grid_x * self.grid.grid_y)
        self.allpos = []
        #self.load()
        self.random_pos(50)
        #以0.05的密度绘制墙壁,可以修改此行来更改墙壁的位置
        self.display()
    def load(self):
        with open('save','r') as data:
            for line in data:
                x = ''
                y = ''
                flag = False
                for t in line:
                    if not t == ',':
                        if not t == '\n':
                            if flag:
                                y += t
                            else:
                                x += t
                        else:
                            self.allpos.append((int(x),int(y)))
                    else:
                        flag = True
                self.allpos.append((int(x),int(y)))
        
    def random_pos(self,rate):
        for i in range(0,int(self.grid.grid_x)):
            for j in range(0,int(self.grid.grid_y)):
                temp = randint(1,1000)
                if temp < rate and (i > 4 or j > 3):
                #小蛇初始位置附近不设墙壁
                    self.allpos.append((i,j))
    def display(self):
        for position in self.allpos:
            self.grid.draw(position,self.color)
            #绘制出墙

class Food(object):
#食物
    def __init__(self, Grid):  
        self.grid = Grid  
        self.color = "green"          
        self.set_pos()  
    def set_pos(self):
    #设置食物的刷新位置
        x = randint(0,self.grid.grid_x - 1)  
        y = randint(0,self.grid.grid_y - 1)
        self.pos = (x, y)
    def display(self):  
        self.grid.drawoval(self.pos,self.color)
        #绘制出食物

class Gold(object):
#金币
    def __init__(self, Grid):  
        self.grid = Grid  
        self.color = "yellow"          
        self.set_pos()  
    def set_pos(self):
        x = randint(0,self.grid.grid_x - 1)  
        y = randint(0,self.grid.grid_y - 1)
        self.pos = (x, y)
    def display(self):  
        self.grid.drawoval(self.pos,self.color)
        #绘制出金币

class Snake(object):
#蛇
    def __init__(self, Grid):  
        self.grid = Grid  
        self.body = [(3,1),(2,1),(1,1)]
        #设定小蛇的初始长度和身体的位置
        self.direction = "Right"
        #设定小蛇的初始朝向
        self.status = ['stop','run']
        #小蛇有两种状态：跑啊跑啊我的骄傲放纵，或者我只想一条蛇安静一会儿
        self.speed = 200
        #设定小蛇的初始速度，这个数值其实是频率，即这个数字越小，小蛇移动越快
        self.color = "blue"          
        self.food = Food(self.grid)
        self.gold = Gold(self.grid)
        self.wall = Wall(self.grid)
        self.wallpos=[]
        self.display_food()
        self.display_gold()
        self.gameover = False  
        self.score = 0
        self.goldactive = False
    def available_grid(self):  
        return [i for i in self.grid.grid_list if ((i not in self.body[2:]) and (i not in self.wall.allpos))]
        #设定小蛇合法的移动范围：身体外、墙外、画面内
    def change_direction(self, direction):
        #改变方向
        self.direction = direction  
    def display(self):  
        for (x,y) in self.body:  
            self.grid.drawoval((x,y),self.color)
        #将身体显示出来
    def display_food(self):
        #小蛇吃到食物后，要刷新一个新食物
        while(self.food.pos in self.body or self.gold.pos == self.food.pos or self.food.pos in self.wall.allpos):
        #while语句用来保证刷新的食物不在小蛇体内，也不能和金币、墙重合
            self.food.set_pos()
            #刷新下一个食物
            #如果不巧刷新在了非法区域，再刷新一次
        self.food.display()    
    def display_gold(self):
        #刷新一个新金币
        self.gold.set_pos()
        while(self.gold.pos in self.body or self.gold.pos == self.food.pos or self.gold.pos in self.wall.allpos):
        #while语句用来保证刷新的金币不在小蛇体内，也不能和食物、墙重合
            self.gold.set_pos()
        self.gold.display()
    def hint(self):
        if self.status[0] == 'stop':
            self.grid.canvas.create_text(400,10,text='Press P to continue',fill='gray')
        else:
            self.grid.canvas.create_rectangle(250,0,550,20,fill='white',outline='white')
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
        #以上操作，先准备让小蛇的身体增加了一段长度
        #小蛇的身体用列表（队列）来保存，第一项表示头，最后一项就是“尾巴”
        if self.food.pos == head:
        #如果吃到了食物   
            self.display_food()  
            self.score += 1
            snakegame.renew_score()
            snakegame.hungry = 1000
            if self.speed > 3:
                self.speed -= 3
        else:
            if self.gold.pos == head and self.goldactive == False:
            #如果吃到了金币
                self.goldactive = True
                self.score += 5
                snakegame.renew_score()
            pop = self.body.pop()
            #由于身体长度不变，头前进一格，“尾巴”会变短
            self.grid.draw(pop,self.grid.bg)  
        self.body.insert(0,new)
        #将头前进的那一格加入身体的一部分
        if not new in self.available_grid():
            #如果新的位置，也就是小蛇的下一步走在了非法的位置（小蛇身体、边界等）
            #那么游戏结束
            self.status.reverse()              
            self.gameover = True  
        else:  
            self.grid.drawoval(new,color=self.color)
            #否则，移动有效，小蛇前进一步

class Game(Frame):  
    def __init__(self,master=None): 
        Frame.__init__(self, master)
        self.master = master
        self.grid = Grid(master=master) 
        self.snake = Snake(self.grid)
        self.bind_all("<KeyRelease>", self.key_release)
        #读取用户键盘的输入，将结果绑定至key_release函数
        self.snake.display()
        self.hungry = 1000
        self.snake.grid.canvas.create_text(400,10,text='Press P to start',fill='gray')
    def run(self):  
        if not self.snake.status[0] == 'stop':
            #移动状态下小蛇一直自动移动
            self.snake.move()
            self.hungry -= 5
        if self.hungry > 500:
            self.snake.color = "blue"
        elif self.hungry < 200:
            self.snake.color = "cyan"
        else:
            self.snake.color = "#1E90FF"
        if self.snake.gameover == True or self.hungry == 0:
            #游戏结束
            message =  messagebox.showinfo("Game Over", "Your score is: %d" % self.snake.score)  
            if message == 'ok':
                root.destroy()
                sys.exit()
        randomtime = randint(0,1000)
        if randomtime in range(10,20) and self.snake.goldactive:
            self.snake.display_gold()
            self.snake.goldactive = False
            #金币不定时刷新
            #只有当前没有金币才会刷新金币
        self.after(self.snake.speed,self.run)
        #给这个方法设定了延迟，以控制小蛇速度
    def key_release(self, event):
        key = event.keysym
        #获得用户按下的键
        key_dict = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}  
        if key in key_dict and not key == key_dict[self.snake.direction]:
        #如果方向不与当前方向相反，则可以改方向
        #如果方向与当前相同，相当于没改
            if not self.snake.status[0] == 'stop':
                self.snake.change_direction(key)  
        elif key == 'p':  
            self.snake.status.reverse()
            self.snake.hint()
            #p键切换暂停/继续的游戏状态
            #print(self.snake.wall.allpos)
            #测试bug用语
    def renew_score(self):
        self.hide_score()
        self.grid.canvas.create_text(400,630,text='Score:%d'%(self.snake.score),fill='gray')
    def hide_score(self):
        self.grid.canvas.create_rectangle(50,620,750,640,fill='white',outline='white')
if __name__ == '__main__':
    root = Tk()  
    snakegame = Game(root)
    snakegame.run()  
    snakegame.mainloop()
