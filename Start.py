from Screen import Login
from Screen.SignUp import SignUpScreen
from Screen.Section import SectionScreen
from Screen.Resturant import ResScreen
from Screen.Lodging import LodScreen

from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.clock import Clock


class SwitchScreen(ScreenManager):
    #Switch Screen is the main screen manager of the application
    def loginC(self):
        self.L = Login.LoginScreen()
        self.L.set()
        self.add_widget(self.L)
        self.current = 'login'
        self.SU = SignUpScreen()
        self.SU.set()
        self.add_widget(self.SU)
        self.SE = SectionScreen()
        self.SE.set()
        self.add_widget(self.SE)
        self.RS = ResScreen()
        self.RS.set()
        self.add_widget(self.RS)
        self.LS = LodScreen()
        self.LS.set()
        self.add_widget(self.LS)
    def update(self,dt):
        # Checks if there is any change in the screen
        if self.LS.bk == True or self.RS.rb.o.bk == True:
            self.current = 'section'
            self.SE.m.L.LSel = False
            self.LS.bk = False
            self.RS.rb.o.bk = False
            self.SE.m.R.RSel = False
        elif self.SE.m.R.RSel == True and self.L.B.LMB.LM.LoginT == True :
            self.current = "CustResScreen"
        elif self.SE.m.L.LSel == True:
            self.current = "LodgingScreen"
        elif self.L.B.LMB.LM.LoginT == True :
            self.current = 'section'
        elif self.L.B.LMB.LM.SignUpT == True :
            self.current = 'signup'
            if self.SU.X.SL.su.backtl == True or self.SU.X.SL.su.signupT == True:
                self.L.B.LMB.LM.SignUpT = False
                self.current = 'login'
                self.SU.X.SL.su.backtl = False
                self.SU.X.SL.su.signupT = False


class HotelManagementSystemApp(App):
    # main application
    def build (self):
        self.a = SwitchScreen()
        self.a.loginC()
        Clock.schedule_interval(self.a.LS.update,1.0 / 10.0)
        Clock.schedule_interval(self.a.update, 1.0 / 60.0)
        Clock.schedule_interval(self.a.RS.rb.o.up,1.0 / 30.0)
        return self.a

if __name__== '__main__':
    HotelManagementSystemApp().run()
