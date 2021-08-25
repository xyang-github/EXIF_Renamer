import exiftool
import os
import datetime as dt
from kivy.app import App
from kivy.lang import Builder



class MainApp(App):
    def build:
        return Builder.load_file("frontend.kv")

MainApp().run()


