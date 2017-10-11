import sqlite3

from kivy.uix.label import Label
from kivy.uix.popup import Popup

conn = sqlite3.connect('student_db.db')


def create_table():
    try:
        # conn.execute("DROP TABLE IF EXISTS students")
        conn.execute("CREATE TABLE students"
                     "("
                     "  first_name VARCHAR(22),"
                     "  last_name VARCHAR(22),"
                     "  student_id CHAR(8) PRIMARY KEY,"
                     "  phone INTEGER,"
                     "  parent_address VARCHAR(30),"
                     "  sex CHAR(1)"
                     ")"

                     )
        conn.commit()

        conn.execute("CREATE TABLE admin"
                    "("
                    "  name VARCHAR(30),"
                    " password VARCHAR(230)"
                    ")"
                    )
        conn.commit()
    except sqlite3.OperationalError as exc:
        print exc.message


def insert(f_name, l_name, std_id, phone, address, sex):
    try:
        conn.execute("INSERT INTO students "
                     "   (first_name,last_name,student_id,phone,parent_address,sex)"
                     "  VALUES "
                     "  (?,?,?,?,?,?)",
                     (f_name, l_name, std_id, phone, address, sex))
        conn.commit()

    except sqlite3.OperationalError as exc:
        Popup(conttent=Label(text=str(exc.message)), size_hint=(None, None), size=(200, 200)).open()





"""conn.execute("INSERT INTO admin "
             "(  name,password)"
             "  VALUES "
             "(?,?)",
             ("admin","password"))
             
conn.commit()
"""

