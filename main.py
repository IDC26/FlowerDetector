# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from screens.gallery_screen import Gallery
from screens.camera_screen import CameraClick
from kivy.lang import Builder

Builder.load_file('main.kv')

class AplicatieFlori(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main_screen'))
        #self.sm.add_widget(CameraClick(name='camera_screen'))
        self.sm.add_widget(Gallery(name='gallery_screen'))
        return self.sm

class MainScreen(Screen):
    pass

if __name__ == "__main__":
    AplicatieFlori().run()
