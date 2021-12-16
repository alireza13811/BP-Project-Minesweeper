
from tkinter import *
from threading import Timer
import random

root = Tk()

error = '#871a2a'
success = '#008523'
open_program = True
number_of_flags = 0
elements_list = []
player_name = ''

class Board:
    def __init__(self,x_dimension,y_dimension,bombs):
        self.x = x_dimension
        self.y = y_dimension
        self.bombs = bombs
        self.bombs_list = []
        self.board = []
        self.zeros_list = []
        self.zero_numbers = []
        self.generate_zero_list()
    def bombs_position(self):
        i = 0
        columns = [0 for _ in range(self.x)]
        x_dimension = self.x
        y_dimension = self.y
        while i < self.bombs:
            number = random.randint(0,x_dimension*y_dimension-1)
            index = number%x_dimension
            if columns[index] > 2 or number in self.bombs_list:
                continue
            columns[index] += 1
            self.bombs_list.append(number)
            i += 1
    def raw_board(self):
        self.bombs_position()
        i =0
        x_dimension = self.x
        y_dimension = self.y
        for _ in range(y_dimension):
            list2 = []
            for _ in range(x_dimension):
                if i in self.bombs_list:
                    list2.append(-1)
                else:
                    list2.append(0)
                i += 1
            self.board.append(list2)
    def processing(self):
        self.raw_board()
        board = self.board
        for i in range(self.y):
            for j in range(self.x):
                flag = True
                if board[i][j] == -1:
                    continue
                number_of_bombs = 0
                if i > 0:
                    if board[i-1][j] == -1:
                        number_of_bombs += 1
                    if j > 0 :
                        if board[i-1][j-1] == -1:
                            number_of_bombs += 1
                    if j < self.x - 1:
                        if board[i-1][j+1] == -1:
                            number_of_bombs += 1
                if j < self.x - 1:
                    
                    if board[i][j+1] == -1:
                        number_of_bombs += 1
                if j > 0:
                    if board[i][j-1] == -1:
                        number_of_bombs += 1
                if i < self.y - 1:
                    if board[i+1][j] == -1:
                        number_of_bombs += 1
                    if j > 0:
                        if board[i+1][j-1] == -1:
                            number_of_bombs += 1
                    if j < self.x - 1:
                        if board[i+1][j+1] == -1:
                            number_of_bombs += 1
                if number_of_bombs == 0:
                    x = 0
                    if i > 0:
                        if board[i-1][j] == 0:
                            self.zeros_list[i][j].update(self.zeros_list[i-1][j])
                            x += 1
                            flag = False
                    if j > 0:
                        if board[i][j-1] == 0:
                            self.zeros_list[i][j].update(self.zeros_list[i][j-1])
                            x += 1
                            flag = False
                    
                    if flag:
                        number = random.randint(1,82)
                        while number in self.zero_numbers:
                            number = random.randint(1,82)
                        self.zeros_list[i][j].add(number)
                        self.zero_numbers.append(number)
                    elif x == 2:
                        if i > 0:
                            self.zeros_list[i-1][j].update(self.zeros_list[i][j])
                        if j > 0:
                            self.zeros_list[i][j-1].update(self.zeros_list[i][j])
                self.board[i][j] = number_of_bombs

    def show_number(self,index,element,frame):
        n = 0
        if element['bg'] == 'white' or not open_program or element['text'] == '\u2690':
            return
        for i in range(self.y):
            for j in range(self.x):
                if n == index:
                    element['bg'] = 'white'
                    if self.board[i][j] == -1:
                        element['text'] = '\u273A'
                        element['fg'] = 'black'
                        self.show_board()
                        self.game_lost(frame)
                    else:
                        number = self.board[i][j]
                        element['text'] = number
                        if number == 0:
                            self.zero_box(element,i,j)
                        elif number == 1:
                            element['fg'] = 'blue'
                        elif number == 2:
                            element['fg'] = 'green'
                        else:
                            element['fg'] = 'red'
                    return
                n += 1
    def zero_box(self,element,i1,j1):
        code = self.zeros_list[i1][j1]
        
        element['text'] = 0
        element['bg'] = 'white'
        element['fg'] = 'black'
        for item in code:
            for i in range(self.y):
                for j in range(self.x):
                    if item in self.zeros_list[i][j] :
                        if not self.zeros_list[i][j].issubset(code):
                            self.zero_box(elements_list[i][j],i,j)
                            continue
                        element = elements_list[i][j]
                        element['text'] = 0
                        element['bg'] = 'white'
                        element['fg'] = 'black'
    def generate_zero_list(self):
        for i in range(self.y):
            list1 = []
            for j in range(self.x):
                list1.append(set())   
            self.zeros_list.append(list1)
    def show_board(self):
        for i in range(self.y):
            for j in range(self.x):  
                element = elements_list[i][j]
                number = self.board[i][j]
                if element['bg'] == 'white' and number != -1:
                    continue
                if number == -1:
                    if element['text'] == '\u2690':
                        element['fg'] = 'green'
                    else:
                        element['text'] = '\u273A'
                        element['fg'] = 'red'
                    element['bg'] = '#393b39'
                elif element['text'] == '\u2690':
                    element['text'] = '\u2716'
                    element['fg'] = 'red'
    def timer(self,remaining_time,r,frame):
        if open_program and remaining_time>=1:
            minutes = remaining_time // 60
            secondes = remaining_time % 60
            t = Timer(1, lambda: self.timer(remaining_time,r,frame))
            t.start() 
            remaining_time -= 1
            r["text"] = f'Remaining time: {minutes}m, {secondes}s'
        elif remaining_time == 0:
            r["text"] = f'Remaining time: 0m, 0s'
            t = Timer(1, lambda: self.show_board())
            t.start() 
            t2 = Timer(1, lambda: self.game_lost(frame))
            t2.start()
    def change(self,l,element,frame):
        global number_of_flags
        if not open_program or element['bg'] == 'white':
            return
        text = element['text']
        if not text:
            if number_of_flags > 0:
                element['text'] = '\u2690'
                number_of_flags -= 1
                l["text"] = f'Number of flags: {number_of_flags}'
            else:
                show_message("You don't have any flags!",error)
        elif text == '\u2690':
            element['text'] = ''
            number_of_flags += 1
            l['text'] = f'Number of flags: {number_of_flags}'
        if number_of_flags == 0 and open_program:
            flag = True
            for i in range(self.y):
                for j in range(self.x):
                    x = elements_list[i][j]['text']
                    y = self.board[i][j]
                    if elements_list[i][j]['text'] == '\u2690' and self.board[i][j] != -1 :
                        flag = False
                        break
            if flag:
                self.game_won(frame)

    def game_lost(self,frame):
        global open_program
        open_program = False
        self.final(frame,False)
    def game_won(self,frame):
        global open_program
        open_program = False
        self.final(frame,True)
    def final(self,frame,win):
        for child in frame.winfo_children():
            child.destroy()
        if win:
            text = 'YOU WON'
        else:
            text = 'YOU LOST'
        frame['bg'] = '#ad8b00'
        l = Label(frame, text=text,height=5, bg= '#ad8b00',font=('Arial',13,'bold'))
        l.pack(side=TOP)
        e = Button(frame,text='Rematch',width=20,fg='white',bg='#006b00',font=('Arial',12,'bold'),command=play_game_page)
        e.pack(side=LEFT)
        e2 = Button(frame,text='Exit',width=20,fg='white',bg='#006b00',font=('Arial',12,'bold'),command=quit)
        e2.pack(side=RIGHT)
        with open('database_game.txt','a') as database:
            data = ''
            for i in range(self.y):
                for j in range(self.x):
                    data += ','
                    data += str(self.board[i][j])
            database.write(player_name + '\n') 
            string = str(int(win))+','+str(self.y)+','+str(self.x)+ data + '\n'
            database.write(string)
        with open('database.txt','r') as database:
            data = database.readlines()
            i = 0
            for item in data:
                row = item.split(',')
                name2 = row[0]
                if player_name == name2:
                    password = row[1]
                    wins = int(row[2])
                    loses = int(row[3])
                    if win:
                        wins += 1
                        data[i] = player_name + ',' + password + ',' + str(wins) + ',' + str(loses) + '\n'
                    else:
                        loses += 1
                        data[i] = player_name + ',' + password + ',' + str(wins) + ',' + str(loses) + '\n'
                    break
                i += 1
        with open('database.txt','w') as database:
            database.writelines(data)

