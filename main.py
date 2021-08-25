import exiftool
import os
import datetime as dt
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout


class LoadScreen(FloatLayout):
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainScreen(BoxLayout):
    pass


class MainApp(App):
    def build(self):
        Builder.load_file("frontend.kv")
        return MainScreen()


MainApp().run()


