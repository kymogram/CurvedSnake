from tkinter import *

fenetre = Tk()
photo = PhotoImage(file="testgif.gif")

canvas = Canvas(fenetre,width=350, height=200)
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.pack()
fenetre.mainloop()