#--------------------------------------PAGES---------------------------------------------
def main_page():
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text='Welcome to the MINESWEEPER game',height=5, bg= "#61042e",font=('Arial',14,'bold'))
    l.pack(side=TOP,padx= 20)
    
    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text='Do you have acount?',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l.pack(side=LEFT,padx=40)
    v = IntVar()

    r1 = Radiobutton(frame1, text='YES',variable=v, value=1,bg='#8884e3')
    r2 = Radiobutton(frame1, text='NO', variable=v, value=0,bg='#8884e3')
    r1.pack(side=LEFT,anchor=W,padx=20)
    r2.pack(side=RIGHT,anchor=W,padx=20)
    b = Button(root, text='Continue', width=55,bg='#040042',fg='white',command=lambda : check(v))
    b.pack()

def login_page():
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text='Please login to your account',height=5, bg= "#61042e",font=('Arial',12,'bold'))
    l.pack(side=TOP,padx= 20)

    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text='User name: ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l.grid(row=0,padx=10)
    l2 = Label(frame1, text='Password:  ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l2.grid(row=1,padx=10)
    e1 = Entry(frame1)
    e2 = Entry(frame1)
    e1.grid(row=0,column=1,padx=20)
    e2.grid(row=1,column=1,padx=20)
    b = Button(root, text='Continue', width=37,bg='#040042',fg='white',command=lambda : login(e1.get(),e2.get()))
    b2 = Button(root, text="Don't have any account? create", width=37,bg='#040042',fg='white',command=lambda : create_acc_page())
    b.pack()
    b2.pack()

def create_acc_page():
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text='Please create your account',height=5, bg= "#61042e",font=('Arial',12,'bold'))
    l.pack(side=TOP,padx= 43)

    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text='User name: ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l.grid(row=0,padx=10)
    l2 = Label(frame1, text='Password:  ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l2.grid(row=1,padx=10)
    l3 = Label(frame1, text='Repeat password:  ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l3.grid(row=2,padx=10)
    e1 = Entry(frame1)
    e2 = Entry(frame1)
    e3 = Entry(frame1)
    e1.grid(row=0,column=1,padx=15)
    e2.grid(row=1,column=1,padx=15)
    e3.grid(row=2,column=1,padx=15)
    b = Button(root, text='Continue', width=42,bg='#040042',fg='white',command=lambda : create_acc(e1.get(),e2.get(),e3.get()))
    b2 = Button(root, text='Already have an account? login', width=42,bg='#040042',fg='white',command=lambda : login_page())
    b.pack()
    b2.pack()

def acc_page(name):
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    string = f'{name} welcome to your account'
    l = Label(frame2, text=string,height=5, bg= "#61042e",font=('Arial',12,'bold'))
    l.pack(side=TOP,padx= 43)
    
    with open('database.txt','r') as database:
        data = database.readlines()
        for item in data:
            row = item.split(',')
            name2 = row[0]
            if name == name2:
                wins = row[2]
                loses = row[3][:-1]
                break

    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text=f'Number of wins: {wins}',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l.pack(padx=16,side=LEFT)
    l2 = Label(frame1, text=f'Number of loses: {loses}',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l2.pack(padx=16,side=RIGHT)
    b = Button(root, text='Change name', width=42,bg='#040042',fg='white',command= lambda : change_name_page(name))
    b2 = Button(root, text='History', width=42,bg='#040042',fg='white',command= lambda : show_history(name))
    b3 = Button(root, text='Play', width=42,bg='#040042',fg='white',command= play_game_page)
    b.pack()
    b2.pack()
    b3.pack()

def history_page(data):
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text='Here is your histoty',height=5, bg= "#61042e",font=('Arial',14,'bold'))
    l.pack(side=TOP,padx= 20)
    b = Button(root, text='Back', width=42,bg='#040042',fg='white',command= lambda : acc_page(player_name))
    b.pack()
    
    frame1 = Frame(root,relief= 'sunken',bg="#b38f00")
    frame1.pack(padx= 10)

    canvas = Canvas(root, borderwidth=0, background="#ffffff")
    frame3 = Frame(canvas, background="#ffffff")
    vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((4,4), window=frame3, anchor="nw")
    frame3.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
    
    for item in data:
        
        win = int(item[0])
        y_dimension = int(item[1])
        x_dimension = int(item[2])
        if win:
            text = "You won this game"
            color = "green"
        else:
            text = "You lost this game"
            color = 'red'
        frame5 = Frame(frame3)
        frame5.pack()
        l = Label(frame5, text=text,fg=color, bg= "#b38f00",font=('Arial',14,'bold'))
        l.pack(padx= 20)
        frame4 = Frame(frame3)
        frame4.pack(pady=10) 
        item = item[3:]
        board = [item[i:(i+x_dimension)] for i in range(0,len(item),x_dimension)]
        for i in range(y_dimension):
            for j in range(x_dimension):
                text = board[i][j]
                if int(text) == -1:
                    e = Button(frame4, width=5,height=2, text='\u273A',fg='red',bg='#393b39',font=('Arial',12,'bold'))
                    e.grid(row=i, column=j)
                    continue
                e = Button(frame4, width=5,height=2,text=text,fg='white',bg='#005fb8',font=('Arial',12,'bold'))
                e.grid(row=i, column=j)
    
def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

def change_name_page(name):
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text='Change name',height=5, bg= "#61042e",font=('Arial',12,'bold'))
    l.pack(side=TOP,padx= 58)

    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text='New name: ',height=5, bg= "#8884e3",font=('Arial',10,'bold'))
    l.grid(row=0,padx=5)
    e1 = Entry(frame1)
    e1.grid(row=0,column=1,padx=5)
    b = Button(root, text='Continue', width=31,bg='#040042',fg='white',command=lambda : change_name(name,e1.get()))
    b.pack()
    b2 = Button(root, text='Back to home page', width=31,bg='#040042',fg='white',command=lambda : acc_page(name))
    b2.pack()

