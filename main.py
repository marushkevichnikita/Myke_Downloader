import os
from PIL import Image, MicImagePlugin, FpxImagePlugin
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from pytube import YouTube

Window.size = (600, 300)

Builder.load_string("""

<FirstScreen>:
    orientation: "vertical"
    Image:
        id: gif
        source: 'C:/Users/marus/Desktop/Python/pytube-temp/1/1.gif'
        pos: self.pos
        size_hint: None, None
        size: root.size
        allow_stretch: True
        keep_ratio: False
        anim_delay: -1
        anim_loop: 1

<DownloadScreen>:
    orientation: "vertical"
    spacing: "12dp"
    padding: "24dp"
    size_hint_y: None
    height: self.minimum_height + dp(50)
    pos_hint: {"center_x": .55, "center_y": .5}


    MDTextField:
        id: url_input
        hint_text: "Enter Youtube URL"
        multiline: False
        line_height: 1
        line_color_focus: 255/255, 99/255, 71/255, 1
        helper_text: "Wrong link"
        helper_text_mode: "on_error"



    MDFillRoundFlatButton:
        text: "Video"
        pos_hint: {"center_x": .05, "center_y": -.6}
        on_press: root.download_video()
        
    
    MDFillRoundFlatButton:
        text: "Audio"
        pos_hint: {"center_x": .20, "center_y": -.6}
        on_press: root.download_video2()

        
""")


class FirstScreen(Screen, FloatLayout):
    secs = 0

    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        self.orientation = "vertical"
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, sec):
        self.secs = self.secs+1
        '''  30 seconds'''
        if self.secs == 4:
            self.manager.current = 'download'

    def on_enter(self):
        self.ids.gif.anim_delay = 0.05


class DownloadScreen(Screen, BoxLayout):
    def download_video(self):
        link = self.ids.url_input.text
        try:
            video = YouTube(link)
            stream = video.streams.get_highest_resolution()
            stream.download()
            self.ids.url_input.text = ""
            self.ids.url_input.helper_text_mode = "on_focus"
            self.ids.url_input.helper_text = "Video downloaded successfully"
            self.ids.url_input._helper_text_color = [0, 1, 0, 1]
            self.ids.url_input.error = False
        except Exception as e:
            self.ids.url_input.error = True
            self.ids.url_input.helper_text_mode = "on_error"
            self.ids.url_input.helper_text = "Wrong link"
            
            
    def download_video2(self):
        link = self.ids.url_input.text
        try:
            video = YouTube(link)
            stream = video.streams.filter(only_audio=True).first()
            out_file = stream.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            self.ids.url_input.text = ""
            self.ids.url_input.helper_text_mode = "on_focus"
            self.ids.url_input.helper_text = "Audio downloaded successfully"
            self.ids.url_input._helper_text_color = [0, 1, 0, 1]
            self.ids.url_input.error = False
        except Exception as e:
            self.ids.url_input.error = True
            self.ids.url_input.helper_text_mode = "on_error"
            self.ids.url_input.helper_text = "Wrong link2"

                
class ExampleApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(DownloadScreen(name='download'))
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return sm
  


if __name__ == "__main__":
    ExampleApp().run()
exit()
