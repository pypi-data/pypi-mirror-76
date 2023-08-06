#! Python
# 2020 Novus Space

import tkinter as tk

textList = []
fontSizeList = []

class initGuiClass(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.frame = tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.parent.title(frameTitle)
        self.parent.geometry(frameGeometry)

        i = 0
        j = 0
        while i < len(textList):
            if j < len(fontSizeList):
                print(fontSizeList[j])
                a = tk.Label(self.frame, text=textList[i])
                a.configure(font=fontSizeList[j])
                a.pack()
                print(a)
                j += 1
            i += 1


def initGui(frame_title, frame_geometry):
    global frameTitle, frameGeometry, root
    frameTitle = getTitle(frame_title)
    frameGeometry = getGeometry(frame_geometry)

    root = tk.Tk()
    initGuiClass(root).pack(side="top", fill="both", expand=True)
    root.mainloop()

def addText(textVar, fontSizeVar):
    textList.append(str(textVar))
    fontSizeList.append(int(fontSizeVar))


# Returns functions

def getTitle(title_frame):
    return title_frame

def getGeometry(geometry):
    return geometry


'''
self.menu = tk.Menu(self.frame)
        #self.openFile = self.menu.add_command(label='Open File', command=self.openFile)

        self.parent.config(menu=self.menu)

        self.title = tk.Label(self.frame, text='Novus Space')
        self.title.configure(font=20)
        self.version = tk.Label()
        self.aboutText = tk.Label(self.frame, text='This software can plot your data from a text file,\n '
                                                   'for example data from a rocket flight')
        self.statusUpdate1 = tk.Label(self.frame, text='updating...')
        self.statusUpdate2 = tk.Label(self.frame, text='no update available')

        self.title.pack()
        self.version.pack()
        self.aboutText.pack()

        self.progressBar = ttk.Progressbar(self.frame, orient='horizontal', length=100, mode='determinate')
        self.bytes = 0
        self.maxbytes = 0'''

