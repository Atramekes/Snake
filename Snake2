from tkinter import *
from random import randint
    
class Grid(object):
#这个对象不是个实体对象，它用来布置所有物体（蛇的身体或者食物等）
    def __init__(self,master=None,window_width=800,window_height=600,grid_width=20,offset=10): #width=50
    #window是整个游戏画面的长度和宽度，master=None表示每个物体都是顶层窗口，offset表示窗口边缘留出的空间
        self.height = window_height  
        self.width = window_width  
        self.grid_width = grid_width  
        self.offset = offset  
        self.grid_x = self.width//self.grid_width
        #坐标的单位等于每个物体的宽（长）度/整个游戏画面的宽（长）度
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
    def grid_list(self):
        #生成坐标系
        grid_list = []  
        for y in range(0,int(self.grid_y)):  
            for x in range(0,int(self.grid_x)):  
                grid_list.append((x,y))  
        self.grid_list = grid_list
        #将生成的坐标系赋值给自己
        
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
        self.grid.draw(self.pos,self.color)
        #绘制出食物

class Snake(object):
#蛇
    def __init__(self, Grid):  
        self.grid = Grid  
        self.body = [(self.grid.grid_x-5,self.grid.grid_y-7),(self.grid.grid_x-5,self.grid.grid_y-6),(self.grid.grid_x-5,self.grid.grid_y-5)]
        #设定小蛇的初始长度和身体的位置
        self.direction = "Up"
        #设定小蛇的初始朝向
        self.status = ['stop','run']
        #小蛇有两种状态：跑啊跑啊我的骄傲放纵，或者我只想一条蛇安静一会儿
        self.speed = 100
        #设定两小蛇的初始速度，这个数值其实是频率，即这个数字越小，小蛇移动越快
        self.color = "blue"          
        self.gameover = False  
        self.score = 0
    def available_grid(self):  
        return [i for i in self.grid.grid_list if (i not in self.body[2:]) and (i not in snakegame.snake2.body)]
        #设定小蛇合法的移动范围：身体外、画面内
    def change_direction(self, direction):
        #改变方向
        self.direction = direction  
    def display(self):  
        for (x,y) in self.body:  
            self.grid.draw((x,y),self.color)
        #将身体显示出来
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
        #小蛇的身体用列表（其实是队列）来保存，第一项表示头，最后一项就是“尾巴”
        if snakegame.food.pos == head:
        #如果吃到了食物   
            snakegame.display_food()  
            self.score += 1
        else:
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
            self.grid.draw(new,color=self.color)
            #否则，移动有效，小蛇前进一步


class Snake2(object):
#蛇2
    def __init__(self, Grid):  
        self.grid = Grid
        self.body = [(5,5),(5,4),(5,3)]
        #设定小蛇的初始长度和身体的位置
        self.direction = "Down"
        #设定小蛇的初始朝向
        self.status = ['stop','run']
        #小蛇有两种状态：跑啊跑啊我的骄傲放纵，或者我只想一条蛇安静一会儿
        self.color = "grey"          
        self.gameover = False  
        self.score = 0
    def available_grid(self):  
        return [i for i in self.grid.grid_list if (i not in self.body[2:]) and (i not in snakegame.snake.body)]
        #设定小蛇合法的移动范围：身体外、画面内
    def change_direction(self, direction):
        #改变方向
        self.direction = direction  
    def display(self):  
        for (x,y) in self.body:  
            self.grid.draw((x,y),self.color)
        #将身体显示出来
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
        #小蛇的身体用列表（其实是队列）来保存，第一项表示头，最后一项就是“尾巴”
        if snakegame.food.pos == head:
        #如果吃到了食物   
            snakegame.display_food()  
            self.score += 1
        else:
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
            self.grid.draw(new,color=self.color)
            #否则，移动有效，小蛇前进一步

class Game(Frame):  
    def __init__(self,master=None): 
        Frame.__init__(self, master)
        self.master = master
        self.grid = Grid(master=master) 
        self.snake = Snake(self.grid)
        self.snake2 = Snake2(self.grid)
        self.food = Food(self.grid)
        self.bind_all("<KeyRelease>", self.key_release)
        #读取用户键盘的输入，将结果绑定至key_release函数
        self.display_food()
        self.snake.display()
        self.snake2.display()
    def run(self):  
        if not self.snake.status[0] == 'stop':
            #移动状态下小蛇一直自动移动
            self.snake.move()
        if not self.snake2.status[0] == 'stop':
            #移动状态下小蛇一直自动移动
            self.snake2.move()  
        if self.snake.gameover == True:
            #游戏结束
            message =  messagebox.showinfo("Player2 wins!", "Player2 wins!\nYour scores are: %d vs %d" %(self.snake.score,self.snake2.score))  
            if message == 'ok':
                root.destroy()
                sys.exit()
        elif self.snake2.gameover == True:
            message =  messagebox.showinfo("Player1 wins!", "Player1 wins!\nYour scores are: %d vs %d" %(self.snake.score,self.snake2.score))  
            if message == 'ok':
                root.destroy()
                sys.exit()
        self.after(self.snake.speed,self.run)
        #给这个方法设定了延迟，以控制小蛇速度
    def key_release(self, event):
        key = event.keysym
        #获得用户按下的键
        key_dict = {"Up":"Down","Down":"Up","Left":"Right","Right":"Left"}
        key_dict2 = {"w":"s","s":"w","a":"d","d":"a"}
        key_dict3 = {"w":"Up","s":"Down","a":"Left","d":"Right"}
        key_dict4 = {"Up":"s","Down":"w","Left":"d","Right":"a"} 
        if key in key_dict and not key == key_dict[self.snake.direction]:
        #如果方向不与当前方向相反，则可以改方向
        #如果方向与当前相同，相当于没改
            if not self.snake.status[0] == 'stop':
                self.snake.change_direction(key) 
        elif key in key_dict2 and not key == key_dict4[self.snake2.direction]:
        #如果方向不与当前方向相反，则可以改方向
        #如果方向与当前相同，相当于没改
            if not self.snake2.status[0] == 'stop':
                self.snake2.change_direction(key_dict3[key])  
        elif key == 'p':  
            self.snake.status.reverse()
            self.snake2.status.reverse()
            #p键切换暂停/继续的游戏状态
    def display_food(self):
        #小蛇吃到食物后，要刷新一个新食物
        while(self.food.pos in self.snake.body) or (self.food.pos in self.snake2.body):
            self.food.set_pos()
            #刷新下一个食物
        self.food.display()

if __name__ == '__main__':
    root = Tk()  
    snakegame = Game(root)
    snakegame.run()  
    snakegame.mainloop()
