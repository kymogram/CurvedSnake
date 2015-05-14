from tkinter import *
from tkinter.font import Font
from tkinter import ttk
from tkinter.colorchooser import askcolor


class ComboColorBox:
    def __init__(self, parent, master, colors):
        self.master = master
        self.parent = parent
        self.colors = colors
        style = ttk.Style()
        style.theme_use('default')
        font = Font(family='Arial Rounded MT', size=18, weight='bold')
        style.configure('default.TMenubutton', bg=self.parent.current_bg,
                        fg=self.parent.current_fg, font=font)
        style.map('default.TMenubutton',
                  background=[('disabled', 'magenta'),
                              ('pressed', 'gray'),
                              ('active', 'gray90')])
        self.currentColor = StringVar()
        self.colors_menu = ttk.OptionMenu(self.master, self.currentColor,
                                          *self.colors,
                                          style="default.TMenubutton")
        self.currentColor.set(self.colors[1])  # default value
        apercu = Frame(self.master, bg=self.currentColor.get(), relief=RAISED,
                       borderwidth=2, width=self.colors_menu.winfo_reqheight(),
                       height=self.colors_menu.winfo_reqheight())
        apercu.pack(side=LEFT, padx=5, pady=5)

        self.colors_menu['menu'].add_separator()
        callback = lambda: self.askOther(self.colors_menu, apercu)
        self.colors_menu['menu'].add_command(label="Other...",
                                             command=callback)
        self.createColorIcon(self.colors_menu)
        self.colors_menu.pack(side=LEFT, pady=5)
        callback = lambda e: apercu.config(bg=self.currentColor.get())
        self.colors_menu.bind('<Configure>', callback)

    def createColorIcon(self, widget):
        # the color images are garbage collected if not saved
        self.__colorImgs = []
        for i in range(len(self.colors)+1):  # do not forget the separator
            size = 16
            try:
                c = widget['menu'].entryconfigure(i, 'label')[-1]
                img = PhotoImage(name='image_'.join(c),
                                 width=size, height=size)
                img.put(c, to=(1, 1, size-1, size-1))  # color the image
                img.put('Black', to=(1, 1, size-1, 2))
                img.put('Black', to=(1, 1, 2, size-1))
                img.put('Black', to=(size-1, 1, size-2, size-1))
                img.put('Black', to=(1, size-1, size-1, size-2))
                self.__colorImgs.append(img)  # save the image
                # attach the image to its color name
                widget['menu'].entryconfigure(i, image=img, hidemargin=True)
            except:
                pass
        widget.pack(side=RIGHT, padx=25, pady=25)

    def askOther(self, widget, frame):
        new_col = askcolor()[1]
        if new_col is not None:
            self.colors.append(new_col)
            callback = lambda: self.otherColorSelect(new_col, frame)
            widget['menu'].add_command(label=new_col, command=callback)
            self.currentColor.set(new_col)
            self.createColorIcon(widget)

    def otherColorSelect(self, color, frame):
        self.currentColor.set(color)
        frame.config(bg=color)

    def getColor(self):
        return self.currentColor.get()

    def getColorVal(self):
        return self.currentColor

    def getListAllColors(self):
        return self.colors

    def set(self, elem):
        self.currentColor.set(elem)
