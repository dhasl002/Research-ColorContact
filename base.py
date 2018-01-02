import chimera
from chimera.baseDialog import ModelessDialog
from chimera import help, openModels, Molecule
from chimera import viewer
import Tix, Pmw
import Tkinter
import CGLtk
import os
import chimera
import subprocess
from chimera import dialogs
from Tkinter import Tk
import Queue
import multiprocessing
import Midas
import sys


_buttonInfo = {}
_mp = None
oPath = ""

class ModelPanel(ModelessDialog):
	title="ColorContacts"
	buttons=('Run Tracer','Close')
	name="ColorContacts"
	#help="UsersGuide/modelpanel.html"
	
	def __init__(self):
		self.outputQueue = Queue.Queue()
		self.runEnabled = True
		self.threadClass = None

		openModels = chimera.openModels.list()

		self.txtCurrentPath = ""
		self.thresh = ""

		#get path argument default from mrc path
		self.txtPath = Tkinter.StringVar()
		self.thresholdValue = Tkinter.StringVar()
		
		self.txtPath.set(self.txtCurrentPath)
		self.thresholdValue.set(self.thresh)
		

		ModelessDialog.__init__(self)
		
	def fillInUI(self, parent):
		global _mp
		_mp = self
		self.parent = parent

		#not model panel
		from Tkinter import Entry, Label, Text, Frame, Button, Listbox, Checkbutton, Grid, Scrollbar
		
		self.label1 = Label(parent, text="ColorContacts", font="-weight bold -underline 1")
		self.label1.grid(row=0, column = 8, sticky='WS', pady=(12,2))
		self.label2 = Label(parent, text="Text File:")
		self.label2.grid(row=1, column = 7, sticky='E')
		self.txtEntry = Entry(parent, textvariable=self.txtPath)
		self.txtEntry.grid(row=1, column=8,sticky='EW')
		self.txtEntryButton = Button(parent,text="Browse", command=lambda: self.fileBrowse(self.txtPath, [("TXT","*txt")]))
		self.txtEntryButton.grid(row=1, column=10,sticky='W')
		self.label3 = Label(parent, text="            ")
		self.label3.grid(row=1, column = 11, sticky='E')
		self.label4 = Label(parent, text="     Confidence Threshold:")
		self.label4.grid(row=2, column = 7, sticky='E')
		self.skeletonFileEntrySSE = Entry(parent, textvariable=self.thresholdValue)
		self.skeletonFileEntrySSE.grid(row=2, column=8,sticky='EW')
		self.label5 = Label(parent, text="            ")
		self.repeating = Tkinter.IntVar()
		self.label6 = Label(parent, text="Do Not Repeat Colors:")
		self.label6.grid(row=3, column = 8, sticky='E')
		self.checkBox = Checkbutton(parent, variable=self.repeating).grid(row=3, column =9, sticky='WS', pady=(13,0))
	
	def RunTracer(self):

		if self.runEnabled:

			colors = ["tan", "sienna", "brown", "salmon", "red", "sandy brown", "orange red", "orange", "goldenrod", "gold", "yellow", "khaki", "dark khaki", "dark olive green", "olive drab", "chartreuse", "green", "dark green", "dark cyan", "light sea green", "aquamarine", "cyan", "deep sky blue", "steel blue", "sky blue", "blue", "medium blue", "navy blue", "medium purple", "purple", "plum", "orchid", "magenta", "dark magenta", "hot pink", "deep pink", "slate gray", "dark slate gray", "white"]
			#39 colors

			AAList = []
			path = str(self.txtPath.get())

			it = 0
			i = 0
			x = -100
			breakVar = 0
			noRepeat = int(self.repeating.get())
			
			for x in range(-50, 1000):
				Midas.color(colors[0], sel=':' + str(x))
	
			with open(path) as inf2:
				for line in inf2:
					AA1, AA2, trash1, trash2, trash3 = line.strip().split(",")
					next(inf2)
					if it == 38:
						it = 0
					if float(trash3) < float(self.thresholdValue.get()):
						break
					if noRepeat == 1:
						for i in range (0,len(AAList)):
							if AA1 == AAList[i] or AA2 == AAList[i]:
								breakVar = 1
						if breakVar == 1:
							break
					Midas.color(colors[it], sel=':' + str(AA1))
					Midas.color(colors[it], sel=':' + str(AA2))
					it = it + 1
					AAList.append(AA1)
					AAList.append(AA2)
				
	def fileBrowse(self, currentBox, browseTypes, copyBoxes = []):
		from tkFileDialog import askopenfilename

		window = Tk()
		window.withdraw() # we don't want a full GUI, so keep the root window from appearing
		window.lift()
		window.attributes("-topmost", True)
		fullpath = os.path.normpath(
			askopenfilename(parent = window, filetypes = browseTypes))
		
		if fullpath and fullpath != ".":
			currentBox.set(fullpath)
			self.copyToEmpty(currentBox, copyBoxes)
			
	def copyToEmpty(self, currentBox, copyBoxes):
		for copyBox in copyBoxes:
				if not copyBox[0].get():
					filename = os.path.splitext(currentBox.get())[0] #file path and name without extension
					copyBox[0].set(filename + copyBox[1])
			
from chimera import dialogs
dialogs.register(ModelPanel.name, ModelPanel)