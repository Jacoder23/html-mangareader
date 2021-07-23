import os
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "lue.ui")

class LueWidget(ttk.Frame):
    def __init__(self, master=None, **kw):
        super(LueWidget, self).__init__(master, **kw)
        self.title = ttk.Label(self)
        self.title.configure(anchor='ne', compound='top', cursor='based_arrow_down', font='TkTextFont')
        self.title.configure(justify='left', padding='5', takefocus=True, text='Comic title')
        self.title.grid(column='0', row='0')
        self.title_entry = ttk.Entry(self)
        _text_ = '''entry3'''
        self.title_entry.delete('0', 'end')
        self.title_entry.insert('0', _text_)
        self.title_entry.grid(column='0', row='1')
        self.author = ttk.Label(self)
        self.author.configure(compound='bottom', cursor='based_arrow_down', padding='5', takefocus=False)
        self.author.configure(text='Author')
        self.author.grid(column='0', row='2')
        self.author_entry = ttk.Entry(self)
        self.author_entry.configure(cursor='arrow', justify='left')
        _text_ = '''entry5'''
        self.author_entry.delete('0', 'end')
        self.author_entry.insert('0', _text_)
        self.author_entry.grid(column='0', row='3')
        self.html = ttk.Label(self)
        self.html.configure(compound='top', cursor='arrow', justify='left', padding='5')
        self.html.configure(text='HTML File')
        self.html.grid(column='0', row='4')
        self.html_entry = PathChooserInput(self)
        self.html_entry.configure(type='file')
        self.html_entry.grid(column='0', row='5')
        self.orientation = ttk.Label(self)
        self.orientation.configure(padding='5', text='Reading orientation?')
        self.orientation.grid(column='0', row='6')
        self.v_orientation = ttk.Radiobutton(self)
        self.v_orientation.configure(text='Vertical')
        self.v_orientation.grid(column='0', row='7')
        self.h_orientation = ttk.Radiobutton(self)
        self.h_orientation.configure(cursor='arrow', state='normal', text='Horizontal')
        self.h_orientation.grid(column='0', row='8')
        self.bg = ttk.Label(self)
        self.bg.configure(anchor='n', justify='left', padding='5', text='Background color')
        self.bg.grid(column='0', row='9')
        self.l_bg = ttk.Radiobutton(self)
        self.l_bg.configure(takefocus=False, text='Light')
        self.l_bg.grid(column='0', row='10')
        self.d_bg = ttk.Radiobutton(self)
        self.d_bg.configure(text='Dark')
        self.d_bg.grid(column='0', row='11')


if __name__ == '__main__':
    root = tk.Tk()
    widget = LueWidget(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()

