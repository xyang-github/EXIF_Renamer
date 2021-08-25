import exiftool
import os
from datetime import datetime as dt
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup


class SelectDialog(FloatLayout):
    """Dialog box to select image file from file browser"""
    select = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MainScreen(BoxLayout):
    def select(self):
        """Instantiates selection dialog box as a popup and opens it"""
        select_dialog = SelectDialog(select=self.select_files, cancel=self.select_dismiss)
        self.popup = Popup(title="Select File(s)",
                           content=select_dialog,
                           size_hint=(0.9, 0.9))
        self.popup.open()

    def select_dismiss(self):
        """Dismisses the popup box"""
        self.popup.dismiss()

    def select_files(self, selection):
        """Stores file path as a list of strings"""
        self.image_list = selection
        self.display_filenames(self.image_list)
        self.select_dismiss()  # dismisses the popup once selection has been made

    def display_filenames(self, image_list):
        """Create a string variable of file paths to be displayed in filenames label"""
        image_list_formatted = ""
        for image in self.image_list:
            image_list_formatted += image + "\n"
        self.ids.filenames.text = image_list_formatted

    def rename(self):
        for image in self.image_list:
            file = image
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(file)

            date = metadata['EXIF:DateTimeOriginal']
            date_object = dt.strptime(date, '%Y:%m:%d %H:%M:%S')
            date_object_formatted = dt.strftime(date_object, '%Y-%m-%d  %H-%M-%S')
            os.rename(file, date_object_formatted)

# works if in the same directory. Need to find a way to make it work for files in different directories.



class MainApp(App):
    def build(self):
        Builder.load_file("frontend.kv")
        return MainScreen()


MainApp().run()


