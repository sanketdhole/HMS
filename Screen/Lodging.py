from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from Screen.Login import Title
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import datetime
import random
now = datetime.datetime.now()
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",passwd="1997",db="hmsdb")
cursor = hmdb.cursor()

Builder.load_string('''
<LodBg>:
    canvas:
        Color:
            rgba : 0,0,0,1
        Rectangle:
            size : self.size
            pos : self.pos
<Room>
    canvas:
        Color:
            rgba: .7,.5,.7,1
        Rectangle:
            size : self.size
            pos : self.pos
''')

class inLabel(BoxLayout):
    def set(self,lt):
        self.orientation = 'horizontal'
        self.size_hint = (1,.5)
        self.label = Label(text =lt + ' : ', size_hint = (.5,1))
        self.ti = TextInput(hint_text = lt , size_hint = (.5,1))

class GuestBg(BoxLayout):
    def set(self):
        self.size_hint = (.3,7)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = (10,10)
        self.checkinT = False
        self.title = Label(text='Enter Guest Details',size_hint = (1,None),height=20)
        self.add_widget(self.title)
        self.fn = inLabel()
        self.fn.set('First Name')
        self.add_widget(self.fn)
        self.ln = inLabel()
        self.ln.set('Last Name')
        self.add_widget(self.ln)
        self.ids = inLabel()
        self.ids.set('Id No.')
        self.add_widget(self.ids)
        self.phoneno = inLabel()
        self.phoneno.set('Phone No')
        self.checkin = Button(text = 'Check In' , on_press = self.cin)
        self.add_widget(self.checkin)

    def cin(self,a):
        self.checkinT = True



class GuestDataScreen(Screen):
    def set(self,rmno):
        self.rmno = rmno
        self.T = Title()
        self.T.set()
        self.add_widget(self.T)
        self.gr = GuestBg()
        self.gr.set()
        self.add_widget(self.gr)


class Room(BoxLayout):
    def set(self,x):
        self.rcin = False
        self.rcout = False
        self.cin = False
        self.cout = False
        self.orientation = 'vertical'
        self.size_hint = (.3,.2)
        self.room = str(x+1)
        self.roomno = Label(text = 'Room No. : '+str(x+1),size_hint = (1,.5))
        self.add_widget(self.roomno)
        self.bl = BoxLayout(size_hint = (1,.5))
        self.checkin = Button(text = 'Check In',on_press = self.roomcheckin)
        self.bl.add_widget(self.checkin)
        self.checkout = Button(text = 'Check Out', on_press = self.roomcheckout)
        self.bl.add_widget(self.checkout)
        self.status = Label(text = 'Available')
        self.bl.add_widget(self.status)
        self.add_widget(self.bl)

    def roomcheckin(self,a):
        self.rcin = True
        self.cin = True
        self.status.text = 'UnAvailable'

    def roomcheckout(self,a):
        self.rcin = False
        self.rcout = True
        self.cout = True
        self.status.text = "Available"





class LodBg(StackLayout):
    def set(self):
        self.size_hint = (1,.9)
        self.orientation = 'lr-tb'
        self.padding = (10,10)
        self.spacing = 10
        self.roomsno = 10
        self.rooms = []
        for i in range(self.roomsno):
            self.rooms.append(Room())
            self.rooms[i].set(i)
            self.add_widget(self.rooms[i])

class LodScreen(Screen):
    def set(self):
        self.name = "LodgingScreen"
        self.T = Title()
        self.T.set()
        self.add_widget(self.T, index = 0)
        self.L = LodBg()
        self.L.set()
        self.add_widget(self.L,index = 1)
        self.bl = StackLayout(orientation = 'rl-tb',size_hint = (1,None),height = 30)
        self.bl.add_widget(Button(text = 'Back',size_hint= (.1,1),on_press = self.back))
        self.add_widget(self.bl)
        self.bk = False

    def update(self,a):
        for i in range(10):
            if self.L.rooms[i].rcin == True and self.L.rooms[i].cin == True:
                self.d = '{}/{}/{}'.format(now.day, now.month, now.year)
                self.t = '{}:{}:{}'.format(now.hour, now.minute, now.second)
                self.queryin = 'insert into lodgedetails values ("{}","{}","{}","{}","in")'.format(self.d, self.t,random.randint(10,10000),self.L.rooms[i].room)
                cursor.execute(self.queryin)
                self.L.rooms[i].cin = False
                hmdb.commit()
            elif self.L.rooms[i].rcout == True and self.L.rooms[i].cout == True:
                self.d = '{}/{}/{}'.format(now.day, now.month, now.year)
                self.t = '{}:{}:{}'.format(now.hour, now.minute, now.second)
                self.queryout = 'insert into lodgedetails values ("{}","{}","{}","{}","out")'.format(self.d, self.t,random.randint(10,10000),self.L.rooms[i].room)
                self.L.rooms[i].cout = False
                cursor.execute(self.queryout)
                hmdb.commit()


    def back(self,a):
        self.bk = True


class LodScreenApp(App):
    def build(self):
        self.L = LodScreen()
        self.L.set()
        self.sm = ScreenManager()
        self.sm.add_widget(self.L)
        Clock.schedule_interval(self.L.update, 1.0/30.0)
        return self.L
if __name__ == '__main__':
    LodScreenApp().run()