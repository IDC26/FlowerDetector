import os
import time
import cv2
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy_garden.xcamera import XCamera
from kivy.uix.camera import Camera


class CameraClick(Screen):
    def __init__(self, **kwargs):
        ''' constructorul clasei '''
        super(CameraClick, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=True, resolution=(1920, 1080))
        self.layout.add_widget(self.camera)
        self.add_widget(self.layout)
        self.capture_button = Button(text='Fa poza', size_hint_y=None, height='48dp')
        self.capture_button.bind(on_press=self.capture)
        self.layout.add_widget(self.capture_button)
    def toggle_camera(self, instance):
        self.camera.play = not self.camera.play
        self.toggle_button.text = 'Opreste Camera' if self.camera.play else 'Porneste Camera'

    def capture(self, instance):
        ''' functia de captura a pozei '''
        timestr = time.strftime("%Y%m%d_%H%M%S")
        directory = "/storage/emulated/0/Download/pozeapp/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = os.path.join(directory, 'IMG_{}.png'.format(timestr))

        self.camera.export_to_png(filepath)
        image = cv2.imread(filepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)  # converteste imaginea din format BGRA la BGR
        cv2.imwrite(filepath, image)
        print("Poza salvata cu succes!")
        print(filepath)
        self.manager.current = 'gallery_screen'