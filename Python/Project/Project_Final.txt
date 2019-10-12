import tkinter as tk
from PIL import Image, ImageTk
from tkinter.ttk import *
from tkinter import simpledialog
import sqlite3
import tkinter.ttk as ttk
import tkinter.font as tkFont
#from tkinter import scrolledtext
from tkinter import messagebox
import time
import datetime

lf= ("Lucida Calligraphy", 50)
lf2= ("Lucida Calligraphy", 24)
lf3= ("Lucida Calligraphy", 14)
lf4 = ("Lucida Calligraphy",10)


class Mainwindow(tk.Tk):

    def __init__(self):                             # initalized main window

        ''' no need its just an convention
            args stand for arguments pass throungh variables
            kwargs stand for keyword arguments  pass throungh dictionary '''
        tk.Tk.__init__(self)                        # initalized Tkinter
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True) # fill fills in the limits & expand is beyond limits
        container.grid_rowconfigure(0, weight=10)
        container.grid_columnconfigure(0, weight=10)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew") # north south east west

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    orderlist = []
    banklist = []
    heading = ['Item','Price','Ouantity','Total']

    def recall(self,xi,xi1,yi,zi):                      #data1, data2 , tree , answer(qty)
        ai = 0
        total_value = 0 
        aaa = xi[0]                                     # Product name
        aab = xi[1]+xi[2]                               # Product-id + Sub-Product-id
        bbb = xi1[0]                                    # Quantity
        bbb1 = bbb[0]                                   # Selling Price
        ccc = bbb1 * zi                                 # Total = qty * price  
        ccd = (aaa,aab,bbb1,zi,ccc)                     # Pr_name, Pr_id, SP ,Qty, Total
        Mainwindow.orderlist.append(ccd)                
        
        for col in Mainwindow.heading:
            yi.heading(col,text=col.title())            # Creating Tile display for Headings
            yi.column(col, width=tkFont.Font().measure(col.title()))    # Adjusting it in a box

        while ai <len(Mainwindow.orderlist):
            x = Mainwindow.orderlist[ai]
            cce = (x[0],x[2],x[3],x[4])                 # Item , Price , Quantity , Total 
            total_value = total_value + x[4]
            yi.insert('', 'end', values=cce)
            yi.column(Mainwindow.heading[0],width=120)
            ai = ai+1
            listbx=tk.Label(self,text ='TOTAL                                  '+str(total_value),
                                width=39,height=3,bg='white',relief= tk.RAISED,font = 16)
            listbx.place(x=950,y=430)        

    def myy(self,x1,x2,x3):
        
        conn = sqlite3.connect('master.db')
        c = conn.cursor()
        if x1==1:
            answer = simpledialog.askinteger("Input", "Enter the Quantity",minvalue=1, maxvalue=100)
            if answer is None:
                self.destroy
            else:
                def select_my_table(answer,item_x,cd):
                    c.execute("SELECT Sub_r_name,Pr_id,Sub_pr_id FROM sub_product_id WHERE Sub_pr_id = (?) AND Pr_id = (?)",(item_x,cd))
                    data = c.fetchone()
                    c.execute("SELECT SP,Tax FROM pr_price WHERE Sub_pr_id = (?) AND Tax > (?)",(item_x,0))
                    data_2 = c.fetchall()
                    conn.commit()
                    tree = ttk.Treeview(self,columns = Mainwindow.heading,show = 'headings')
                    vsb = ttk.Scrollbar(orient="vertical",command=tree.yview)
                    tree.configure(yscrollcommand=vsb.set)
                    tree.place(x=950,y=200,height=230,width=340)
                    vsb.place(x=1290,y=200,height=230)
                    self.recall(data,data_2,tree,answer)
                select_my_table(answer,x2,x3)
        c.close()
        conn.close()

    def reset(self):
        del Mainwindow.orderlist[0:]
        tree = ttk.Treeview(self,columns = Mainwindow.heading,show = 'headings')
        vsb = ttk.Scrollbar(orient="vertical",command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.insert('', 'end', values=Mainwindow.orderlist)
        tree.place(x=950,y=200,width=340)
        vsb.place(x=1290,y=200,height=225)
        listbx=tk.Label(self,text ='TOTAL                                  '+str(0),
                                width=39,height=3,bg='white',relief= tk.RAISED,font = 16)
        listbx.place(x=950,y=430)  
        
    def popup(self):
        Popup(self)   

    def bank(self):
        Bank(self)

    def buy1(self,x,y):
        Mainwindow.banklist.append(x)
        Mainwindow.banklist.append(y)

    def buy(self,cc1):

        conn = sqlite3.connect('transaction.db')
        c = conn.cursor()
        c.execute("SELECT MAX(Bill_no) FROM Total_Sales")
        no = c.fetchone()
        #print(no)
        billno = no[0]
        #print(billno)
        billno=billno+1
        ai = 0
        unix = time.time()
        dt = str(datetime.datetime.fromtimestamp(unix).strftime('%d-%m-%y '))
        t = str(datetime.datetime.fromtimestamp(unix).strftime('%H:%M:%S'))
        #print(dt,t)
        aad1 = 0
        flag = 0

        while ai < len(Mainwindow.orderlist):
            aaa = Mainwindow.orderlist[ai]
            aad = aaa[4]                                    # individual value
            aad1 = aad1+aad
            ai=ai+1
        aae=aad1
        print(aae)

        def billinfo(billno,dt,t,c,conn):
            aad1 = 0
            ai = 0
            while ai < len(Mainwindow.orderlist):
            
                aaa = Mainwindow.orderlist[ai]
                aab = aaa[1]                    # Pr_cd
                aac = aaa[3]                    # total qty
                aad = aaa[4]                    # individual value
                aad1 = aad1+aad                 # total value
                c.execute("INSERT INTO Bill_info VALUES (?, ?, ?, ?, ?, ?, ?, ?)",('T12035', billno, 'T001', dt, t, aab, aac, aad))
                conn.commit()
                ai=ai+1

        if cc1==2:
            self.bank()
            try:
                cd_no = Mainwindow.banklist[0]
                bk_n = Mainwindow.banklist[1]
                del Mainwindow.banklist[0:]
            except IndexError:
                flag = 1
            if flag == 0:
                c.execute("INSERT INTO Total_Sales VALUES (?, ?, ?, ?, ?, ?, ?)",(billno,dt,t,aad1,cc1,cd_no,bk_n))
                conn.commit()
                billinfo(billno,dt,t,c,conn)

        else:
            c.execute("INSERT INTO Total_Sales (Bill_no,Date,Time,Amt,Cash_Card) VALUES(?, ?, ?, ?, ?)",(billno,dt,t,aad1,cc1))
            conn.commit()
            billinfo(billno,dt,t,c,conn)
                  
        c.close()
        conn.close()
        self.reset()

class Bank(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.geometry('300x150+300+300')
        label = tk.Label(self,height = self.winfo_screenheight(),width = self.winfo_screenwidth(),bg='LightBlue2',)
        label.place(x=0,y=0)
        tk.Label(self,bg='LightBlue2').grid(row=1)
        tk.Label(self,text="Card No : ",bg='LightBlue2',fg='blue4',font=lf3).grid(row=3)
        tk.Label(self,text="Bank name : ",bg='LightBlue2',fg='blue4',font=lf3).grid(row=5)
        tk.Label(self,bg='LightBlue2').grid(row=6)
        var = tk.IntVar()
        tk.Entry(self,textvariable=var).grid(row = 3,column = 2)
        var1 = tk.StringVar()
        tk.Entry(self, textvariable=var1).grid(row = 5,column = 2)
        B1 = tk.Button(self, text="Submit",width = 7,bg = 'khaki1',font=lf4,command=lambda:checkout(var.get(),var1.get()))
        B1.grid(row = 15,column = 0)
        B2 = tk.Button(self, text="Cancle",width = 7,bg = 'khaki1',font=lf4,command=lambda:rollbk())
        B2.grid(row = 15,column = 2)
 
        def checkout(x,y):
            self.destroy()
            master.buy1(x,y)

        def rollbk():
            self.destroy()
            master.popup()

        self.transient(master)              #set to be on top of the main window
        self.grab_set()                     #hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self)            #pause anything on the main window until this one closes (optional)


class Popup(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)

        self.geometry('300x80+300+300')
        label = tk.Label(self, text="How would you like to Pay",width = self.winfo_screenwidth(),bg='LightBlue2',fg='blue4',font=lf3)
        label.pack()
        tk.Label(self,height = self.winfo_screenheight(),width = self.winfo_screenwidth(),bg='LightBlue2').pack(side='bottom')
        B1 = tk.Button(self, text="Cash",width = 7,bg = 'khaki1',font=lf4,command=lambda:situation(1))
        B1.place(x = 35 ,y = 45)
        B2 = tk.Button(self, text="Card",width = 7,bg = 'khaki1',font=lf4,command=lambda:situation(2))
        B2.place(x = 120 ,y = 45)
        B2 = tk.Button(self, text="Cancle",width = 7,bg = 'khaki1',font=lf4,command=self.destroy)
        B2.place(x = 205 ,y = 45)

        def situation(x):
            if x==1:          
                self.destroy()
                master.buy(1)
                
            else:
                self.destroy()
                master.buy(2)
            
        self.transient(master)              #set to be on top of the main window
        self.grab_set()                     #hijack all commands from the master (clicks on the main window are ignored)
        master.wait_window(self)            #pause anything on the main window until this one closes (optional)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(),width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both') 
        
        ll2 = tk.Label(self,height = 50, width = 120,bg='white',fg='white')
        ll2.place(x=50,y=200) 

        ll3 = tk.Label(self,height = 50, width = 50,bg='white',fg='white')
        ll3.place(x=950,y=200) 

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render,width=130,bg='white')
        img.image = render
        img.place(x=30,y=20)

        load1 =Image.open("D:\\Python\\project_py\\mainburger.png")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\Beverages.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\coffee.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        load4 = Image.open("D:\\Python\\project_py\\Sweets.jpg")
        render4 = ImageTk.PhotoImage(load4)
        img4 = tk.Label(self, image= render4)
        img4.image = render4

        load5 = Image.open("D:\\Python\\project_py\\Sides.jpg")
        render5 = ImageTk.PhotoImage(load5)
        img5 = tk.Label(self, image= render5)
        img5.image = render5

        load6 = Image.open("D:\\Python\\project_py\\Salads.jpg")
        render6 = ImageTk.PhotoImage(load6)
        img6 = tk.Label(self, image= render6)
        img6.image = render6        

        button = tk.Button(self, image=img1.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageOne))
        button.place(x = 120, y = 250)

        button2 = tk.Button(self, image=img2.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageTwo))
        button2.place(x = 370, y = 250)

        button3 = tk.Button(self, image=img3.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageThree))
        button3.place(x = 620, y = 250)

        button4 = tk.Button(self, image=img4.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageFour))
        button4.place(x = 120, y = 500)

        button5 = tk.Button(self, image=img5.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageFive))
        button5.place(x = 370, y = 500)

        button6 = tk.Button(self, image=img6.image, height=160, width=200,borderwidth=2,bg='white',
                            command=lambda: controller.show_frame(PageSix))
        button6.place(x = 620, y = 500)

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render
        
        load1 =Image.open("D:\\Python\\project_py\\burger\\burger1.png")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\burger\\burger2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\burger\\burger3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        load4 = Image.open("D:\\Python\\project_py\\burger\\burger4.jpg")
        render4 = ImageTk.PhotoImage(load4)
        img4 = tk.Label(self, image= render4)
        img4.image = render4
        
        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)

        button = tk.Button(self,image=img1.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,1,100))
        button.place(x = 150, y = 250)
   
        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,2,100))
        button2.place(x = 520, y = 250)
        
        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,4,100))
        button3.place(x = 150, y = 480)
        
        button4 = tk.Button(self, image=img4.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,3,100))
        button4.place(x = 520, y = 480)        

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render

        load1 =Image.open("D:\\Python\\project_py\\beverages\\bev1.jpg")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\beverages\\bev2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\beverages\\bev3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        load4 = Image.open("D:\\Python\\project_py\\beverages\\bev4.jpg")
        render4 = ImageTk.PhotoImage(load4)
        img4 = tk.Label(self, image= render4)
        img4.image = render4
        
        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)

        button = tk.Button(self, image=img1.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,5,101))
        button.place(x = 150, y = 250)

        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,6,101))
        button2.place(x = 520, y = 250)

        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,7,101))
        button3.place(x = 150, y = 480)
        
        button4 = tk.Button(self, image=img4.image, height=200, width=200,bg='white',command=lambda:controller.myy(1,8,101))
        button4.place(x = 520, y = 480) 

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render

        load1 =Image.open("D:\\Python\\project_py\\coffee\\cc1.jpg")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\coffee\\cc2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\coffee\\cc3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)

        button = tk.Button(self, image=img1.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,9,102))
        button.place(x = 150, y = 250)

        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,10,102))
        button2.place(x = 520, y = 250)

        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white' ,command=lambda: controller.myy(1,11,102))
        button3.place(x = 150, y = 480)

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)
        
