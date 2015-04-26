from tkinter import *
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor

class A:
	def __init__(self):
		self.fenetre = Tk()
		# creates a 'color palette' as an 'option menu'
		# the default placement (direction) of the popup
		# menu is 'below' the button; the direction
		# can be any of: right, left, above and flush
 
		# the first value appears to be internally
		# reserved for the associated StringVar value
		# if it is not left blank, the first color will
		# not appear in the palette and all subsequent
		# color/name matchups are off by 1
		self.colors = ['','White','Yellow', 'Pink', 'Red', 'Blue', 'Green', 'Orange']
		# Ajouter les couleurs déjà utilisées avant:
		# - - - TODO - - -
		# create the option menu
		self.__colorVar = StringVar()  
		om = ttk.OptionMenu(self.fenetre, self.__colorVar, *self.colors,
							direction='flush')
		self.__colorVar.set(self.colors[1]) # Par défaut
#		om.bind("<Configure>",lambda e:self.checkAutre(om)) 
		om['menu'].add_separator()
		om['menu'].add_command(label="Autre...",command=lambda:self.checkAutre(om))
		self.createColorIcon(om)
		om.pack(padx=20,pady=20)

		self.fenetre.mainloop()


	def createColorIcon(self,widget):
		# the color images are garbage collected if not saved
		self.__colorImgs = []  # Vérifier si ca va pas dans le init
		
		for i in range(len(self.colors)+1): # Car on à "le séparateur"
			w = 16 

			try:
				c = widget['menu'].entryconfigure(i, 'label')[-1]
			except:
				# S'applique lors de la lecture du séparateur
				c = 'Autre...' 

			if c != 'Autre...':
				img = PhotoImage(name='image_'.join(c),
								 width=w, height=w)
				img.put(c, to=(1,1,w-1,w-1))   # color the image
				# Cadre
				img.put('Black', to=(1,1,w-1,2))
				img.put('Black', to=(1,1,2,w-1))
				img.put('Black', to=(w-1,1,w-2,w-1))
				img.put('Black', to=(1,w-1,w-1,w-2))
				self.__colorImgs.append(img) # save the image
				 
				# attach the image to its color name
				widget['menu'].entryconfigure(i, image=img,
										  hidemargin=True)
				 
				if not i%4:   # display in grid, 4 across
					widget['menu'].entryconfigure(i, columnbreak=True)
		 
		# if used, the 'tearoff' appears to the left of the palette
		# rather than 'above' it; also, if it is set to
		# 'True' BEFORE the images are created the 'columnbreak'
		# entry option is not recognized 
		   
		#widget['menu'].configure(tearoff=True) 

		widget.pack(side=RIGHT, padx=25, pady=25)

	def checkAutre(self,widget):
		new_col = askcolor()[1]
		if new_col != None:
			self.colors.append(new_col)
			widget['menu'].add_command(label=new_col,command=self.__colorVar.set(new_col))
			self.__colorVar.set(new_col)
			self.createColorIcon(widget)



	"""
	# Marche pas super :( 
	def setFrameColor(self, color):
		res = "Black"
		fr = Frame()
		rgb = fr.winfo_rgb(color)
		max_val_rgb = 65535*3 # Comme c'est sur 16 bits
		val_rgb = sum(rgb)
		if val_rgb < 2*max_val_rgb//5: # Si la couleur est (plutot) foncée
			res = "White"
		return res

	"""

A()
