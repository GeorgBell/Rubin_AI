from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.button import  Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial
import cv2
from usb_cam import create_data_directory, MicroCamera
from time import sleep


class KivyCamera(Image):
    def __init__(self, capture, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.capture.stream_start()
        sleep(2)
        Clock.schedule_interval(self.update, 0.01)

    def update(self, dt):
        # convert it to texture
        frame = self.capture.yield_frame()
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.texture = image_texture

class CamApp(App):
    def build(self):

        self.capture = MicroCamera(device_id=1)
        self.box = BoxLayout(orientation='horizontal', spacing=20)
        self.my_camera = KivyCamera(capture=self.capture)
        self.btn_capture = Button(text='Capture', on_press=partial(self.capture.capture_single_image, *[1,2,3]), size_hint=(1,1))
        self.box.add_widget(self.my_camera)
        self.box.add_widget(self.btn_capture)

        return self.box

    def on_stop(self):
        #without this, app will not exit even if the window is closed
        self.capture.stream_stop()
        print("Stream stopped")
        self.capture.camera_close()
        print("Camera closed")


if __name__ == '__main__':
    CamApp().run()
