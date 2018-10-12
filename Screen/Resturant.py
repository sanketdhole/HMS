from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.clock import Clock
import random
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",passwd="1997",db="hmsdb")
cursor = hmdb.cursor()

Builder.load_string('''
<ResTitle>:
    orientation: 'vertical'
    size_hint : 1, .1
    canvas:
        Color :
            rgba : .9411,.3843,.5725,1
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Resturant"
        color : 0,0,0,1
        bold : True
        font_size : 50
        
<ResMenu>:
    canvas:
        Color:
            rgba : 0,1,0,1
        Rectangle:
            size : self.size
            pos : self.pos
                
<Orders>:
    canvas:
        Color:
            rgba : 0,1,1,1
        Rectangle:
            size : self.size
            pos : self.pos
<Item>:
    canvas:
        Color:
            rgba : 0,1,.5,1
        Rectangle:
            size : self.size
            pos : self.pos
            
<Order>:
    canvas:
        Color:
            rgba : 0,0,0,1
        Rectangle:
            size: self.size
            pos : self.pos
''')
cartitem = []
nud = False

class Order(BoxLayout):
    def set(self,item):
        self.rm = False
        self.orientation = 'horizontal'
        self.size_hint = (1,None)
        self.height = 44
        self.name = Label(text = item[0],size_hint = (.4,1))
        self.add_widget(self.name)
        self.quantity = Label(text = str(item[2]),size_hint = (.3,1))
        self.add_widget(self.quantity)
        self.price = Label(text = str(int(item[2]) * int(item[1])),size_hint =(.2,1))
        self.add_widget(self.price)
        self.remove = Button(text = "X",size_hint = (.1,1),on_press = self.removeOrder)
        self.add_widget(self.remove)
        return self

    def removeOrder(self,a):
        self.rm =True


class  Orders(BoxLayout):
    global cartitem
    global nud
    def set(self):
        self.orientation = 'vertical'
        self.size_hint = (.3,1)
        self.padding = (10,10)
        self.spacing = 10
        self.cart = Label(text='Your Cart',color=(0,0,0,1),size_hint= (1,None),height=15)
        self.add_widget(self.cart)
        self.bl = BoxLayout(orientation='horizontal',size_hint =(1,None),height=15)
        self.i = Label(text='Items',color=(0,0,0,1),size_hint= (.4,1))
        self.bl.add_widget(self.i)
        self.q = Label(text='Quantity',color=(0,0,0,1),size_hint= (.3,1))
        self.p = Label(text='Price',color=(0,0,0,1),size_hint= (.3,1))
        self.bl.add_widget(self.q)
        self.bl.add_widget(self.p)
        self.add_widget(self.bl)
        self.gl = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.gl.bind(minimum_height = self.gl.setter('height'))
        self.sv = ScrollView(size_hint=(1, 1), size=(self.width, self.height),do_scroll_x = False)
        self.add_widget(self.sv)
        self.tbl = BoxLayout(orientation = 'horizontal',size_hint = (1,None),height = 15)
        self.total = 0
        self.tbl.add_widget(Label(text='Total',size_hint=(.5,1),color = (0,0,0,1)))
        self.totalprice = Label(text=str(self.total),size_hint=(.5,1),color = (0,0,0,1))
        self.tbl.add_widget(self.totalprice)
        self.add_widget(self.tbl)
        self.sbl = BoxLayout(orientation = 'horizontal',size_hint = (1,None),height = 15)
        self.sbl.add_widget(Button(text='Save',size_hint = (.5,1),on_press = self.back))
        self.sbl.add_widget(Button(text = 'Pay Off',size_hint = (.5,1),on_press = self.back))
        self.add_widget(self.sbl)
        self.shown = []
        self.obj = []
        self.bk = False
        nud = False
    def back(self,a):
        self.bk = True
        self.query = 'insert into reslog values (%s,%s)'%(self.total,random.randint(10,10000))
        cursor.execute(self.query)
        hmdb.commit()

    def up(self,a):
        global nud
        global cartitem
        self.similar = False
        for i in self.obj:
            if i.rm == True:
                self.gl.remove_widget(i)
                i.rm = False
        if nud == True:
            self.sv.remove_widget(self.gl)
            for i in range(len(cartitem)):
                for j in range(len(self.shown)):
                    if self.shown[j][0] == cartitem[i][0]:
                        self.similar = True
                        self.objj = j
                        self.obji = i

                if self.similar == True:
                    self.obj[self.obji].price.text = str(int(cartitem[self.obji][1]) * int(cartitem[self.obji][2]))
                    self.obj[self.obji].quantity.text = str(cartitem[self.obji][2])
                    self.similar = False
                else:
                    self.obj.append(Order())
                    self.obj[i] = self.obj[i].set(cartitem[i])
                    self.gl.add_widget(self.obj[i])
                    self.a = cartitem[i]
                    self.shown.append(self.a)
            nud = False
            self.total = 0
            for i in range(len(self.shown)):
                self.total += int(self.obj[i].price.text)
            self.totalprice.text = str(self.total)
            self.sv.add_widget(self.gl)
        else:
            pass

