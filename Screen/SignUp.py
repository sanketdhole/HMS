from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.lang import Builder
from Screen.Login import Title
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",passwd="1997",db="hmsdb")
cursor = hmdb.cursor()

Builder.load_string('''
<STitle>:
    orientation: 'vertical'
    size_hint : 1, .08
    pos_hint : {'top' : .9,'center_x' : 0.5}
    canvas:
        Color :
            rgba : 1,.8353,.3098,1
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Sign Up"
        color : 0,0,0,1
        bold : True
        font_size : 35
<SignUpBg>:
    canvas:
        Color:
            rgba : 1,.8353,.3098,1
        Rectangle :
            size : self.size
            pos : self.pos
            

''')
class STitle(BoxLayout):
    # Sign up title
    pass

class RButton(BoxLayout):
    # Radio button for selecting gender
    def set(self):
        self.selectMale = False
        self.selectFemale = False
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = (10,10)
        self.l = Label(text = 'Gender',size_hint = (1.5,1),color = (0,0,0,1))
        self.add_widget (self.l)
        self.m = ToggleButton(text = 'Male',group = 'gender',on_press = self.selectM,background_color=(.1254,.0392,.2117,1))
        self.add_widget(self.m)
        self.f = ToggleButton(text = 'Female', group = 'gender',on_press = self.selectF,background_color=(.1254,.0392,.2117,1))
        self.add_widget(self.f)

    def selectM(self,x):
        self.selectMale = True
        self.selectFemale = False

    def selectF(self,x):
        self.selectFemale = True
        self.selectMale = False

class DOB(BoxLayout):
    # Frame of widgets to get date of birth
    def set(self):
        self.orientation = 'horizontal'
        self.padding = (5,5)
        self.spacing = 10
        self.l = Label(text= 'Date Of Birth', color = (0,0,0,1))
        self.d = TextInput(hint_text = 'DD',size_hint = (.3,1),write_tab = False,input_filter = 'int')
        self.m = TextInput(hint_text = 'MM',size_hint = (.3,1),write_tab = False,input_filter = 'int')
        self.yy = TextInput(hint_text = 'YYYY',size_hint = (.5,1),write_tab = False,input_filter = 'int')
        self.add_widget(self.l)
        self.add_widget(self.d)
        self.add_widget(self.m)
        self.add_widget(self.yy)

class SignUpBg(BoxLayout):
    # Background for SignUP page
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint  = (1,.82)
        self.FL = FirstList()
        self.FL.set()
        self.add_widget(self.FL)
        self.SL = SecondList()
        self.SL.set()
        self.add_widget(self.SL)

class IL(BoxLayout):
    # Frame which group the label and input for various attributes
    def set(self,t,ps = False, input_f = None):
        self.t = t
        self.add_widget(Label(text = t + ' : ', color = (0,0,0,1)))
        self.ti = TextInput(hint_text = t ,password = ps,write_tab = False, input_filter = input_f )
        self.add_widget(self.ti)

class PopUp(Popup):
    def set(self,title,content):
        self.title = title
        self.content = Label(text = content )
        self.size_hint = (None,None)
        self.size = (200,200)

class FirstList(BoxLayout):
    # Contais Frames at the left side of screen
    def set(self):
        self.orientation = 'vertical'
        self.padding = (10,10)
        self.spacing = 10
        self.FirstName = self.aw('First Name')
        self.LastName = self.aw('Last Name')
        self.Email = self.aw('Email')
        self.PhoneNo = self.aw('Phone No.',inp='int')
        self.Username = self.aw('Username')
        self.PassWord = self.aw('Password',ps=True)
        self.CPassWord = self.aw('Confirm Password',ps=True)
        self.SAddress = self.aw('Street Address',inp = None)
        self.City = self.aw('City')

    def aw(self,t,ps= False, inp = None):
        self.w = IL()
        self.w.set(t,ps,input_f=inp)
        self.add_widget(self.w)
        return self.w

    def check(self):
        if self.CPassWord.ti.text != self.PassWord.ti.text:
            self.PE = PopUp()
            self.PE.set('Password Differ', 'Your Password do not match with confirm password')
            self.PE.open()
            return False
        return True

    def getdata(self):
        self.FirstListItem = []
        if self.check() == True:
            self.FirstListI = [self.FirstName,self.LastName,self.Email,self.PhoneNo,self.Username,self.CPassWord,self.SAddress,self.City]
            for i in self.FirstListI:
                self.FirstListItem.append(i.ti.text)
            return self.FirstListItem

