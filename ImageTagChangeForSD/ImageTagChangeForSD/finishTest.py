import tkinter
import sys
import winsound

def goToExit(event):
    f = open('finish.wav', 'rb')
    data = f.read()
    f.close()

    winsound.PlaySound(data, winsound.SND_MEMORY)

    sys.exit()

root2 = tkinter.Tk()
root2.title('finished')
root2.geometry("200x50+700+400") # 横幅 x 縦幅 + 横位置 + 縦位置
root2.lift()

button_go = tkinter.Button(root2, text='EXIT', width=0, height=0, font=("",15,"normal","bold"))
button_go.bind("<ButtonPress>", goToExit)
button_go.place(x=70,y=0)

root2.mainloop()

'''
def toFinish():
    finishPath = 'E:/DATA/ImageTagChangeForSD/ImageTagChangeForSD'
    sys.path.append(finishPath)
    import finishTest
    finishTest
'''