def play_game_page():
    global open_program
    open_program = True
    delete_page()
    frame2 = Frame(root,relief= 'sunken',bg="#61042e")
    frame2.pack(padx= 10, pady=10)
    l = Label(frame2, text="Let's start the game",height=5,width=35, bg= "#61042e",font=('Arial',12,'bold'))
    l.pack(side=TOP)

    frame1 = Frame(root,relief= 'sunken',bg="#8884e3")
    frame1.pack(padx= 10)
    l = Label(frame1, text='The type of the game: ',height=5,width=20, bg= "#8884e3",font=('Arial',10,'bold'))
    l.pack(side=LEFT)

    v = IntVar()
    r1 = Radiobutton(frame1, text='9*9',variable=v, value=1,bg='#8884e3')
    r2 = Radiobutton(frame1, text='12*12', variable=v, value=2,bg='#8884e3')
    r3 = Radiobutton(frame1, text='15*20', variable=v, value=3,bg='#8884e3')
    r1.pack(side=RIGHT,padx=5)
    r2.pack(side=RIGHT,padx=5)
    r3.pack(side=RIGHT,padx=5)
    b = Button(root, text='Continue', width=49,bg='#040042',fg='white',command=lambda : processing(v.get()))
    b.pack()

def game_page(total_rows,total_columns,game_time):
    global elements_list
    delete_page()
    frame1 = Frame(root,relief= 'sunken',bg="#61042e",width=82)
    frame1.pack(padx= 10, pady=20)
    minutes = game_time // 60
    secondes = game_time % 60
    l = Label(frame1, text=f'Number of flags: {number_of_flags}',height=5, bg= "#61042e",font=('Arial',16,'bold'))
    r = Label(frame1, text=f'Remaining time: {minutes}m, {secondes}s',height=5, bg= "#61042e",font=('Arial',16,'bold'))
    l.pack(side=LEFT,padx= 10)
    r.pack(side=RIGHT,padx=10)
    frame = Frame(root)
    frame.pack()
    board = Board(total_columns,total_rows,number_of_flags)
    board.processing()
    board.timer(game_time,r,frame1)
    n = 0
    elements_list = []
    for i in range(total_rows):
        list1 = []
        for j in range(total_columns):   
            e = Button(frame, width=5,text='',fg='white',bg='#005fb8',font=('Arial',12,'bold'))
            e.grid(row=i, column=j)
            e.bind("<Button-1>",lambda a,e=e,n=n,f=frame1: board.show_number(n,e,f))
            e.bind("<Button-2>",lambda a,l=l,e=e,f=frame1: board.change(l,e,f))
            e.bind("<Button-3>",lambda a,l=l,e=e,f=frame1: board.change(l,e,f))
            list1.append(e)
            n += 1
        elements_list.append(list1)
    
