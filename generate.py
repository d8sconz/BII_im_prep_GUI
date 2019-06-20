import cv2 as cv 
import numpy as np
import random
from collections import Counter, OrderedDict
import pickle
import os
from datetime import datetime as dt
import bisect
from pathlib import Path

Cats = os.getcwd() + '/Cats'
new_cats = Cats + '/new_cats'

f = open('test_data.pkl', 'rb')
cnt_list = pickle.load(f)
f.close()

n = [0, 32, 64, 96, 128, 160, 192, 224, 255]
img_x, img_y = 64,64            # divisible x 3
#MainIm = np.zeros((img_x, img_y), np.uint8)

def show_img(nm):
    image = cv.imread('tmp_img.png', 0)
    cv.namedWindow(nm, cv.WINDOW_NORMAL)
    cv.moveWindow(nm, 1600,150)
    cv.imshow(nm, image)
    cv.waitKey(1000)
    cv.destroyAllWindows()

def save_img(nm, im):
    #im = cv.imread('tmp_img.png')
    p = Path(os.path.join(new_cats,nm))
    if not os.path.exists(p.parent):
        os.mkdir(p.parent)
    img = f"{p} {dt.now():%d-%m-%Y %H:%M}.png"
    cv.imwrite(img, im)
    return

def pix_val(x,y,num):
    pixdata = Counter(cnt_list[x+img_x*y])
    pix = pixdata.most_common(9)
    return pix[num][0]

def av_img():
    av_cat = np.zeros((img_x, img_y), np.uint8)
    for y in range(img_y):
        for x in range(img_x):
            pixdata = dict(Counter(cnt_list[x+img_x*y]))
            tot, num = 0, 0
            for key in pixdata.keys():
                tot += (key*pixdata[key])
                num += pixdata[key]
            av = tot/num
            MainIm.itemset((y,x),av)
    normalizedImg = np.zeros((img_y, img_x))
    MainIm = cv.normalize(MainIm,  normalizedImg, 0, 255, cv.NORM_MINMAX)
    cv.imwrite('tmp_img.png', MainIm)
    nm = 'Normalised average cat'
    #show_img(nm)
    save_img(f"av_cat/new_cat_av", av_cat)

    post_cat = np.zeros((img_x, img_y), np.uint8)
    for y in range(img_y):
        for x in range(img_x):
            pxl = MainIm.item(y, x)
            px_val = bisect.bisect(n, pxl)
            # Convert to 12 gray values
            MainIm.itemset((y, x), int(n[px_val-1]))
    cv.imwrite('tmp_img.png', MainIm)
    nm = 'Normalised average cat, posterised'
    #show_img(nm)
    save_img(f"av_cat_post/new_cat_av_post", post_cat)
    return av_cat, post_cat

def max_rndm_img():      #Image composed of most common (random) pixel val
    pix = []
    for y in range(img_y):
        for x in range(img_x):
            pix_vals = []
            pixdata = dict(Counter(cnt_list[x+img_x*y]))
            tot, num = 0, 0
            for key, value in pixdata.items():
                for _ in range(value):
                    pix_vals.append(key)
            rndm = random.choice(pix_vals)
            MainIm.itemset((y, x), rndm)
    cv.imwrite('tmp_img.png', MainIm)
    nm = 'Weighted random max cat'
    #show_img(nm)
    img = os.path.join(
        new_cats, f"av_cat_max_rndm/new_cat_max {dt.now():%d-%m-%Y %H:%M}.png")
    cv.imwrite(img, MainIm)
    return MainIm

def img(i):      #Images composed of all pixel values
    for y in range(img_y):
        for x in range(img_x):
            MainIm.itemset((y,x),pix_val(x,y,i))
    cv.imwrite('tmp_img.png', MainIm)
    nm = f"img_{i}"
    #show_img(nm)
    im = save_img(f"{nm}/{nm}", MainIm)
    return MainIm

def main():
    for i in range(9):
        img(i)
    av_img()
    max_rndm_img()
    
    os.remove('tmp_img.png')

if __name__ == '__main__':
    main()
    