class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render

        load1 =Image.open("D:\\Python\\project_py\\sweets\\sw1.jpg")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\sweets\\sw2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\sweets\\sw3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        load4 = Image.open("D:\\Python\\project_py\\sweets\\sw4.jpg")
        render4 = ImageTk.PhotoImage(load4)
        img4 = tk.Label(self, image= render4)
        img4.image = render4

        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)

        button = tk.Button(self, image=img1.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,12,103))
        button.place(x = 150, y = 250)

        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,13,103))
        button2.place(x = 520, y = 250)

        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,14,103))
        button3.place(x = 150, y = 480)
        
        button4 = tk.Button(self, image=img4.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,15,103))
        button4.place(x = 520, y = 480)

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)

class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render

        load1 =Image.open("D:\\Python\\project_py\\sidesk\\ss1.jpg")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\sidesk\\ss2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\sidesk\\ss3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        load4 = Image.open("D:\\Python\\project_py\\sidesk\\ss4.jpg")
        render4 = ImageTk.PhotoImage(load4)
        img4 = tk.Label(self, image= render4)
        img4.image = render4

        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)

        button = tk.Button(self, image=img1.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,16,104))
        button.place(x = 150, y = 250)

        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,17,104))
        button2.place(x = 520, y = 250)

        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,18,104))
        button3.place(x = 150, y = 480)
                
        button4 = tk.Button(self, image=img4.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,19,104))
        button4.place(x = 520, y = 480)

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)

