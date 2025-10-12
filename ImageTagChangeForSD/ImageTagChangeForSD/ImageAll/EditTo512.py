import cv2
import os

dir_name = 'D:/xxx/picture/TrainingDataforSD/forEditTo512/'
'''
name_list = os.listdir(dir_name)

for e,name in enumerate(name_list):
    pic_dir = dir_name + name

    img = cv2.imread(pic_dir) #imreadモジュールでtest.pngを読み込む
    w =img.shape[1]
    h =img.shape[0]
    center = int(w / 2)
    img_res = img[0:512, center - 256:center + 256] #画像の一部を切り抜き
 
    cv2.imwrite(dir_name + name, img_res) #リサイズした画像を保存
'''