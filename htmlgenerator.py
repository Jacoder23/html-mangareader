import sys
import os
import tempfile
from string import Template
import pathlib
import zipfile
import webbrowser

import templates
from excepts import ImagesNotFound

# todo: take list of explicit image paths, which are passed in from listdir or the unzip
def render_from_template(path,
                         doc_template, page_template, img_types,
                         outfile=os.path.join(tempfile.gettempdir(), 'html-mangareader', 'render.html')):
    files = filter(lambda e: os.path.isfile(os.path.join(path, e)),
                   os.listdir(path))
    imagefiles = filter(lambda f: f.split('.')[-1].lower() in img_types, files)
    if not imagefiles:
        raise ImagesNotFound('No image files were found in path: {0}'.format(path))
    imagepaths = [pathlib.Path(os.path.join(path, p)).as_uri() for p in sorted(imagefiles, key=str.lower)]
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w', encoding='utf-8', newline='\r\n') as renderfd:
        html_template = Template(doc_template)
        img_template = Template(page_template)
        img_list = [img_template.substitute(img=imagepaths[i], id=i, previd=(i-1), nextid=(i+1))
                    for i in range(0, len(imagepaths))]
        doc_string = html_template.substitute(body=''.join(img_list))
        renderfd.write(doc_string)
    print("view saved to " + outfile)
    return outfile

def extract_zip(path, img_types, outpath=os.path.join(tempfile.gettempdir(), 'html-mangareader')):
    with zipfile.ZipFile(path, mode='r') as zip_file:
        imagefiles = filter(lambda f: f.split('.')[-1].lower() in img_types, zip_file.namelist())
        if not imagefiles:
            raise ImagesNotFound('No image files were found in archive: {}'.format(path))
        zip_file.extractall(outpath, imagefiles)
        return outpath

def extract_render(path, doc_template, page_template, img_types, outpath):
    imgpath = path
    if os.path.isfile(path):
        try:
            imgpath = extract_zip(path, img_types)
        except zipfile.BadZipFile:
            print('{} does not appear to be a valid zip/cbz file.'.format(path))
            return
    try:
        renderfile = render_from_template(imgpath, doc_template, page_template, img_types)
        webbrowser.open(renderfile)
    except ImagesNotFound as e:
        print(e)
        return
    return

if __name__ == '__main__':
    path = '.' if len(sys.argv) <= 1 else sys.argv[1]
    # render_from_template(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES, os.path.join(path, 'render.html'))
    # render_from_template(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES)
    # outpath = extract_zip('testar.zip', templates.DEFAULT_IMAGETYPES)
    # print(outpath)
    extract_render(path, templates.DOC_TEMPLATE, templates.IMG_TEMPLATE, templates.DEFAULT_IMAGETYPES, None)