class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        f1 = textgradiant(self)
        f1.pack(side="top", fill="both", expand = True)

        ll = tk.Label(self,height = self.winfo_screenheight(), width = self.winfo_screenwidth(),bg='orange',fg='white')
        ll.pack(side='top',fill='both')

        tk.Label(self,height = 50, width = 120,bg='white',fg='white').place(x=50,y=200)  

        tk.Label(self,height = 50, width = 50,bg='white',fg='white').place(x=950,y=200)       

        load = Image.open("D:\\Python\\project_py\\fodiz.jpg")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(self, image= render)
        img.image = render

        load1 =Image.open("D:\\Python\\project_py\\salads\\sal1.jpg")
        render1 =ImageTk.PhotoImage(load1)
        img1 = tk.Label(self, image= render1)
        img1.image = render1

        load2 = Image.open("D:\\Python\\project_py\\salads\\sal2.jpg")
        render2 = ImageTk.PhotoImage(load2)
        img2 = tk.Label(self, image= render2)
        img2.image = render2

        load3 = Image.open("D:\\Python\\project_py\\salads\\sal3.jpg")
        render3 = ImageTk.PhotoImage(load3)
        img3 = tk.Label(self, image= render3)
        img3.image = render3

        button0 = tk.Button(self,width= 130, image=img.image,borderwidth=2,bg='white',command=lambda: controller.show_frame(StartPage))
        button0.place(x=30,y=20)
  
        button = tk.Button(self, image=img1.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,20,105))
        button.place(x = 150, y = 250)
  
        button2 = tk.Button(self, image=img2.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,21,105))
        button2.place(x = 520, y = 250)
  
        button3 = tk.Button(self, image=img3.image, height=200, width=200,bg='white',command=lambda: controller.myy(1,22,105))
        button3.place(x = 150, y = 480)

        tk.Button(self, text = "Buy", bg="dark orange", fg="white",height=1,width=6, font=lf2, command=lambda:controller.popup()).place(x=970,y=600)
        tk.Button(self, text = "Cancle", bg="orange red", fg="white",height=1,width=6, font=lf2, command=lambda:controller.reset()).place(x=1140,y=600)

class textgradiant(tk.Canvas):
    def __init__(self,parent):
        tk.Canvas.__init__(self,parent)
        label2 = tk.Label(self,text="POS For Foodizs",font=lf,bg='orange',fg='white',height=2)
        label2.pack(side='bottom',fill='both',expand = True)

app = Mainwindow()
app.geometry('1366x700+0+0')
app.title('P O S for Foodizs')
app.mainloop()

#pip install Pillow==5.2.0