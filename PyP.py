global root, progress, progc, compress, target, extensions, confframe, comptypes, compto, start_compression, startframe

import os, sys, time, threading

target = 'To compress'
compto = 'C:/Users/David/Documents/GitHub/PyP/compression.txt'
extensions = ['py', 'png', 'txt']
comp_types = ['PyP', 'xd'] #Default is first
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

def start_compression():
    global compress, progress, progc, confframe
    progress = tk.Canvas(root, width=100, height=50)
    progc = progresscanvas(progress)
    progress.pack()
    compress = True

def compression():
    global confframe
    while not compress:
        pass
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
    file = open(compto, 'w')
    file.write('')
    file.close()
    file = open(compto, 'a')
    for item in folders:
        file.write(item + '\n')
        progc.step(progress, step * pos)
        pos = pos + 1
    file.write('$\n')
    for item in files:
        file.write(item + '\n')
        try:
            f = open(item, 'r')
            file.write(f.read() + '\n')
            f.close()
        except OSError:
            file.write('Error\n')
            print('Error while writing in ' + item)
        progc.step(progress, step * pos)
        pos = pos + 1
    file.close()

def start_decompression():
    

def decompression():
    confframe.destroy()
    start_decompression()

def c():
    global confframe, comptypes
    startframe.destroy()
    confframe = tk.Frame(root)
    comptypes = tk.Listbox(confframe)
    gobutton = tk.Button(confframe, text='Start', command=start_compression)
    for t in comp_types:
        comptypes.insert(tk.END, t)
    comptypes.pack(side=tk.TOP)
    gobutton.pack(side=tk.TOP, fill=tk.X)
    confframe.pack()
    compression_thread = threading.Thread(target=compression, name='Compression Thread')
    compression_thread.daemon = True
    compression_thread.start()

def d():
    global confframe, comptypes
    startframe.destroy()
    confframe = tk.Frame(root)
    gobutton = tk.Button(confframe, text='Start', command=start_decompression)
    gobutton.pack(side=tk.TOP, fill=tk.X)
    confframe.pack()
    decompression_thread = threading.Thread(target=decompression, name='Decompression Thread')
    decompression_thread.daemon = True
    decompression_thread.start()

root.iconphoto(True, data.images.icon)

startframe = tk.Frame()
comp = tk.Button(startframe, text='Compress', command=c)
decomp = tk.Button(startframe, text='Decompress', command=d)

startframe.pack()
comp.pack()
decomp.pack()

root.mainloop()
