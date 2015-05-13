from tkinter import *
from tkinter import ttk
from tkinter.colorchooser import askcolor

class ComboColorBox:
    def __init__(self, parent, colors):
        self.parent = parent
        self.colors = colors
        style = ttk.Style()
        style.theme_use('default')
        """
        Creér un style pour les bouttons qui seront utilisé dans le jeu
        """
        
        style.configure('default.TMenubutton',
                        background='white',
                        foreground='black',
                        font=('Arial Rounded MT', 18, 'bold')
                        )
        style.map('default.TMenubutton',
                  background=[('disabled', 'magenta'),
                              ('pressed', 'gray'),
                              ('active', 'gray90')]
                  )
        # Ajouter les couleurs déjà utilisées avant:
        # - - - TODO - - -
        # create the option menu
        self.__colorVar = StringVar()
        self.om = ttk.OptionMenu(self.parent.window, self.__colorVar, *self.colors,style="default.TMenubutton")
        self.__colorVar.set(self.colors[1]) # Par défaut
        
        apercu = Frame(self.parent.window, bg=self.__colorVar.get(),relief=RAISED,
                       borderwidth=2,
                       width=self.om.winfo_reqheight(),
                       height=self.om.winfo_reqheight()
                       )
        apercu.pack(side=LEFT,padx=5,pady=5)

        self.om['menu'].add_separator()
        self.om['menu'].add_command(label="Autre...",command=lambda:self.checkAutre(self.om,apercu))
        self.createColorIcon(self.om)
        self.om.pack(side=LEFT,pady=5)

        self.om.bind('<Configure>',lambda e: apercu.config(bg=self.__colorVar.get()))

    def createColorIcon(self,widget):
        # the color images are garbage collected if not saved
        self.__colorImgs = []  # Vérifier si ca va pas dans le init
        
        for i in range(len(self.colors)+1): # Car on à "le séparateur"
            size = 16
            try:
                c = widget['menu'].entryconfigure(i, 'label')[-1]
            except:
                # S'applique lors de la lecture du séparateur
                c = 'Autre...' 

            if c != 'Autre...':
                img = PhotoImage(name='image_'.join(c),
                                 width=size, height=size)
                img.put(c, to=(1,1,size-1,size-1))   # color the image
                # Cadre
                img.put('Black', to=(1,1,size-1,2))
                img.put('Black', to=(1,1,2,size-1))
                img.put('Black', to=(size-1,1,size-2,size-1))
                img.put('Black', to=(1,size-1,size-1,size-2))
                self.__colorImgs.append(img) # save the image
                 
                # attach the image to its color name
                widget['menu'].entryconfigure(i, image=img,
                                          hidemargin=True)
        widget.pack(side=RIGHT, padx=25, pady=25)

    def checkAutre(self,widget,fr):
        new_col = askcolor()[1]
        if new_col != None:
            self.colors.append(new_col)
            widget['menu'].add_command(label=new_col,
                                       command=lambda:self.otherColorSelect(new_col,fr))
            self.__colorVar.set(new_col)
            self.createColorIcon(widget)

    def otherColorSelect(self,color,fr):
        self.__colorVar.set(color)
        fr.config(bg = color)
        
    def getColor(self):
        return self.__colorVar.get()
    
    def getColorVal(self):
        return self.colorVal
    
    def set(self, elem):
        self.__colorVar.set(elem)
    
