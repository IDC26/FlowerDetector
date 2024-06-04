# send_screen.py
import os.path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.camera import Camera
from kivy.uix.screenmanager import Screen
import time


class CameraClick(Screen):
    def __init__(self, **kwargs):
        super(CameraClick, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=False, resolution=(1920, 1080))
        self.layout.add_widget(self.camera)

        self.toggle_button = ToggleButton(text='Porneste Camera', size_hint_y=None, height='48dp')
        self.toggle_button.bind(on_press=self.toggle_camera)
        self.layout.add_widget(self.toggle_button)

        self.capture_button = Button(text='Fa poza', size_hint_y=None, height='48dp')
        self.capture_button.bind(on_press=self.capture)
        self.layout.add_widget(self.capture_button)

        self.add_widget(self.layout)

    def toggle_camera(self, instance):
        self.camera.play = not self.camera.play

    def capture(self, instance):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        timestr = time.strftime("%Y%m%d_%H%M%S")
        directory = "/storage/emulated/0/Download/pozeapp/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, 'IMG_{}.png'.format(timestr))
        self.camera.export_to_png(filepath)
        self.manager.current = 'main_screen'
        print("Captured")
