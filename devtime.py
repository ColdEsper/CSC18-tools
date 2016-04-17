import tkinter as tk
import threading
from threading import Timer
import time
import json
import os

backupFile = "devtime_record_old.json"
mainFile = "devtime_record.json"
loadedData = []

updating = False
currentIndex = None
timeStart=None
timeEnd=None
buttons=[]
times=[]
timeLabels=[]
errorsInduced=[]
errorsFixed=[]
errorInducedLabels=[]
errorFixedLabels=[]
root = tk.Tk()

def updateTime ():
    global currentIndex
    global timeStart 
    global timeEnd 
    global times
    global timeLabels
    global buttons
    global updating
    updating = True
    if currentIndex != None:
        timeEnd = time.time()
        times[currentIndex]+=(timeEnd-timeStart)
        val = times[currentIndex]
        minutes = int(val/60.0)
        seconds = int(val)%60
        timeLabels[currentIndex].set(str(minutes)+"M "+str(seconds)+"S")
        if os.path.exists(mainFile):
            with open(mainFile,"r") as data:
                with open(backupFile,"w") as backup:
                    for line in data:
                        backup.write(line)
        with open(mainFile,"w") as data:
            jsonLabels = []
            for label in range(0,len(timeLabels)):
                jsonLabels.append([label,times[label]])
            data.write(json.dumps(jsonLabels))
        timeStart = timeEnd
        timeEnd=None
        updating = False
        return True
    else:
        updating = False
        return False
def updateThread ():
    global updating
    while updating:
        time.sleep(0.2)
    updateTime()
    thread = Timer(0.2,updateThread)
    thread.daemon = True
    thread.start()
def startTimer (timerIndex):
    global currentIndex
    global timeStart 
    global timeEnd 
    global times
    global buttons
    if not updateTime():
        timeStart = time.time()
    currentIndex = timerIndex
def endTimer ():
    global currentIndex
    global timeStart 
    global timeEnd 
    global times
    global buttons
    updateTime()
    timeStart=None
    currentIndex = None
def addError (index):
    global root
    global errorsInduced
    global errorInducedLabels
    errorsInduced[index]+=1
    errorInducedLabels[index].set(str(errorsInduced[index]))
def delError (index):
    global root
    global errorsFixed
    global errorFixedLabels
    errorsFixed[index]+=1
    errorFixedLabels[index].set(str(errorsFixed[index]))
def createTimer (name):
    global currentIndex
    global timeStart 
    global timeEnd 
    global times
    global timeLabels
    global errors
    global errorLabels
    global buttons
    global root
    i=createTimer.rows
    index=int(i/2)
    if len(loadedData) != 0:
        times.append(loadedData[index][1])
    else:
        times.append(0)
    timeLabels.append(tk.StringVar())
    if len(loadedData) != 0:
        minutes = int(loadedData[index][1]/60.0)
        seconds = str(int(loadedData[index][1]-(minutes*60)))
        minutes = str(minutes)
        timeLabels[-1].set(minutes+"M "+seconds+"S")
    else:
        timeLabels[-1].set("0M 0S")
    createTimer.rows+=2
    tk.Label(root,textvariable=timeLabels[-1]).grid(row=i,column=0)
    errorsInduced.append(0)
    errorInducedLabels.append(tk.StringVar())
    errorInducedLabels[-1].set("0")
    errorsFixed.append(0)
    errorFixedLabels.append(tk.StringVar())
    errorFixedLabels[-1].set("0")
    tk.Label(root,textvariable=errorInducedLabels[-1]).grid(row=i,column=1)
    tk.Label(root,textvariable=errorFixedLabels[-1]).grid(row=i,column=2)
    buttons.append(tk.Button(root, text=str(name),command= lambda : startTimer(index)))
    buttons[-1].grid(row=i+1,column=0)
    buttons.append(tk.Button(root, text=str(name+" error added"),command= lambda : addError(index)))
    buttons[-1].grid(row=i+1,column=1)
    buttons.append(tk.Button(root, text=str(name+" error fixed"),command= lambda : delError(index)))
    buttons[-1].grid(row=i+1,column=2)
createTimer.rows=0
def clearTime ():
    for time in range(0,len(times)):
        times[time] = 0
        timeLabels[time].set("0M 0S")

if os.path.exists(mainFile):
    with open(mainFile,"r") as data:
        loadedData=json.loads(data.read())
createTimer("plan")
createTimer("design")
createTimer("code")
createTimer("test")
createTimer("postmortem")
buttons.append(tk.Button(root, text="End timers",command=endTimer))
buttons[-1].grid(row=createTimer.rows,column=1)
buttons.append(tk.Button(root, text="Clear times",command=clearTime))
buttons[-1].grid(row=createTimer.rows,column=2)
thread = Timer(1.0,updateThread)
thread.daemon = True
thread.start()
root.mainloop()
