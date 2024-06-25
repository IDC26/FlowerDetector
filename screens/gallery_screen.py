import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.filemanager import MDFileManager
from kivy.utils import platform

# KV String
Builder.load_string("""
<Gallery>:
    id: gallery_screen
    name: 'gallery_screen'
    MDRaisedButton:
        text: "Alege Poza"
        elevation: 10
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_release: root.file_manager_open()
""")

def preprocess_image(path, input_shape):
    img_height, img_width, _ = input_shape
    image = Image.open(path)
    image = image.resize((img_height, img_width))
    image = np.array(image, dtype=np.float32)
    image = np.expand_dims(image, 0)
    return image

class Gallery(Screen):
    def __init__(self, **kwargs):
        super(Gallery, self).__init__(**kwargs)
        self.file_manager = None
        self.manager_open = False
        self.interpreter = None

    def file_manager_open(self):
        if not self.file_manager:
            self.file_manager = MDFileManager(
                exit_manager=self.exit_manager, select_path=self.select_path)
        if platform == "android":
            self.file_manager.show('/storage/emulated/0/Download/pozeapp/')
        else:
            self.file_manager.show('/')

        self.manager_open = True

    def select_path(self, path):
        print("Selected path:", path)
        image = self.preprocess_and_classify(path)
        if image is not None:
            predicted_class, confidence = self.classify_image(image)
            if predicted_class is not None:
                class_names = ['margaretă', 'păpădie', 'trandafiri', 'floare-soarelui', 'lalele']
                predicted_class_name = class_names[predicted_class]

                popup = Popup(
                    title='Rezultatul clasificarii',
                    content=Label(text=f'Clasa prezisa: {predicted_class_name}\nProbabilitate: {confidence:.2f}%'),
                    size_hint=(None, None), size=(400, 200)
                )
                popup.bind(on_dismiss=self.return_to_main)
                popup.open()
                print(predicted_class_name)
            else:
                popup = Popup(
                    title='Rezultatul clasificarii',
                    content=Label(text=f'Imaginea nu a putut fi clasificata'),
                    size_hint=(None, None), size=(400, 200)
                )
                popup.bind(on_dismiss=self.return_to_main)
                popup.open()
                print("Imaginea nu a putut fi clasificata.")
        else:
            print("Imaginea nu a putut fi preprocesata.")

    def preprocess_and_classify(self, path):
        if not self.interpreter:
            self.interpreter = tflite.Interpreter(model_path="flori.tflite")
            self.interpreter.allocate_tensors()
        input_details = self.interpreter.get_input_details()
        input_shape = input_details[0]['shape'][1:4]
        return preprocess_image(path, input_shape)

    def classify_image(self, image):
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.interpreter.set_tensor(input_details[0]['index'], image)
        self.interpreter.invoke()
        predictions_lite = self.interpreter.get_tensor(output_details[0]['index'])
        score_lite = self.softmax(predictions_lite[0])
        if np.max(score_lite) >= 0.85:
            predicted_class_index = np.argmax(score_lite)
            confidence = 100 * np.max(score_lite)
            return predicted_class_index, confidence
        else:
            return None, None

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def exit_manager(self, *args):
        self.file_manager.close()
        self.manager_open = False

    def return_to_main(self, *args):
        self.manager.current = 'main_screen'