class SButton(BoxLayout):
    # Sign up button and back button
    def set(self):
        self.backtl = False
        self.signupT = False
        self.orientation = 'horizontal'
        self.spacing = 10
        self.b = Button(text = 'Sign Up',on_press = self.SignUpButton,background_color=(.1254,.0392,.2117,1))
        self.add_widget(self.b)
        self.back = Button(text = 'Back', on_press = self.backtologin,background_color=(.1254,.0392,.2117,1))
        self.add_widget(self.back)

    def SignUpButton(self,a):
        self.signupT = True

    def backtologin(self,x):
        self.backtl = True


class SecondList(BoxLayout):
    # Consist of Frames at the right side of the screen
    def set(self):
        self.padding = (10,10)
        self.spacing = 10
        self.orientation = 'vertical'
        self.PinCode = self.aw('Pincode')
        self.State = self.aw('State')
        self.Country = self.aw('Country')
        self.Aadhaar = self.aw('Aadhaar No.')
        self.Licence = self.aw('Licence No.')
        self.Other = self.aw('Other Id No.')
        self.g = RButton()
        self.g.set()
        self.add_widget(self.g)
        self.dob = DOB()
        self.dob.set()
        self.add_widget(self.dob)
        self.su = SButton()
        self.su.set()
        self.add_widget(self.su)


    def aw(self,t):
        w = IL()
        w.set(t)
        self.add_widget(w)
        return w

    def check(self):
        self.PinCode = int(self.PinCode)

    def getdata(self):

        self.SecondListI = [self.PinCode, self.State, self.Country, self.Aadhaar, self.Licence, self.Other,]
        self.SecondListItem = []
        for i in self.SecondListI:
            self.SecondListItem.append(i.ti.text)
        if self.g.selectMale == True :
            self.SecondListItem.append('Male')
        elif self.g.selectFemale == True:
            self.SecondListItem.append('Female')
        self.d = self.dob.d.text
        self.m = self.dob.m.text
        self.y = self.dob.yy.text
        self.SecondListItem.append((str(int(self.d))+'/'+str(int(self.m))+'/'+str(int(self.y))))
        return self.SecondListItem


class SignUpScreen(Screen,BoxLayout):
    # main screen for sign up
    def set(self):
        self.name = 'signup'
        self.orientation = 'vertical'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T,index = 0)
        self.add_widget(STitle(),index = 0)
        self.X = SignUpBg()
        self.X.set()
        self.X.SL.su.b.on_press = self.getdata
        self.add_widget(self.X,index = 1)

    def getdata(self):
        self.X.FL.getdata()
        self.fl = self.X.FL.FirstListItem
        self.X.SL.getdata()
        self.sl = self.X.SL.SecondListItem
        self.total = self.fl + self.sl
        self.X.SL.su.backtl = True
        self.query = 'INSERT INTO userdetails VALUES ('
        for i in range(len(self.total)):
            self.query += "'"+self.total[i]+"'"
            if i == len(self.total)-1:
                self.query = self.query
            else:
                self.query += ','
        self.query += ')'
        cursor.execute(self.query)
        self.q = "insert into logindetails values ('{}','{}','Customer')".format(self.total[4],self.total[5])
        cursor.execute(self.q)
        hmdb.commit()


class SignUpApp(App):
    # Create local app
    def build(self):
        self.sm = ScreenManager()
        self.a = SignUpScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        inspector.create_inspector(Window, self.a)
        return self.sm

if __name__ == '__main__':
    SignUpApp().run()