from argparse import ArgumentParser, Namespace
import os
import sys
import traceback
import webbrowser
from os import path
from tkinter import *
from tkinter import Tk, messagebox, filedialog
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
from mangareader.mangarender import extract_render
from mangareader import templates
from time import sleep

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "lue.ui")

class LueWidget(ttk.Frame):  
    def __init__(self, master=None, **kw):
        super(LueWidget, self).__init__(master, **kw)

        ##main()

        self.orient = IntVar()
        self.color = IntVar()
        # path = ""
        
        self.title = ttk.Label(self)
        self.title.configure(anchor='ne', compound='top', font='TkTextFont')
        self.title.configure(justify='left', padding='5', takefocus=True, text='Comic title')
        self.title.grid(column='0', row='0')
        self.title_entry = ttk.Entry(self)
        _text_ = '''Comic'''
        self.title_entry.delete('0', 'end')
        self.title_entry.insert('0', _text_)
        self.title_entry.grid(column='0', row='1')
        self.author = ttk.Label(self)
        self.author.configure(compound='bottom', padding='5', takefocus=False)
        self.author.configure(text='Author')
        self.author.grid(column='0', row='2')
        self.author_entry = ttk.Entry(self)
        self.author_entry.configure(cursor='arrow', justify='left')
        _text_ = '''Author'''
        self.author_entry.delete('0', 'end')
        self.author_entry.insert('0', _text_)
        self.author_entry.grid(column='0', row='3')
        self.html = ttk.Label(self)
        self.html.configure(compound='top', cursor='arrow', justify='left', padding='5')
        self.html.configure(text='Image Directory')
        self.html.grid(column='0', row='4')
        self.html_entry = PathChooserInput(self)
        self.html_entry.configure(type='directory')
        self.html_entry.grid(column='0', row='5')
        self.orientation = ttk.Label(self)
        self.orientation.configure(padding='5', text='Reading orientation')
        self.orientation.grid(column='0', row='6')
        self.v_orientation = ttk.Radiobutton(self)
        self.v_orientation.configure(text='Vertical', variable=self.orient, value=1)
        self.v_orientation.grid(column='0', row='7')
        self.h_orientation = ttk.Radiobutton(self)
        self.h_orientation.configure(text='Horizontal', variable=self.orient, value=2)
        self.h_orientation.grid(column='0', row='8')
        self.bg = ttk.Label(self)
        self.bg.configure(anchor='n', justify='left', padding='5', text='Background color')
        self.bg.grid(column='0', row='9')
        self.l_bg = ttk.Radiobutton(self)
        self.l_bg.configure(text='Light', variable=self.color, value=1)
        self.l_bg.grid(column='0', row='10')
        self.d_bg = ttk.Radiobutton(self)
        self.d_bg.configure(text='Dark', variable=self.color, value=2)
        self.d_bg.grid(column='0', row='11')
        self.button1 = ttk.Button(self)
        self.button1.configure(text='Submit', command=lambda : submit(self))
        self.button1.grid(column='0', row='12')
        
def submit(self):
    main(self, self.html_entry.cget('path'))

def parse_args() -> Namespace:
    parser = ArgumentParser(description='Mangareader')
    parser.add_argument('path', nargs='?', help='Path to image, folder, or comic book archive')
    parser.add_argument('--no-browser', action='store_true')
    return parser.parse_args()

def main(self, filepath) -> None:
    args = parse_args()
    target_path = filepath
    ##target_path = args.path
    working_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    lib_dir = f'{working_dir}/mangareader'
    with open(f'{working_dir}/version', encoding='utf-8') as version_file:
        version = version_file.read().strip()
    if self.color == 1:
        dark = False
    else:
        dark = True
    if self.orient == 1:
        horizontal = False
    else:
        horizontal = True
    try:
        boot_path = extract_render(
            path=target_path,
            version=version,
            doc_template_path=f'{lib_dir}/doc.template.html',
            page_template_path=f'{lib_dir}/img.template.html',
            boot_template_path=f'{lib_dir}/boot.template.html',
            asset_paths=(f'{lib_dir}/{asset}' for asset in templates.ASSETS),
            img_types=templates.DEFAULT_IMAGETYPES,
            dark=dark,
            horizontal=horizontal,
            input_title=self.title_entry.get() + " - By " + self.author_entry.get()
        )
        if args.no_browser:
            print(boot_path)
        else:
            webbrowser.open(boot_path.as_uri())
    except Exception as e:
        Tk().withdraw()
        messagebox.showerror(
            'Mangareader encountered an error: ' + type(e).__name__, ''.join(traceback.format_exc())
        )
    # # Read in the file
    # with open(filepath, 'r') as file :
        # filedata = file.read()

    # # Replace the target string
    # filedata = filedata.replace('ram', 'abcd')

    # # Write the file out again
    # with open('file.txt', 'w') as file:
        # file.write(filedata)


# if __name__ == '__main__':
    # main()

if __name__ == '__main__':
    root = tk.Tk()
    widget = LueWidget(root)
    widget.pack(expand=True, fill='both')
    root.mainloop()
