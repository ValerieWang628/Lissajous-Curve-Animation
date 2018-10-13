
from tkinter import *
import math

def init(data):
    data.outerMargin = 10
    data.innerMargin = 15
    data.cols = 7
    data.row = data.cols
    data.circNum = data.cols - 1
    data.gridZoom = 1.02
    data.gridSize = (data.width-2*data.outerMargin)//(data.cols * data.gridZoom)
    data.circleCtrHori = []
    data.circleCtrVerti = []
    data.lilCircHori = []
    data.lilCircVerti = []
    data.jct = []
    data.radius = 0
    data.lilR = 3
    data.jctR = 1.5
    data.thetaIncre = 0
    data.timerDelay = 1
    circleCenter(data)
    data.theta = [ 0 for c in range(data.circNum)]


def mousePressed(event, data):
    pass

def keyPressed(event, data):
    pass

def drawCircle(canvas, data):
    color = ["red", "orange", "yellow", "green", "cyan", "blue"]
    for i in range(1, data.cols):
        x0 = data.outerMargin + data.gridSize * i + data.innerMargin
        y0 = data.outerMargin + data.innerMargin
        x1 = x0 + data.gridSize - data.innerMargin
        y1 = y0 + data.gridSize - data.innerMargin
        canvas.create_oval(x0, y0, x1, y1, fill = "black", outline = color[i-1], width = 1.5)
        canvas.create_oval(y0, x0, y1, x1, fill = "black", outline = color[i-1], width = 1.5)

def drawText(canvas, data):
    color = ["red", "orange", "yellow", "green", "cyan", "blue"]
    for i in range(1, data.cols):
        x0 = data.outerMargin + data.gridSize * i + data.innerMargin
        y0 = data.outerMargin + data.innerMargin
        x1 = x0 + data.radius
        y1 = y0 + data.radius
        canvas.create_text(x1, y1, text = str(i) + "x", font = "Helvetica 15", fill = color[i-1])
        canvas.create_text(y1, x1, text = str(i) + "x", font = "Helvetica 15", fill = color[i-1])

def circleCenter(data):
    for i in range(1, data.cols):
        x0 = data.outerMargin + data.gridSize * i + data.innerMargin
        y0 = data.outerMargin + data.innerMargin
        x1 = x0 + data.gridSize - data.innerMargin
        y1 = y0 + data.gridSize - data.innerMargin
        data.radius = (x1 - x0)//2
        data.circleCtrHori.append((x0 + data.radius, y0 + data.radius))
        data.circleCtrVerti.append((y0 + data.radius, x0 + data.radius))

def lilCirc(data, circCtrList, lilCircList):
    lilCircList = []
    for i in range(len(circCtrList)):
        circ = circCtrList[i]
        theta = data.theta[i]
        x0, y0 = circ
        x1 = x0 + data.radius * math.sin(theta)
        y1 = y0 + data.radius * math.cos(theta)
        lilCircList.append((x1, y1))
    return lilCircList

def theta(data):
    for i in range(data.circNum):
        data.theta[i] += data.thetaIncre * (i + 1)

def drawPoint(canvas, data, circCtrList, lilCircList):
    pointList = lilCirc(data, circCtrList, lilCircList)
    for tup in pointList:
        x, y = tup[0], tup[1]
        x0 = x - data.lilR
        y0 = y - data.lilR
        x1 = x + data.lilR
        y1 = y + data.lilR
        canvas.create_oval(x0, y0, x1, y1, fill = "white")
        
def drawLine(canvas, data, circCtrList, lilCircList, hori = True):
    color = ["red", "orange", "yellow", "green", "cyan", "blue"]
    pointList = lilCirc(data, circCtrList, lilCircList)
    for i in range(len(pointList)):
        tup = pointList[i]
        x0, y0 = tup[0], tup[1]
        if hori: 
            x1, y1 = x0, data.outerMargin
            x2, y2 = x0, data.height - data.outerMargin
        else: 
            x1, y1 = data.outerMargin, y0
            x2, y2 = data.width - data.outerMargin, y0
        canvas.create_line(x0, y0, x2, y2, fill = color[i], width = 1)
     

def LineJct(data):
    pointListHori = lilCirc(data, data.circleCtrHori, data.lilCircHori)
    pointListVerti = lilCirc(data, data.circleCtrVerti, data.lilCircVerti)
    for i in range(len(pointListHori)):
        for j in range(len(pointListVerti)):
            tupHori = pointListHori[i]
            tupVerti = pointListVerti[j]
            x, y = tupHori[0], tupVerti[1]
            x0 = x - data.jctR
            y0 = y - data.jctR
            x1 = x + data.jctR
            y1 = y + data.jctR
            data.jct.append((x0, y0, x1, y1))
            
def drawLineJct(canvas, data):
    LineJct(data)
    for point in data.jct:
        canvas.create_oval(point, fill = "white")

def drawBg(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "white")
    x0 = data.outerMargin
    y0 = data.outerMargin
    x1 = data.width - data.outerMargin
    y1 = data.height - data.outerMargin
    canvas.create_rectangle(x0, y0, x1, y1, fill = "black")

def timerFired(data):
    data.thetaIncre += 0.001
    theta(data)

def redrawAll(canvas, data):
    drawBg(canvas, data)
    drawCircle(canvas, data)
    drawText(canvas, data)
    drawPoint(canvas, data, data.circleCtrHori, data.lilCircHori)
    drawPoint(canvas, data, data.circleCtrVerti, data.lilCircVerti)
    drawLine(canvas, data, data.circleCtrHori, data.lilCircHori)
    drawLine(canvas, data, data.circleCtrVerti, data.lilCircVerti, hori = False)
    drawLineJct(canvas, data)
    

def run(width=300, height=300):
    # this starter code is from CMU-15112 course website
    # initially written by David Kosbie
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(700, 700)