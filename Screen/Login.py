from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
#import mysql.connector as db
#hmdb = db.connect(host="localhost",user="root",passwd="1997",db="hmsdb")
#cursor = hmdb.cursor()

#Builder.load_string('''
'''<LoginScreen>:
	BoxLayout:
<Title>:
	orientation: 'vertical'
	size_hint : 1, .1
	canvas:
		Color :
			rgba : .9411,.3843,.5725,1
        	Rectangle:
            		size : self.size
            		pos : self.pos
    	Label:
        	text : "Hotel Management System"
        	color : 0,0,0,1
        	bold : True
        	font_size : 50
<LoginBg>:
    	canvas:
        	Rectangle:
            		source : 'b.jpg'
            		size : self.size
            		pos : self.pos
<LoginMenu>:
    	orientation : 'vertical'
    	canvas:
        	Color :
            		rgba :1,.8784,.5098,1
        	Rectangle:
            		size : self.size
            		pos : self.pos
<LoginMenuB>:
    	canvas:
        	Color:
            		rgba : 1,.8353,.3098,1
        	Rectangle :
            		size : self.size
            		pos : self.pos
<UP>:
    	orientation : 'horizontal'

<AccType>:
    	Button:
        	text : 'Customer'
        	size_hint_y : None
        	height : 36
        	on_release : root.select('Customer')
        	background_normal: ''
        	background_color : 1,.4392,.2627,1
        	color : 0,0,0,1
    	Button:
        	text : 'Employee'
        	size_hint_y : None
        	height : 36
        	on_release : root.select('Employee')
        	background_normal: ''
        	background_color : 1,.4392,.2627,1
        	color : 0,0,0,1
    	Button:
        	text : 'Manager'
        	size_hint_y : None
        	height : 36
        	on_release : root.select('Manager')
        	background_normal: ''
        	background_color : 1,.4392,.2627,1
        	color : 0,0,0,1
 '''

class UP(BoxLayout):
    # Frame grouping label and input for login
    def set(self):
        self.padding = (5,5)
        self.spacing = 10
    def aset(self):
        self.add_widget(Label(text = 'Account Type', color = (0,0,0,1)))
        self.Account = AccType()
        self.acc = Button(text = 'Select Acc. Type',background_normal= '',background_color = (1,.4392,.2627,1),color = (0,0,0,1))
        self.acc.bind(on_release = self.Account.open)
        self.Account.bind(on_select = lambda instance, x : setattr( self.acc ,'text', x))
        self.add_widget(self.acc)
        self.set()
    def oset(self,t,f):
        self.add_widget(Label(text = t + ' : ', color = (0,0,0,1)))
        self.I = TextInput(hint_text = t, multiline = False, padding = (10,10),password = f)
        self.add_widget(self.I)
        self.set()


class Title(BoxLayout):
    # Main title of the Application
    def set(self):
        self.size_hint = (1,.1)
        self.pos_hint = {'top' : 1,'center_x' : 0.5}

class LoginBg(AnchorLayout):
    #Background which consist of image background
    def set(self):
        self.size_hint = (1,1)
        self.LMB = LoginMenuB()
        self.LMB.set()
        self.LoginT = self.LMB.LoginT
        self.SignUpT = self.LMB.SignUpT
        self.add_widget(self.LMB)

class LoginMenuB(BoxLayout):
    # Square background of login menu
    def set(self):
        self.size_hint=(.37,.52)
        self.pos_hint={'center_x' : 0.5,'center_y' : 0.5}
        self.padding = (10,10)
        self.LM = LoginMenu()
        self.LM.set()
        self.LoginT = self.LM.LoginT
        self.SignUpT = self.LM.SignUpT
        self.add_widget(self.LM)


    def aw(self, ob):
        self.add_widget(ob)

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self):
        self.title = 'Wrong Login Details'
        self.content = Label(text = 'You have entered \n wrong Login Details')
        self.size_hint = (None,None)
        self.size = (200,200)

class LoginMenu(BoxLayout):
    # Login Menu with all the input and button widgets
    def logincheck(self,instance):
        self.query = "SELECT * FROM logindetails WHERE username = '{}' AND acctype='{}' ".format(self.UN.I.text,self.AS.acc.text)
        #cursor.execute(self.query)
        self.validcheck = cursor.fetchone()
        if self.PW.I.text == ''or self.validcheck == None:
            self.p = PopUp()
            self.p.set()
            self.p.open()
        else :
            if self.PW.I.text == self.validcheck[1]:
                self.LoginT = True
                hmdb.close()
            else :
                self.p = PopUp()
                self.p.set()
                self.p.open()


    def signupcheck(self,instance):
        self.SignUpT = True

    def set(self):
        self.LoginT = False
        self.SignUpT = False
        self.padding = (10,10)
        self.pos_hint={'center_x' : 0.5,'center_y' : 0.5}
        self.aw(Label(text='Login',color =(0,0,0,1), bold = True,font_size = 25))
        self.AS = UP()
        self.AS.aset()
        self.aw(self.AS)
        self.UN = UP()
        self.UN.oset('Username',False)
        self.aw(self.UN)
        self.PW = UP()
        self.PW.oset('Password',True)
        self.aw(self.PW)
        self.lg = Button(text = 'Login',background_normal= '',background_color = (1,.4392,.2627,1),color = (0,0,0,1))
        self.lg.bind(on_press = self.logincheck)
        self.aw(self.lg)
        self.signup = BoxLayout(orientation = 'horizontal', padding = (5,5),spacing = 10)
        self.orl = Label(text = 'Or', size_hint = (.3,1),color = (0,0,0,1))
        self.signupb = Button(on_press = self.signupcheck,text = 'Sign Up', size_hint = (.7,1),background_normal= '',background_color = (1,.4392,.2627,1),color = (0,0,0,1))
        self.signup.add_widget(self.orl)
        self.signup.add_widget(self.signupb)
        self.aw(self.signup)



    def aw(self,ob):
        self.add_widget(ob)

class LoginScreen(Screen,BoxLayout):
    # main login screen
    def set(self):
        self.name = 'login'
        self.orientation = 'vertical'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T,index = 0)
        self.B = LoginBg()
        self.B.set()
        self.LoginT = self.B.LoginT
        self.SignUpT = self.B.SignUpT
        self.add_widget(self.B,index = 1)


class AccType(DropDown):
    # To create drop down list
    pass



class Main():
    # crete local login application
    def Start(self):
        self.sm = ScreenManager()
        self.L = LoginScreen()
        self.L.set()
        self.sm.add_widget(self.L)
        return self.sm

class HotelMangementSystemApp(App):
    def build(self):
        inspector.create_inspector(Window,Main)
        X = Main()
        return X.Start()

if __name__ == '__main__':
    HotelMangementSystemApp().run()
