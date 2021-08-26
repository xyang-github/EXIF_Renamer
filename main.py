import exiftool
import os
from datetime import datetime as dt
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
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
        self.ids.rename.disabled = False
        self.ids.rename.opacity = 1

    def extract_data(self, image_list):
        """Extract EXIF information from each file"""
        self.original_filename_text = ""  # string of original file names to be displayed for user
        self.new_filename_text = ""  # string of new file names to be displayed for user
        self.original_filename_list = []
        self.new_filename_list = []

        for image in self.image_list:
            file = image  # full path to the original file
            self.original_filename_list.append(file)

            with exiftool.ExifTool() as et:
                metadata = et.get_metadata(file)

            original_filename = metadata['File:FileName']  # extract original filename of image
            date = metadata['EXIF:DateTimeOriginal']  # extract date picture taken from metadata
            self.directory = metadata['File:Directory']  # extract file directory of picture
            extension = metadata['File:FileTypeExtension']  # extract file extension type

            self.format_data(date, extension, original_filename)

    def format_data(self, date, extension, original_filename):
        """Create a string of the desired naming format"""
        date_object = dt.strptime(date, '%Y:%m:%d %H:%M:%S')
        date_object_formatted = dt.strftime(date_object, '%Y-%m-%d  %H-%M-%S')
        new_filename = f"{date_object_formatted}.{extension}"

        self.original_filename_text += original_filename + "\n"
        self.new_filename_text += new_filename + "\n"

        self.new_filename_list.append(new_filename)

    def display_filenames(self):
        """Displays original and new filenames"""
        self.ids.original_filenames.text = self.original_filename_text
        self.ids.new_filenames.text = self.new_filename_text

    def rename(self):
        """Renames file without changing directories"""
        counter = 0
        for original_img in range(len(self.original_filename_list)):
            for new_img in range(len(self.new_filename_list)):
                try:
                    os.rename(self.original_filename_list[counter], f"{self.directory}/{self.new_filename_list[counter]}")
                    counter += 1
                    break
                except FileExistsError:
                    counter += 1
                    break

        # Popup box that states renaming is done
        done_dialog = Popup(title="File(s) Renamed!",
                            content=Label(text="Done!"),
                            size_hint=(0.5, 0.5))
        done_dialog.open()

        # Disables rename button when renaming process is complete
        self.ids.rename.disabled = True
        self.ids.rename.opacity = 0


class MainApp(App):
    def build(self):
        Builder.load_file("frontend.kv")
        return MainScreen()


MainApp().run()