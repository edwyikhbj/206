import socket
from tkinter import *
from threading import Thread
from PIL import ImageTk, Image
import random
import platform

scrW = None
scrH = None
canvas1 = None
canvas2 = None
font = "Courier"

SERVER = None
IP_ADDRESS = None
PORT = None

playerName = None
nameEntry = None
nameWindow = None
gameWindow = None
gameOver = False

ticketGrid = []
currentNumList = []
displayedNumList = []
flashNumList = []
flashNumLabel = None

def gameWindow():
  global canvas2
  global gameWindow
  global scrW, scrH
  global flashNumLabel

  gameWindow = Tk()
  gameWindow.title("Tambola Fun")
  gameWindow.geometry('800x600')

  scrW = gameWindow.winfo_screenwidth()
  scrH = gameWindow.winfo_screenheight()

  bg = ImageTk.PhotoImage(file="./assets/background.png")

  canvas2 = Canvas(gameWindow, width=500, height=500)
  canvas2.pack(fill="both", expand=True)
  canvas2.create_image(0, 0, image=bg, anchor="nw")
  canvas2.create_text(400, scrH/12, text="Tambola Board", font=(font,50), fill="#3e2723")

  createTicket()
  placeNumbers()

  flashNumLabel = canvas2.create_text(400, scrH/2.1, text="Waiting for Players to join...", font=(font,30), fill="#3e2723")

  gameWindow.resizable(False, False)
  gameWindow.mainloop()

def askPlayerName():
  global canvas1
  global playerName, nameEntry, nameWindow
  global scrW, scrH

  nameWindow = Tk()
  nameWindow.title("Tambola Board Game")
  nameWindow.geometry("800x600")

  scrW = nameWindow.winfo_screenwidth()
  scrH = nameWindow.winfo_screenheight()

  bg = ImageTk.PhotoImage(file="./assets/background.png")
  canvas1 = Canvas(nameWindow, width=500, height=500)
  canvas1.pack(fill="both", expand=True)
  canvas1.create_image(0, 0, image=bg, anchor="nw")
  canvas1.create_text(400, scrH/8, text="Enter Name", font=(font,60), fill="#000")

  nameEntry = Entry(nameWindow, width=15, justify="center", font=(font,30), bd=5, bg="#FFF")
  nameEntry.place(relx=0.5, rely=0.4, anchor=CENTER)

  button = Button(nameWindow, text="Save", width=11, height=2, font=(font,30), bd=3, bg="#80deea", command=saveName)
  button.place(relx=0.5, rely=0.6, anchor=CENTER)

  nameWindow.resizable(False, False)
  nameWindow.mainloop()

def saveName():
  global SERVER
  global playerName, nameEntry, nameWindow

  playerName = nameEntry.get()
  nameEntry.delete(0,END)
  nameWindow.destroy()

  SERVER.send(playerName.encode())
  gameWindow()

def recievedMsg():
  global SERVER
  global displayedNumList, flashNumList, flashNumLabel
  global canvas2
  global gameOver

  numbers = [str(i) for i in range(1,91)]
  print(numbers)

  while True:
    chunk = SERVER.recv(2048).decode()
    if (chunk in numbers and flashNumList and not gameOver):
      flashNumList.append(int(chunk))
      canvas2.itemconfigure(flashNumLabel, text=chunk, font=(font,60))
    elif ("wins the game." in chunk):
      gameOver = True
      canvas2.itemconfigure(flashNumLabel, text=chunk, font=(font,40))

def createTicket():
  global gameWindow
  global ticketGrid

  mainLabel = Label(gameWindow, width=90, height=19, relief="ridge", bd=5, bg="#FFF")
  mainLabel.place(relx=0.5, rely=0.5, anchor=CENTER)

  xPos = 84
  yPos = 154
  for row in range(0, 3):
    rowList = []
    for col in range(0,9):
      if (platform.system() == "Darwin"):
        boxButton = Button(
          gameWindow, padx=-22, pady=23, 
          font=(font,18), bd=3, bg="#f9795d", 
          highlightbackground="#f9795d", 
          activebackground="#fa6241")
        boxButton.place(x=xPos, y=yPos)
      else:
        boxButton = Button(gameWindow, width=2, height=1, font=(font,35), bd=5, bg="#f9795d")
        boxButton.place(x=xPos, y=yPos)
      
      rowList.append(boxButton)
      xPos+= 632/9
    ticketGrid.append(rowList)
    xPos = 84
    yPos+= 292/3

def placeNumbers():
  global ticketGrid
  global currentNumList

  for row in range(0,3):
    ranColList = []
    counter = 0
    while counter<=4:
      ranCol = random.randint(0,8)
      if ranCol not in ranColList:
        ranColList.append(ranCol)
        counter+=1

    numContainer = {
      "0": [str(i) for i in range(1,11)],
      "1": [str(i) for i in range(11,21)],
      "2": [str(i) for i in range(21,31)],
      "3": [str(i) for i in range(31,41)],
      "4": [str(i) for i in range(41,51)],
      "5": [str(i) for i in range(51,61)],
      "6": [str(i) for i in range(61,71)],
      "7": [str(i) for i in range(71,81)],
      "8": [str(i) for i in range(81,91)]
    }
    counter = 0
    while counter < len(ranColList):
      colNum = ranColList[counter]
      numListByIndex = numContainer[str(colNum)]
      ranNum = random.choice(numListByIndex)
      
      if ranNum not in currentNumList:
        numBox = ticketGrid[row][colNum]
        numBox.configure(text=ranNum, fg="#000", bg="#fff0be", highlightbackground="#fff0be", activebackground="#f0d271")
        currentNumList.append(ranNum)
        counter+=1


def setup():
  global SERVER, IP_ADDRESS, PORT

  IP_ADDRESS = '127.0.0.1'
  PORT = 8000

  SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SERVER.connect((IP_ADDRESS, PORT))
  
  thread = Thread(target=recievedMsg)
  thread.start()

  askPlayerName()

setup()