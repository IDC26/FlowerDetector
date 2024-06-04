# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from screens.Gallery import Gallery
from kivy.lang import Builder

Builder.load_file('main.kv')


class MainApp(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(MainScreen(name='main_screen'))
        self.gallery_screen = Gallery(name='gallery_screen')
        self.sm.add_widget(self.gallery_screen)
        return self.sm


class MainScreen(Screen):
    pass


if __name__ == "__main__":
    MainApp().run()
