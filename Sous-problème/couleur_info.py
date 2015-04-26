from tkinter import *

fenetre = Tk()

fr = Frame()

rgb = fr.winfo_rgb("red")
print(rgb)
red, green, blue = rgb[0]/256, rgb[1]/256, rgb[2]/256

fenetre.mainloop()