from tkinter import *
import tkinter.ttk as ttk
from tkinter.colorchooser import askcolor

class A:
	def __init__(self):
		self.fenetre = Tk()
		self.fenetre['bg'] = 'black'
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
	
		self.colors = ['','White','Yellow', 'Pink', 'Red', 'Blue', 'Green', 'Orange']
		# Ajouter les couleurs déjà utilisées avant:
		# - - - TODO - - -
		# create the option menu
		self.__colorVar = StringVar()  
		om = ttk.OptionMenu(self.fenetre, self.__colorVar, *self.colors,
							direction='flush',style="default.TMenubutton")
		self.__colorVar.set(self.colors[1]) # Par défaut
		
		apercu = Frame(self.fenetre, bg=self.__colorVar.get(),relief=RAISED,
					   borderwidth=2,
					   width=om.winfo_reqheight(),
					   height=om.winfo_reqheight()
					   )
		apercu.pack(side=LEFT,padx=5,pady=5)

		om['menu'].add_separator()
		om['menu'].add_command(label="Autre...",command=lambda:self.checkAutre(om,apercu))
		self.createColorIcon(om)
		om.pack(side=LEFT,pady=5)

		om.bind('<Configure>',lambda e: apercu.config(bg = self.__colorVar.get()))

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
A()
