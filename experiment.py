from psychopy import sound, visual, core, event, data, gui
import glob
import random, os
import pandas as pd
from triggers import setParallelData

#dialogue box
Dialoguebox = gui.Dlg(title = "Information")
Dialoguebox.addField("Name:")
Dialoguebox.addField("Gender:", choices=["Female", "Male", "Other"])
Dialoguebox.addField("Age:")
Dialoguebox.show()

#saving the data from the dialogue box
if Dialoguebox.OK:
    id = Dialoguebox.data[0]
    gender = Dialoguebox.data[1]
    age = Dialoguebox.data[2]
elif Dialoguebox.Cancel:
    core.quit()

# data
#making sure there is a data folder
timestamp = data.getDateStr()

if not os.path.exists("data"):
    os.makedirs("data")

cols = ["id", "gender", "age", "trial", "trigger", "audio_name", "t_after_stimulus", "time_1", "time_2"]

results = pd.DataFrame(
    columns = cols
    )
filename = "data/{}_{}.csv".format(id, timestamp)

win = visual.Window(
        size=[1920,1080],
        color="white",
        units="pix",
        screen=1,
        fullscr = True
    )

def check_quit():
    if event.getKeys(keyList=["escape"]):
            core.quit()
    
def fixation_cross():
    
    fixation = visual.TextStim(
        win, 
        text="+",
        color = 'black',
        height=100)
    
    fixation.draw()

msg = visual.TextBox2(
        win,
        pos = (0,0),
        font = 'Open Sans',
        color = 'black',
        text = '''
        Welcome to the experiment!

        You will soon be presented with a series of sounds.
        Please keep your eyes on the central cross.

        Press Q to begin

        '''
    )

final = visual.TextBox2(
        win,
        pos = (0,0),
        font = 'Open Sans',
        color = 'black',
        text = '''
        Thank you for your participation!

        Press Q to conclude the experiment

        '''
    )


#---The Experiment---
fileList = glob.glob('sounds/*')
#randomising the list
random.shuffle(fileList)

msg.draw()
win.flip()

while not event.getKeys(keyList=["q"]):
    pass
    if event.getKeys(['escape']):
        core.quit()

timer = core.Clock()
fixation_cross()
win.flip()

for file in fileList:
    if event.getKeys(['escape']):
        results.to_csv(filename,index=False)
        core.quit()
    condition = int(file[7:8])
    if condition==1: 
        trigger = 11
    if condition==2: 
        trigger = 21
    trial = fileList.index(file)+1
    audio_name = file
    stim = sound.Sound(file, volume = 0.5)
    duration = stim.getDuration()
    waiting_time = random.uniform(0.9, 1.1)
    fixation_cross()
    win.callOnFlip(setParallelData, trigger)
    win.flip()
    time_1 = timer.getTime()
    stim.play()
    time_2 = timer.getTime()
    if duration < 2:
        core.wait(duration + waiting_time)
    else:
        core.wait(2 + waiting_time)
        stim.pause()

    row = pd.Series({
        "id": id, 
        "gender": gender,
        "age": age,
        "trial": trial,
        "trigger": trigger,
        "audio_name": audio_name,
        "t_after_stimulus": waiting_time,
        "time_1": time_1,
        "time_2": time_2,
        })
    trialDf = pd.DataFrame(row,index=cols).T

    results = pd.concat([results,trialDf],
        ignore_index = True,
        axis=0
    )
    fixation_cross()
    win.callOnFlip(setParallelData, 0)
    win.flip()


results.to_csv(filename,index=False)


final.draw()
win.flip()
event.waitKeys(keyList = ['q', 'escape'])