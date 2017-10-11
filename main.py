import re

from kivy.uix.textinput import TextInput

import model
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
import sqlite3


class ErrorPopup(Popup):
    pass


class AddStudent(Screen):
    first_name = ObjectProperty(None)
    last_name = ObjectProperty(None)
    student_id = ObjectProperty(None)
    phone_number = ObjectProperty(None)
    parent_address = ObjectProperty(None)
    male_check = ObjectProperty(None)
    female_check = ObjectProperty(None)

    def insert_student(self):
        if self.validate_input():
            model.insert(self.first_name.text, self.last_name.text, self.student_id.text.upper(),
                         self.phone_number.text,
                         self.parent_address.text, self.validate_check())

            print "Student inserted"

            self.first_name.text, self.last_name.text, self.student_id.text, \
                self.phone_number.text, self.parent_address.text =\
                "", "", "", "", ""

        else:
            error_pop = ErrorPopup()
            error_pop.ids.error.text = "Failed to insert student in database.try again"
            error_pop.title = "Insert Error"
            error_pop.open()

    def validate_check(self):
        if self.male_check.state == "down":
            print "Male"
            return "M"
        if self.female_check.state == "down":
            print "Female"
            return "F"

    def validate_input(self):
        if self.first_name.text != "" and self.last_name.text != "" and self.student_id.text != "" and self.phone_number.text != "" and self.parent_address.text != "":
            print "True"
            return True
        else:
            print "False"
            return False


class RemoveStudent(Screen):
    pass


class Manager(ScreenManager):
    pass


class MainScreenManager(ScreenManager):
    pass


class Login(Screen):
    login_name = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)

    def login(self):
        try:
            conn = sqlite3.connect("student_db.db")
            curs = conn.cursor()
            curs.execute(
                "SELECT * FROM admin"
            )

            name, password = curs.fetchone()
            print name, password
            if name == self.login_name.text and password == self.password.text:
                self.manager.current = "main_screen"
                self.password.text, self.login_name.text = "", ""
                print "User logged in"
            else:
                print "Login failure"
                pop_error = ErrorPopup()
                pop_error.title = "Login failure"
                pop_error.ids.error.text = "Failed to login.Check credentials"
                pop_error.open()

        except sqlite3.OperationalError as err:
            pop_error = ErrorPopup()
            pop_error.title = "Login failure"
            pop_error.ids.error.text = err.message + " .Failed to login user"
            pop_error.open()


class MainScreen(Screen):
    pass

class FloatInput(TextInput):

    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in \
                              substring.split('.', 1)])
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class MainApp(App):
    def build(self):
        manager = Manager()
        return manager


if __name__ == '__main__':
    conn = sqlite3.connect('student_db.db')
    curs = conn.cursor()
    data = curs.execute("SELECT * FROM students")
    data = data.fetchall()
    print data
    MainApp().run()
