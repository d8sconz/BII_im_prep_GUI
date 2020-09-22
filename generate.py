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
cnt_lst = []
n = [0, 28, 57, 85, 113, 142, 170, 198, 227, 255]
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
    return img

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
            av_cat.itemset((y,x),av)
    normalizedImg = np.zeros((img_y, img_x))
    av_cat = cv.normalize(av_cat,  normalizedImg, 0, 255, cv.NORM_MINMAX)
    cv.imwrite('tmp_img.png', av_cat)
    nm = 'Normalised average cat'
    #show_img(nm)
    av_cat_f = save_img("av_cat/new_cat_av", av_cat)

    post_cat = np.zeros((img_x, img_y), np.uint8)
    for y in range(img_y):
        for x in range(img_x):
            pxl = av_cat.item(y, x)
            px_val = bisect.bisect(n, pxl)
            # Convert to 12 gray values
            post_cat.itemset((y, x), int(n[px_val-1]))
    cv.imwrite('tmp_img.png', post_cat)
    nm = 'Normalised average cat, posterised'
    #show_img(nm)
    post_cat_f = save_img("av_cat_post/new_cat_av_post", post_cat)
    return av_cat_f, post_cat_f

def max_rndm_img():      
    #Image composed of most common (random) pixel val
    MainIm = np.zeros((img_x, img_y), np.uint8)
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
    img = save_img("av_cat_max_rndm/new_cat_max", MainIm)
    return img

def pix_val(x,y,num):
    try:
        pixdata = Counter(cnt_list[x+img_x*y])
        pix = pixdata.most_common(9)
        p_val =  pix[num][0]
    except:
        p_val = 0
    return p_val

def img(i):      #Images composed of all pixel values
    global cnt_list
    with open('test_data.pkl', 'rb') as f:
        cnt_list = pickle.load(f)
    MainIm = np.zeros((img_x, img_y), np.uint8)
    for y in range(img_y):
        for x in range(img_x):
            MainIm.itemset((y,x),pix_val(x,y,i))
    cv.imwrite('tmp_img.png', MainIm)
    nm = f"img_{i}"
    #show_img(nm)
    im = save_img(f"{nm}/{nm}", MainIm)
    return im

def main():
    for i in range(9):
        img(i)
    av_img()
    max_rndm_img()
    
    os.remove('tmp_img.png')

if __name__ == '__main__':
    main()
    


