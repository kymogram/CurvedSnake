from tkinter import *
import tkinter.ttk as ttk
 
class MenuButtonsDemo(ttk.Frame):
     
    def __init__(self, isapp=True, name='menubuttonsdemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Menu Buttons Demo')
        self.isapp = isapp
        self._create_demo_panel()
         
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
         
        self._below_btn(demoPanel)
        self._left_btn(demoPanel)
        self._center_panel(demoPanel)
        self._right_btn(demoPanel)
        self._above_btn(demoPanel)
         
    def _below_btn(self, parent):
        menu = Menu(parent, tearoff=False)
        mb = ttk.Menubutton(parent, text='Below', underline=0, direction='below',
                            menu=menu)
        menu.add_command(label='Below menu: first item')
        menu.add_command(label="Below menu: second item")
        mb.grid(row=0, column=1, sticky=N)
         
    def _left_btn(self, parent):
        menu = Menu(parent, tearoff=False)
        mb = ttk.Menubutton(parent, text='Left', underline=0,
                            direction='left', menu=menu)
        menu.add_command(label='Left menu: first item')
        menu.add_command(label='Left menu: seconditem')
        mb.grid(row=1, column=2, sticky=E)
     
    def _center_panel(self, parent):
        txt = ['This is a demonstration of menubuttons. The "Below" ',
               'menubutton pops its menu below the button; the "Right" ',
               'button pops to the right, etc.\n\nThere are two option ',
               'menus directly below this text; one is just a standard ',
               'menu and the other is a 15-color palette.']
         
        frame = ttk.Frame(parent)
        label = ttk.Label(frame, wraplength=300, font='Helvictica 14',
                          justify=LEFT,text=''.join(txt))
        label.pack(side=TOP, padx=25, pady=25)
         
        # option menus
        self._create_option_menu_one(frame)
        self._create_color_palette(frame)
         
        frame.grid(row=1, column=1, sticky='news')
         
    def _create_option_menu_one(self, parent):
        # Note that the 0-index of the values appears
        # to be reserved for the associated StringVar value
        # if the first value is not left blank, it will
        # not display in the pop-up
        self.__optVar = StringVar()
        om1 = ttk.OptionMenu(parent, self.__optVar, *('','one', 'two', 'three'),
                             direction='flush')
        self.__optVar.set('one')
        om1.pack(side=LEFT, padx=25, pady=25)
                 
    def _create_color_palette(self, parent):
        # creates a 'color palette' as an 'option menu'
        # the default placement (direction) of the popup
        # menu is 'below' the button; the direction
        # can be any of: right, left, above and flush
 
        # the first value appears to be internally
        # reserved for the associated StringVar value
        # if it is not left blank, the first color will
        # not appear in the palette and all subsequent
        # color/name matchups are off by 1
        colors = ('', 'Black', 'red4', 'DarkGreen',
                  'NavyBlue', 'gray75', 'Red', 'Green',
                  'Blue', 'gray50', 'Yellow', 'Cyan',
                  'Magenta', 'White', 'Brown', 'DarkSeaGreen')
         
        # create the option menu
        self.__colorVar = StringVar(self)  
        om = ttk.OptionMenu(parent, self.__colorVar, *colors,
                            direction='flush')
        self.__colorVar.set('Black')
     
        # the color images are garbage collected if not saved
        self.__colorImgs = []  
         
        for i in range(len(colors)):
            c = om['menu'].entryconfigure(i, 'label')[-1]
 
            img = PhotoImage(name='image_'.join(c),
                             width=16, height=16)
            img.put(c, to=(1,1,15,15))   # color the image
            self.__colorImgs.append(img) # save the image
             
            # attach the image to its color name
            om['menu'].entryconfigure(i, image=img,
                                      hidemargin=False)
             
            if not i%4:   # display in grid, 4 across
                om['menu'].entryconfigure(i, columnbreak=True)
         
        # if used, the 'tearoff' appears to the left of the palette
        # rather than 'above' it; also, if it is set to
        # 'True' BEFORE the images are created the 'columnbreak'
        # entry option is not recognized 
           
        #om['menu'].configure(tearoff=True)            
         
        om.pack(side=RIGHT, padx=25, pady=25)
         
    def _right_btn(self, parent):
        menu = Menu(parent, tearoff=False)
        mb = ttk.Menubutton(parent, text='Right', underline=0, direction='right',
                            menu=menu)
        menu.add_command(label='Right menu: first item')
        menu.add_command(label='Right menu: second item')
        mb.grid(row=1, column=0, sticky=W)
         
    def _above_btn(self, parent):
        menu = Menu(parent, tearoff=False)
        mb = ttk.Menubutton(parent, text='Above', underline=0,
                            direction='above', menu=menu)
        menu.add_command(label='Above menu: first item')
        menu.add_command(label='Above menu: second item')
        mb.grid(row=2, column=1, sticky=S)
         
if __name__ == '__main__':
    MenuButtonsDemo().mainloop()