class Item(BoxLayout):
    global cartitem
    global nud
    def set(self,row):
        self.orientation = 'vertical'
        self.row = row
        self.size_hint = (.3,.2)
        self.name = Label(text=row[0],size_hint=(1,0.5),color = (0,0,0,1))
        self.add_widget(self.name)
        self.bl = BoxLayout(orientation = 'horizontal', size_hint = (1,.5))
        self.price = Label(text='Price :'+str(row[1]),size_hint = (.5,1),color = (0,0,0,1))
        self.bl.add_widget(self.price)
        self.addtocart = Button(text='Add to Card', size_hint = (.5,1),on_press= self.additem)
        self.bl.add_widget(self.addtocart)
        self.add_widget(self.bl)
        return self

    def additem(self,a):
        global nud
        similar = False
        nud = True
        if cartitem==[]:
            cartitem.append(list(self.row))
        else:
            for i in range(len(cartitem)):
                if cartitem[i][0]==self.row[0]:
                    cartitem[i][2] +=1
                    similar = True
                    break
                else:
                    similar = False
            if similar == False:
                cartitem.append(list(self.row))


class Items(TabbedPanelItem):
    def set(self,text):
        cursor.execute('select * from {}'.format(text))
        row = cursor.fetchone()
        self.sl = StackLayout(orientation = 'lr-tb',padding=(10,10),spacing = 10)
        self.l = []
        i = 0
        while row is not None:
            self.l.append(Item())
            self.l[i] = self.l[i].set(row)
            self.sl.add_widget(self.l[i])
            i += 1
            row = cursor.fetchone()
        self.add_widget(self.sl)



class ResMenu(TabbedPanel,BoxLayout):
    def set(self):
        self.orientaion = 'horizontal'
        self.do_default_tab = False
        self.starter = Items(text='Starter')
        self.starter.set('starter')
        self.add_widget(self.starter)
        self.default_tab = self.starter
        self.maincourse = Items(text= 'Main Course')
        self.maincourse.set('maincourse')
        self.add_widget(self.maincourse)
        self.breads = Items(text='Breads')
        self.breads.set('breads')
        self.add_widget(self.breads)
        self.extras = Items(text="Extras")
        self.extras.set('extras')
        self.add_widget(self.extras)



class ResBg(BoxLayout):
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint = (1,.9)
        self.m = ResMenu()
        self.m.set()
        self.o = Orders()
        self.o.set()
        self.add_widget(self.o)
        self.add_widget(self.m)

class ResTitle(BoxLayout):
        # Main title of the Application
    def set(self):
        self.size_hint = (1, .1)
        self.pos_hint = {'top': 1, 'center_x': 0.5}

class ResScreen(Screen,BoxLayout):
    def set(self):
        self.name = "CustResScreen"
        self.orientation = 'vertical'
        self.Ti = ResTitle()
        self.Ti.set()
        self.add_widget(self.Ti)
        self.rb = ResBg()
        self.rb.set()
        self.add_widget(self.rb)


class ResScreenM(ScreenManager):
    def set(self):
        self.R = ResScreen()
        self.R.set()
        self.add_widget(self.R)

class ResScreenApp(App):
    def build(self):
        self.s = ResScreenM()
        self.s.set()
        Clock.schedule_interval(self.s.R.rb.o.up, 1.0 / 60.0)
        inspector.create_inspector(Window, self.s)
        return self.s


if __name__ == '__main__':
    ResScreenApp().run()