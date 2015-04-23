from tkinter import *
import tkinter.ttk as ttk

class A:
    def __init__(self):
        self.fenetre = Tk()
        self.fenetre['bg'] = 'black'
        style = ttk.Style()
        style.theme_use('default')
        """
        Creér un style pour les bouttons qui seront utilisé dans le jeu
        """
        style.configure('default.TButton',
                        background='white',
                        foreground='black',
                        font=('Helvetica', 18, 'bold')
                        )
        style.map('default.TButton',
                  background=[('disabled', 'magenta'),
                                ('pressed', 'gray'),
                                ('active', 'gray90')]
                  )
        ttk_btn = ttk.Button(text="yolo", style="default.TButton")
        ttk_btn.pack(padx=10,pady=10)

        """
        Autres
        """
        self.fenetre.mainloop()


A()
