from argparse import ArgumentParser, Namespace
import os
import sys
import traceback
import webbrowser
from os import path
import glob
from tkinter import *
from tkinter import Tk, messagebox, filedialog
import tkinter as tk
import tkinter.ttk as ttk
from pygubu.widgets.pathchooserinput import PathChooserInput
from mangareader.mangarender import extract_render
from mangareader import templates
from time import sleep
import shutil, errno

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "lue.ui")

class LueWidget(ttk.Frame):  

    # https://stackoverflow.com/a/17548459
    def inplace_change(self, filename, old_string, new_string):
        # Safely read the input filename using 'with'
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print('"{old_string}" not found in {filename}.'.format(**locals()))
                return

        # Safely write the changed content, if found in the file
        with open(filename, 'w') as f:
            print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)
        
    def copyanything(self, src, dst):
        try:
            shutil.copytree(src, dst)
        except OSError as exc: # python >2.5
            if exc.errno in (errno.ENOTDIR, errno.EINVAL):
                shutil.copy(src, dst)
            else: raise

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
        self.button1.configure(text='Render', command=lambda : submit(self))
        self.button1.grid(column='0', row='12')
        
def submit(self):
    main(self, self.html_entry.cget('path'))

def parse_args() -> Namespace:
    parser = ArgumentParser(description='Mangareader')
    parser.add_argument('path', nargs='?', help='Path to image, folder, or comic book archive')
    parser.add_argument('--no-browser', action='store_true')
    return parser.parse_args()

def main(form, filepath) -> None:
    assets = list(templates.ASSETS)
    args = parse_args()
    target_path = filepath
    ##target_path = args.path
    working_dir = getattr(sys, '_MEIPASS', path.abspath(path.dirname(__file__)))
    lib_dir = f'{working_dir}/mangareader'
    with open(f'{working_dir}/version', encoding='utf-8') as version_file:
        version = version_file.read().strip()
    if form.color.get() == 1:
        dark = False
        if form.orient.get() == 1:
            horizontal = False
            assets[1] = "scripts - LV.js"
        else:
            horizontal = True
            assets[1] = "scripts - LH.js"
    else:
        dark = True
        if form.orient.get() == 1:
            horizontal = False
            assets[1] = "scripts - DV.js"
        else:
            horizontal = True
            assets[1] = "scripts - DH.js"
            
    print("Dark: " + str(dark))
    print("Horizontal: " + str(horizontal))
    print(filepath)
    try:
        boot_path = extract_render(
            path=target_path,
            version=version,
            doc_template_path=f'{lib_dir}/doc.template.html',
            page_template_path=f'{lib_dir}/img.template.html',
            boot_template_path=f'{lib_dir}/boot.template.html',
            asset_paths=(f'{lib_dir}/{asset}' for asset in set(assets)),
            img_types=templates.DEFAULT_IMAGETYPES,
            dark=dark,
            horizontal=horizontal,
            input_title=form.title_entry.get() + " - By " + form.author_entry.get()
        )
        if args.no_browser:
            print(boot_path)
        else:
            webbrowser.open(boot_path.as_uri())
        export_path = filedialog.askdirectory()
        print(os.path.dirname(boot_path))
        print(export_path)
        comicTitle = form.title_entry.get()
        final_export_path = os.path.join(export_path,''.join(comicTitle.split()).lower())
        print(final_export_path)
        form.copyanything(os.path.dirname(boot_path), final_export_path)
        
        # just using urllib.parse fucks this up somehow
        # this is hardly production ready but hey im they only one who cares about this and has to clean up if something goes wrong so good enough
        form.inplace_change(os.path.join(final_export_path, "index.html"), "file:///" + filepath.replace(" ", "%20").replace(",", "%2C").replace("[", "%5B").replace("]", "%5D"), "https://ashsgrafiction.com/comics/")
    except Exception as e:
        Tk().withdraw()
        messagebox.showerror(
            'Lue Comic Generator encountered an error: ' + type(e).__name__, ''.join(traceback.format_exc())
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