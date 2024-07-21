import tkinter as tk
import pandas as pd
import pyglet

# Colours and Fonts
black_pearl = '#1e272e'
good_night = '#485460'
dark_periwinkle = '#575fcf'
hint_of_elusive_blue ='#d2dae2'

pyglet.font.add_file('assets//EduAUVICWANTHand-VariableFont_wght.ttf')
font1, font2 = ('Edu AU VIC WA NT Hand', 24), ('Edu AU VIC WA NT Hand', 32)

# Text in th Info Frame
infoText = 'This is a Trivia Quiz Game. \n It is a multiple choice quiz with 10 questions \n about many different topics such as \n geography, animals, history and more. \n You can only use your mouse.'

# Global Variables
numOfFrames = 13
frame_counter = 0
total_points = 0

# Loading Question Data
questionDat = pd.read_excel('assets//question_data.xlsx')

# Functions
def createFrame():
	return tk.Frame(root,
			width=900,
			height=600,
			bg=black_pearl)

def createButton(frm, txt, cmnd):
	return tk.Button(frm, 
			 text=txt,
			 command=cmnd,
			 font=font1,
			 bg=black_pearl,
			 fg=dark_periwinkle,
			 activebackground=good_night,
			 activeforeground=black_pearl,
			 bd=0,
			 cursor='hand2',
			 padx=30)

def loadWidgets(i): # 0 <= i <= numOfFrames - 1
	if i == 0 or i == -1:
		for widget in widgetList[i]:
			widget.pack()
	else:
		for k in range(len(widgetList[i]) - 2):
			widgetList[i][k].pack()
		widgetList[i][-2].pack(side=tk.LEFT)
		widgetList[i][-1].pack(side=tk.RIGHT)
	

def loadFrame(i): # 0 <= i <= numOfFrames - 1
	global frame_counter 
	frame_counter = i
	frameList[i].tkraise()
	loadWidgets(i)

def loadQuestions(i): # 1 <= i <= 10
	question = str(questionDat.iat[i - 1, 0]) + ' - ' + questionDat.iat[i - 1, 1]
	return tk.Label(frameList[i], 
			text=question,
			font=font1,
		 	bg=black_pearl,
		 	fg=dark_periwinkle,
			pady=20)

def loadChoices(i): # 1 <= i <= 10
	return [tk.Radiobutton(frameList[i],
			       text=questionDat.iat[i - 1, j + 1],
			       variable=varList[i - 1],
			       value=j,
			       font=font1,
			       bg=black_pearl,
			       fg=dark_periwinkle,
			       activebackground=good_night,
			       activeforeground=black_pearl,
			       bd=0) for j in range(1, 5)]

def calcResult():
	global total_points
	for i in range(10):
		if varList[i].get() == questionDat.iat[i, 6]:
			total_points += 1

def finishQuiz():
	global total_points
	calcResult()
	results.config(text=f'You answered {total_points}/10 questions correctly!')
	loadFrame(numOfFrames - 2)
	for var in varList:
		var.set(0)
	total_points = 0

# Main Window
root = tk.Tk()
root.title('Trivia Game')
root.iconbitmap('assets//question_mark.ico')
root.resizable(False, False)

# Frames
frameList = [createFrame() for i in range(numOfFrames)]

# Variables for Radio buttons
varList = [tk.IntVar() for i in range(10)]

# Widgets
title = tk.Label(frameList[0], 
		 text='Trivia Game', 
		 font=font2,
		 bg=black_pearl,
		 fg=dark_periwinkle,
		 pady=45)
start = createButton(frameList[0], 'Start', lambda: loadFrame(1))
info1 = createButton(frameList[0], 'Info', lambda: loadFrame(-1))
quit1 = createButton(frameList[0], 'Quit', root.destroy)

invisible = tk.Label(frameList[1],  
		 text='', 
		 font=font2,
		 bg=black_pearl)

results = tk.Label(frameList[-2], 
		   text='',
		   font=font2,
		   bg=black_pearl,
		   fg=dark_periwinkle,
		   pady=120)
quit2 = createButton(frameList[-2], 'Quit', root.destroy)
backToMenu1 = createButton(frameList[-2], 'Main Menu', lambda: loadFrame(0))

info2 = tk.Label(frameList[-1], 
		 text=infoText, 
		 font=font1,
		 bg=black_pearl,
		 fg=hint_of_elusive_blue,
		 pady=20)
backToMenu2 = createButton(frameList[-1], 'Main Menu', lambda: loadFrame(0))

# Widget List, a 2d array that organizes the widgets of every frame
widgetList = [[title, start, info1, quit1]]
widgetList.append([loadQuestions(1),
		   *loadChoices(1),
		   invisible,
		   createButton(frameList[1], 'next', lambda: loadFrame(frame_counter + 1))])
for i in range(2, numOfFrames - 3):
	widgetList.append([loadQuestions(i),
			   *loadChoices(i),
			   createButton(frameList[i], 'previous', lambda: loadFrame(frame_counter - 1)),
			   createButton(frameList[i], 'next', lambda: loadFrame(frame_counter + 1))])
widgetList.append([loadQuestions(numOfFrames - 3),
 		   *loadChoices(numOfFrames - 3),
		   createButton(frameList[-3], 'previous', lambda: loadFrame(frame_counter - 1)),
		   createButton(frameList[-3], 'Finish Quiz', finishQuiz)])
widgetList.append([results, backToMenu1, quit2])
widgetList.append([info2, backToMenu2])

# Loading Quiz
for frame in frameList:
	frame.grid(row=0, column=0)
	frame.pack_propagate(False)
loadFrame(0)

root.mainloop()
