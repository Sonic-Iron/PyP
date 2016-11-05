global root, progress, progc, compress, target, extensions, confframe, comptypes, compto, start_compression, startframe, locentry, toentry

import os, sys, time, threading

extensions = ['py', 'txt', 'bat']
comp_types = ['PyP', 'Python'] #Default is first
print('PyP')

import tkinter as tk

root = tk.Tk()
root.title('PyP')

class data:
    class images:
        icon = tk.PhotoImage(file=sys.path[0] + '/icon.png')

def progresscanvas(canvas, width=100, height=50):
    canvas.create_rectangle(5, 5, width, height, fill='red', outline='red')
    class actions:
        def step(canvas, tolsteps, width=100, height=50):
            canvas.create_rectangle(10, 10, 10 + tolsteps, height - 5, fill='blue', outline='blue')
    return actions

compress = False
decompress = False

def start_compression():
    global compress, progress, progc, confframe
    progress = tk.Canvas(root, width=100, height=50)
    progc = progresscanvas(progress)
    progress.pack()
    compress = True

def compression():
    while not compress:
        pass
    global confframe, toentry, locentry, target, compto
    target = locentry.get()
    compto = toentry.get()
    if target[len(target)-1] != '/':
        target = target + '/'
    steps = 17
    folders = []
    files = []
    ctype = comptypes.curselection()
    try:
        ctype = ctype[0]
    except IndexError:
        ctype = 0
    ctype = comp_types[ctype]
    try:
        confframe.destroy()
    except tk.TclError:
        pass
    def scan(self, d):
        global items
        for thing in os.listdir(d):
            if not thing == d[0]:
                try:
                    scan(self, d + '/' + thing)
                    folders.append(d + '/' + thing)
                except OSError:
                    catch = False
                    for extension in extensions:
                        if thing[len(thing)-len(extension):] == extension:
                            catch = True
                    if catch:
                        files.append(d + '/' + thing)
    scan(scan, target)
    total = 0
    step = 85 / (len(folders) + len(files))
    pos = 1
    if ctype == 'PyP':
        file = open(compto, 'w')
        file.write(target + '$\n')
        file.close()
        file = open(compto, 'a')
        for item in folders:
            file.write(item + '\n')
            progc.step(progress, step * pos)
            pos = pos + 1
        file.write('$\n')
        for item in files:
            file.write(item + ':')
            try:
                f = open(item, 'r')
                file.write(f.read() + '\n!divider!\n')
                f.close()
            except OSError:
                file.write('PyP - Error while packing\n')
                print('Error while writing in ' + item)
            progc.step(progress, step * pos)
            pos = pos + 1
        file.close()
    elif ctype == 'Python':
        file = open(compto, 'w')
        file.write('''import os
os.system('title PyP Unpacker')
print('PyP Unpacker - make sure you want to unpack into this directory')
input('If so, press enter')
print('Unpacking...')

#Auto generated code:
''')
        file.close()
        file = open(compto, 'a')
        file.write('os.mkdir("' + target + '")')
        for item in folders:
            file.write('\nos.mkdir("' + item + '")')
            progc.step(progress, step * pos)
            pos = pos + 1
        for item in files:
            file.write('''
file = open("''' + item + '''", 'w')
''')
            f = open(item, 'r')
            file.write('file.write("""' + f.read() + '""")\nfile.close()')
            f.close()
            progc.step(progress, step * pos)
            pos = pos + 1
        file.write('\ninput("Done!")')
        file.close()
    def showfile():
        os.popen('"' + sys.path[0] + '/' + compto + '"')
    donelabel = tk.Label(root, text='Done!')
    donelabel.pack(side=tk.BOTTOM)
    donebutton = tk.Button(root, text='Show', command=showfile)
    donebutton.pack(side=tk.BOTTOM, fill=tk.X)

def start_decompression():
    global decompress
    decompress = True

def decompression():
    global toentry, locentry
    while not decompress:
        pass
    progress = tk.Canvas(root, width=100, height=50)
    progc = progresscanvas(progress)
    progress.pack()
    locentry = locentry.get()
    toentry = toentry.get()
    confframe.destroy()
    if toentry[len(toentry)-1] != '/':
        toentry = toentry + '/'
    file = open(locentry, 'r')
    todo = file.read()
    file.close()
    target, folders, files = todo.split('$')
    os.mkdir(toentry + target)
    step = 85 / (1 + len(folders.split('\n')) + len(files.split('\n!divider!\n')))
    pos = 1
    progc.step(progress, step * pos)
    pos = pos + 1
    for item in folders.split('\n'):
        if not item == '':
            os.mkdir(toentry + item)
        progc.step(progress, step * pos)
        pos = pos + 1
    for item in files.split('\n!divider!\n'):
        if not item == '':
            name, contents = item.split(':')
            if name[:1] == '\n':
                name = name[1:]
            file = open(toentry + name, 'w')
            file.write(contents)
            file.close()
        progc.step(progress, step * pos)
        pos = pos + 1
    donelabel = tk.Label(root, text='Done!')
    donelabel.pack(side=tk.BOTTOM)

def c():
    global confframe, comptypes, locentry, toentry
    startframe.destroy()
    confframe = tk.Frame(root)
    comptypes = tk.Listbox(confframe)
    loclabel = tk.Label(confframe, text='Item to pack')
    locentry = tk.Entry(confframe)
    tolabel = tk.Label(confframe, text='Pack into')
    toentry = tk.Entry(confframe)
    loclabel.pack(anchor='nw')
    locentry.pack(anchor='nw')
    tolabel.pack(anchor='nw')
    toentry.pack(anchor='nw')
    gobutton = tk.Button(confframe, text='Start', command=start_compression)
    for t in comp_types:
        comptypes.insert(tk.END, t)
    comptypes.pack(side=tk.TOP)
    gobutton.pack(side=tk.TOP, fill=tk.X)
    confframe.pack()
    compression_thread = threading.Thread(target=compression, name='Packer Thread')
    compression_thread.daemon = True
    compression_thread.start()

def d():
    global confframe, locentry, toentry
    startframe.destroy()
    confframe = tk.Frame(root)
    gobutton = tk.Button(confframe, text='Start', command=start_decompression)
    loclabel = tk.Label(confframe, text='Item to unpack')
    locentry = tk.Entry(confframe)
    tolabel = tk.Label(confframe, text='Unpack to')
    toentry = tk.Entry(confframe)
    loclabel.pack(side=tk.LEFT)
    locentry.pack(side=tk.LEFT)
    tolabel.pack(side=tk.LEFT)
    toentry.pack(side=tk.LEFT)
    gobutton.pack(side=tk.RIGHT, fill=tk.X)
    confframe.pack()
    decompression_thread = threading.Thread(target=decompression, name='Unpacker Thread')
    decompression_thread.daemon = True
    decompression_thread.start()

root.iconphoto(True, data.images.icon)

startframe = tk.Frame()
comp = tk.Button(startframe, text='Pack a directory', command=c)
decomp = tk.Button(startframe, text='Unpack PyP files', command=d)

startframe.pack()
comp.pack(fill=tk.X)
decomp.pack(fill=tk.X)

root.mainloop()
