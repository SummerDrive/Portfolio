import os
import dirImagesOrTags
import tkinter
import sys

def goToExit(event):
    sys.exit()

def openInitial():
    dir_path = dirImagesOrTags.dir_PathP

    name_list = os.listdir(dir_path)

    for e,name in enumerate(name_list):
        #print(str(e) + ' - ' + name)
        num = "{:03}.jpg".format(e + 1)
        print(num)
        os.rename(os.path.join(dir_path,name),os.path.join(dir_path,num))

    root2 = tkinter.Tk()
    root2.title('finished')
    root2.geometry("300x50+700+400") # 横幅 x 縦幅 + 横位置 + 縦位置
    root2.lift()

    button_go = tkinter.Button(root2, text='EXIT', width=0, height=0, font=("",15,"normal","bold"))
    button_go.bind("<ButtonPress>", goToExit)
    button_go.place(x=20,y=20)

    root2.mainloop()