#------------------------------------AUTHENTICATION--------------------------------------
def check(v):
    if v.get() == 1:
        delete_page()
        login_page()
    elif v.get() == 0:
        delete_page()
        create_acc_page()

def login(name,password):
    global player_name
    if not name:
        show_message('Please enter the username!',error)
        return
    elif not password:
        show_message('Please enter the password!',error)
        return
        
    check = check_name(name,password)
    if not check:
        show_message("Username or password is incorrect!",error)
        return
    else:
        player_name = name
        acc_page(name)
    
def create_acc(name,password,r_password):
    global player_name
    if not name:
        show_message('Please enter the username!',error)
        return
    elif not password:
        show_message('Please enter the password!',error)
        return
    elif not r_password:
        show_message('Please enter the repeated password!',error)
        return

    if check_name(name):
        show_message('This username has already taken!',error)
        return
    elif password != r_password:
        show_message('Password and the repeated password are different!',error)
        return

    with open('database.txt','a') as database:
        string = name +','+ password +','+ '0' + ',' + '0'+ '\n'
        database.write(string)
    player_name = name
    acc_page(name)

#-------------------------------------CONTROLLING------------------------------------------
def show_message(text1,color):
    frame = Frame(root,relief= 'sunken',bg=color)
    frame.pack(padx= 10, pady=10)
    m = Message(frame,text=text1,bg=color,width=100,font=('Arial',12))
    m.pack(pady=5)
    t = Timer(5, lambda: delete_element(frame))
    t.start() 

