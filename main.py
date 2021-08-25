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
        self.extract_data(self.image_list)
        self.display_filenames()
        self.select_dismiss()  # dismisses the popup once selection has been made

    def extract_data(self, image_list):
        """Extract EXIF information from each file"""
        self.original_filename_text = ""
        self.new_filename_text = ""
        self.original_filename_list = []
        self.new_filename_list = []

        for image in self.image_list:
            file = image
            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(file)

            date = metadata['EXIF:DateTimeOriginal']   # extract date picture taken from metadata
            self.directory = metadata['File:Directory']  # extract file directory of picture
            extension = metadata['File:FileTypeExtension']  # extract file extension type

            self.format_data(date, extension, file)

    def format_data(self, date, extension, file):
        """Create a string of the desired naming format"""
        date_object = dt.strptime(date, '%Y:%m:%d %H:%M:%S')
        date_object_formatted = dt.strftime(date_object, '%Y-%m-%d  %H-%M-%S')

        new_filename = f"{date_object_formatted}.{extension}"

        self.original_filename_text += file + "\n"
        self.new_filename_text += new_filename + "\n"
        self.original_filename_list.append(file)
        self.new_filename_list.append(new_filename)

    def display_filenames(self):
        """Displays original and new filenames"""
        self.ids.original_filenames.text = self.original_filename_text
        self.ids.new_filenames.text = self.new_filename_text

    def rename(self):
        """Renames file in original directory"""
        for original_img in self.original_filename_list:
            for new_img in self.new_filename_list:
                os.rename(original_img, f"{self.directory}/{new_img}")




class MainApp(App):
    def build(self):
        Builder.load_file("frontend.kv")
        return MainScreen()


MainApp().run()


