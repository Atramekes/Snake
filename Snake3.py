from tkinter import *
from random import randint
import sys   

    
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
        self.grid_y = self.height//self.grid_width  
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
#神秘可持续增长永不变质绿色对蛇增长物体（食物）
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
#永动消化系统良好无污染不紧不慢蓝色小蛇（蛇）
    def __init__(self, Grid):  
        self.grid = Grid  
        self.body = [(self.grid.grid_x-5,self.grid.grid_y-7),(self.grid.grid_x-5,self.grid.grid_y-6),(self.grid.grid_x-5,self.grid.grid_y-5)]
        #设定小蛇的初始长度和身体的位置
        self.direction = "Up"
        #设定小蛇的初始朝向
        self.status = ['run','stop']
        #小蛇有两种状态：跑啊跑啊我的骄傲放纵，或者我只想一条蛇安静一会儿
        self.speed = 200
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
#永动消化系统良好无污染不紧不慢蓝色小蛇2（蛇2）
    def __init__(self, Grid):  
        self.grid = Grid
        self.body = [(5,5),(5,4),(5,3)]
        #设定小蛇的初始长度和身体的位置
        self.direction = "Down"
        #设定小蛇的初始朝向
        self.status = ['run','stop']
        self.speed = 200
        #小蛇有两种状态：跑啊跑啊我的骄傲放纵，或者我只想一条蛇安静一会儿
        self.color = "grey"          
        self.gameover = False  
        self.score = 0
        self.flag = False
        self.templist = []
        self.already_move = []
    def available_grid(self):  
        return [i for i in self.grid.grid_list if (i not in self.body[1:]) and (i not in snakegame.snake.body)]
        #设定小蛇合法的移动范围：身体外、画面内
    def deadly_move(self):
        #判断某一方向的走法是否立刻致命，返回一个致命列表
        head = self.body[0]
        deadly_direction=[]
        if not (head[0],head[1]-1) in self.available_grid():
            deadly_direction.append('Up')
        if not (head[0],head[1]+1) in self.available_grid():
            deadly_direction.append('Down')
        if not (head[0]-1,head[1]) in self.available_grid():
            deadly_direction.append('Left')
        if not (head[0]+1,head[1]) in self.available_grid():
            deadly_direction.append('Right')
        return deadly_direction
    def exist_way(self,position_a,position_b,alreadymove):
        if position_a == position_b:
            self.flag = True
        else:
            available_move=[
                (position_a[0],position_a[1]-1),(position_a[0],position_a[1]+1),(position_a[0]-1,position_a[1]),(position_a[0]+1,position_a[1])
                ]
            for move in available_move:
                if move in self.available_grid() and move not in alreadymove:
                    alreadymove.append(move)
                    self.exist_way(move,position_b,alreadymove)
                    alreadymove.remove(move)
    def dangerous_move(self):
        #判断某一方向的走法是否将来致命，返回一个致命列表
        head = self.body[0]
        dangerous_direction=[]
        self.flag = False
        self.exist_way((head[0], head[1]-1),self.body[len(self.body)-1],[])
        if not self.flag:
            dangerous_direction.append('Up')
        self.flag = False
        self.exist_way((head[0], head[1]+1),self.body[len(self.body)-1],[])
        if not self.flag:
            dangerous_direction.append('Down')
        self.flag = False
        self.exist_way((head[0]-1, head[1]),self.body[len(self.body)-1],[])
        if not self.flag:
            dangerous_direction.append('Left')
        self.flag = False
        self.exist_way((head[0]+1, head[1]),self.body[len(self.body)-1],[])
        if not self.flag:
            dangerous_direction.append('Right')
        return dangerous_direction
    def find_way_complicated(self,position_a,position_b,step,alreadymove):
        if position_a == position_b:
            self.templist.append(step)
        else:
            available_move=[
                (position_a[0],position_a[1]-1),(position_a[0],position_a[1]+1),(position_a[0]-1,position_a[1]),(position_a[0]+1,position_a[1])
                ]
            for move in available_move:
                if move in self.available_grid() and move not in alreadymove:
                    alreadymove.append(move)
                    self.find_way(move,position_b,step+1,alreadymove)
                    alreadymove.remove(move)
    def choose_derection_simple(self):
        head = self.body[0]
        x=head[0]
        y=head[1]
        food_x=snakegame.food.pos[0]
        food_y=snakegame.food.pos[1]
        if abs(x - food_x) < abs(y - food_y):
            if y < food_y:
                half=['Down','Up']
            else:
                half=['Up','Down']
            if x < food_x:
                left=['Right','Left']
            else:
                left=['Left','Right']
        else:
            if x < food_x:
                half=['Right','Left']
            else:
                half=['Left','Right']
            if y < food_y:
                left=['Down','Up']
            else:
                left=['Up','Down']
        return [half[0]]+left+[half[1]]
    def choose_derection_complicated(self):
        #欲选出一个最优方向返回一个优先级列表
        head = self.body[0]
        priority=[]
        self.templist = []
        self.already_move = []
        self.find_way_complicated((head[0], head[1]-1),snakegame.food.pos,0,[])
        if self.templist == []:
            up_step = [99999,'Up']
        else:
            up_step = [min(self.templist),'Up']
        self.templist = []
        self.already_move = []
        self.find_way_complicated((head[0], head[1]+1),snakegame.food.pos,0,[])
        if self.templist == []:
            down_step = [99999,'Down']
        else:
            down_step = [min(self.templist),'Down']
        self.templist = []
        self.already_move = []
        self.find_way_complicated((head[0]-1, head[1]),snakegame.food.pos,0,[])
        if self.templist == []:
            left_step = [99999,'left']
        else:
            left_step = [min(self.templist),'Left']
        self.templist = []
        self.already_move = []
        self._way_complicated((head[0]+1, head[1]),snakegame.food.pos,0,[])
        if self.templist == []:
            right_step = [99999,'Right']
        else:
            right_step = [min(self.templist),'Right']
        steps = [up_step,down_step,left_step,right_step]
        if steps[0][0] > steps[1][0]:
            temp = steps[0][0]
            steps[0][0] = steps[1][0]
            steps[1][0] = temp
        if steps[2][0] > steps[3][0]:
            temp = steps[2][0]
            steps[2][0] = steps[3][0]
            steps[3][0] = temp
        if steps[1][0] < steps[2][0]:
            return [steps[0][1],steps[1][1],steps[2][1],steps[3][1]]
        else:
            temp = steps[1][0]
            steps[1][0] = steps[2][0]
            steps[2][0] = temp
            if steps[0][0] > steps[1][0]:
                temp = steps[0][0]
                steps[0][0] = steps[1][0]
                steps[1][0] = temp
            if steps[2][0] > steps[3][0]:
                temp = steps[2][0]
                steps[2][0] = steps[3][0]
                steps[3][0] = temp
            return [steps[0][1],steps[1][1],steps[2][1],steps[3][1]]
    def change_direction(self):
        if len(self.body) > self.grid.grid_x * self.grid.grid_y // 4:
            choices=self.choose_derection_complicated()
        else:
            choices=self.choose_derection_simple()
        direction = choices[3]
        if choices[2] not in self.deadly_move():
            direction = choices[2]
        if choices[1] not in self.deadly_move():
            direction = choices[1]
        if choices[0] not in self.deadly_move():
            direction = choices[0]
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
        if key in key_dict and not key == key_dict[self.snake.direction]:
        #如果方向不与当前方向相反，则可以改方向
        #如果方向与当前相同，相当于没改
            if not self.snake.status[0] == 'stop':
                self.snake.change_direction(key) 
        elif key == 'p':  
            self.snake.status.reverse()
            self.snake2.status.reverse()
            #p键切换暂停/继续的游戏状态
    def ai(self):
        if not self.snake.status[0] == 'stop':
            #移动状态下小蛇一直自动移动
            self.snake2.change_direction()
            self.snake2.move()
        self.after(self.snake2.speed,self.ai)
    def display_food(self):
        #小蛇吃到食物后，要刷新一个新食物
        while(self.food.pos in self.snake.body) or (self.food.pos in self.snake2.body):
            self.food.set_pos()
                #刷新下一个食物
                #如果不巧（或者说比较幸运）刷新在了身体内，再刷新一次
        self.food.display()

if __name__ == '__main__':
    sys.setrecursionlimit(10000)
    root = Tk()  
    snakegame = Game(root)
    snakegame.run()
    snakegame.ai()  
    snakegame.mainloop()