def delete_element(element):
    if open_program:
        element.destroy()

def delete_page():
    for child in root.winfo_children():
        child.destroy()

def check_name(name,password = False):
    with open("database.txt",'r') as database:
        data = database.readlines()
        for item in data:
            row = item.split(',')
            name2 = row[0]
            if password:
                password2 = row[1]
                if name == name2 and password == password2:
                    return True
            else:
                if name == name2:
                    return True
        else:
            return False

def change_name(name,n_name):
    global player_name
    if not n_name:
        show_message("Please enter the new name!",error)
        return
    with open('database.txt','r') as database:
        data = database.readlines()
        i = 0
        index = 0
        for item in data:
            row = item.split(',')
            name2 = row[0]
            if name2 == n_name:
                show_message("This username has already taken!",error)
                return
            if name == name2:
                index = i
            i += 1
        row = data[index].split(',')
        password = row[1]
        wins = row[2]
        loses = row[3][:-1]
        data[index] = n_name +','+ password +','+ wins + ',' + loses + '\n'
        player_name = n_name
    with open('database.txt','w') as database:
        database.write(''.join(data))
    with open('database_game.txt','r') as database:
        data = database.readlines()
        indexes = []
        i = 0
        while i < len(data):
            item = data[i]
            if name == item[:-1]:
                indexes.append(i)
            i += 2
        for item in indexes:
            data[item] = n_name + '\n'
    with open('database_game.txt','w') as database:
        database.writelines(data)
    acc_page(n_name)

def processing(dimension):
    global number_of_flags
    if dimension == 1:
        dimension_x = 9
        dimension_y = 9
        number_of_flags = 10  
    elif dimension == 2:
        dimension_x = 12
        dimension_y = 12
        number_of_flags = 20
    elif dimension == 3:
        dimension_x = 20
        dimension_y = 15
        number_of_flags = 40
    else:
        show_message("Please choose an option!",error)
        return
    remainig_time = dimension_x * dimension_y * 5
    game_page(dimension_y,dimension_x,remainig_time)

def show_number(l):
    l["text"] = '1'

def show_history(name):
    history = []
    with open('database_game.txt','r') as database:
        data = database.readlines()
        index = 0

        while index < len(data):
            name2 = data[index] 
            if name2[:-1] == name:
                row = data[index+1].split(',')
                history.append(row)
            index += 2
    if len(history) == 0:
        show_message('No data has found for this user!',error)
        return
    history_page(history)
        
#-------------------------------------MAIN FUNCTION----------------------------------------
def main():
    global open_program
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    database = open('database.txt','a')
    database.close()
    database = open('database_game.txt','a')
    database.close()
    root.title("MINESWEEPER")
    main_page()
    root.mainloop()
    open_program = False

if __name__ == '__main__':
    main()