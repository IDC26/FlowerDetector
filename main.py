# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from screens.Gallery import Gallery
from screens.send_screen import CameraClick
from kivy.lang import Builder

Builder.load_file('main.kv')

class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main_screen'))
        self.sm.add_widget(CameraClick(name='send_screen'))
        self.sm.add_widget(Gallery(name='gallery_screen'))
        return self.sm

class MainScreen(Screen):
    pass

if __name__ == "__main__":
    MainApp().run()
