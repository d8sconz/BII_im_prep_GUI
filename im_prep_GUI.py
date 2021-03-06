#!/usr/bin/env python3.7

#import asyncio
import bisect
import itertools
import os
# Pickle for saving/retrieving data file
import pickle
import sys
import time
from datetime import datetime as dt
import urllib.request
#from asyncio.events import get_event_loop
# Counter for pixel value k:v countable dict where,
# k = pixel value, and v = number of occurences
from collections import Counter
#from idlelib import query
import random
import cv2 as cv
import matplotlib as mpl
# Matplotlib chosen for image render because it works.
# Need to return to this and try wxStaticBitmap again with wx.GetApp().Yield()
import matplotlib.pyplot as plt
import numpy as np
import praw
import wx
import wx.lib.agw.aui as aui
import wx.lib.agw.floatspin as floatspin
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wxagg import \
#    NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
#from wxasync import AsyncBind, StartCoroutine, WxAsyncApp

#Need to make sure data pickle file exists before importing generate
try:
    f = open('test_data.pkl', 'rb')
    f.close()
except:
    print("No data file, creating new")
    data = []
    f = open('test_data.pkl', 'wb')
    pickle.dump(data, f)
    f.close()

import generate

# random change

# ------------------file variables-------------------
# Base path
pth = os.path.dirname(os.path.abspath('__file__'))
# folder for gui graphics
gui_graphics = pth + '/gui_graphics'
# temp file for initial image handling
img_pth = os.path.join(pth, "tmp_img.png")
# Folders, subfolders for processed images
if not os.path.exists(pth + '/Cats'):
    os.makedirs(pth + '/Cats')
all_cats = pth + '/Cats'
# temp file for initial image handling
if not os.path.exists(all_cats + '/temp'):
    os.makedirs(all_cats + '/temp')
tmp_img_pth = all_cats + '/temp'
if not os.path.exists(all_cats + '/raw_cats'):
    os.makedirs(all_cats + '/raw_cats')
raw_cats = all_cats + '/raw_cats'
if not os.path.exists(all_cats + '/dead_cats'):
    os.makedirs(all_cats + '/dead_cats')
dead_cats = all_cats + '/dead_cats'
if not os.path.exists(all_cats + '/new_cats'):
    os.makedirs(all_cats + '/new_cats')
new_cats = all_cats + '/new_cats'
# Classifier files for face recognition
cascades1 = all_cats + '/cascades/haarcascade_frontalcatface.xml'
cascades2 = all_cats + '/cascades/haarcascade_frontalcatface_extended.xml'
cascades3 = all_cats + '/cascades/haarcascade_eye.xml'
# Classifiers for face recognition
cat_face1 = cv.CascadeClassifier(cascades1)
cat_face2 = cv.CascadeClassifier(cascades2)
cat_face3 = cv.CascadeClassifier(cascades3)
# Processed image dimensionshref = submission.url
min_img_wndw = 295      # min href = submission.urlsize of top panels
img_y, img_x = 64, 64   # raw href = submission.urlcat size
dim = (img_y, img_x)
im_resize_init = 1280   # Init href = submission.urlial resize dimension of downloaded images

#href = submission.url
#Ghost of programs past - for href = submission.urluse with wx.staticBitmap if I return to it
MainIm = np.zeros((img_x, img_y), np.uint8)
n = [0, 28, 57, 85, 113, 142, 170, 198, 227, 255]

#======================================================================
#---------------------Front page of notebook---------------------------
class Front_page(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)

        image_panel = Download_image(vSplitter)
        terminal_panel = Terminal(vSplitter)
        #terminal_panel.SetBackgroundColour(wx.BLACK)
        vSplitter.SplitVertically(image_panel, terminal_panel)
        vSplitter.SetSashGravity(0.5)

        panelThree = Control_panel(topSplitter, image_panel, terminal_panel)
        topSplitter.SplitHorizontally(vSplitter, panelThree)
        topSplitter.SetSashGravity(0.5)

        topSplitter.SetMinimumPaneSize(min_img_wndw)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

# ---------------class for panel containing image on front page--------
class Download_image(wx.Panel):
    def __init__(self, parent):
        super(Download_image, self).__init__(parent)
        img = wx.Image(min_img_wndw, min_img_wndw)
        self.image_ctrl = wx.StaticBitmap(self, bitmap=wx.Bitmap(img))
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.image_ctrl, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sizer)

        #load opening image
        if not os.path.exists(new_cats + '/img_0'):
            os.makedirs(new_cats + '/img_0')
        im_pth = new_cats + '/img_0'
        files = os.listdir(im_pth)
        im_pths = [os.path.join(im_pth, im_name) for im_name in files]
        try:
            img = max(im_pths, key=os.path.getctime)
            #opening_image = cv.imread(img)
            opening_image = img
        except:
            opening_image = os.path.join(pth + "/gui_graphics/Abe.png")
       
        self.draw(opening_image)

    def draw(self, img_pth):
        display_im  = wx.Image(img_pth, wx.BITMAP_TYPE_ANY)
        display_im = display_im.Scale(min_img_wndw, min_img_wndw)
        self.image_ctrl.SetBitmap(wx.Bitmap(display_im))
        self.Refresh()

#--------class for panel containing terminal output on front page------
class Terminal(wx.Panel):
    def __init__(self, parent):
        super(Terminal, self).__init__(parent)
        self.term = wx.TextCtrl(self,
                                size=(200, 100),
                                style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH
                                )
        self.term.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.term.SetBackgroundColour(wx.BLACK)     
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.term, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.term.Update()

#------------------Panel for all controls on front page----------------
class Control_panel(wx.Panel):
    def __init__(self, parent, image_panel, terminal_panel):
        wx.Panel.__init__(self, parent=parent)
        # Panels
        self.panel = wx.Panel(self, -1, size=(580, 180))
        self.cat_panel = image_panel
        self.term_panel = terminal_panel
        self.btn_go_toggle = 1
        self.image_store = []        # holds last image_num images for review
        self.image_num = 10          # number of images to hold for review
        self.inc = 0                 # holds index number of image_store for back/fwd buttons
        self.current_pic = 0         # holds index number of current review pic for "Go" button
        self.auto = 0
        self.review = 0
        self.good_cat = 0
        self.haar_scale = 1.08
        self.haar_neig = 5

        # Buttons, sliders and gauge, setup and initialise
        self.btn_back = wx.Button(self.panel, id=-1, pos=(390, 30), size=(45, 35))
        self.btn_back.name = "back"
        self.btn_back.SetBitmap(wx.Bitmap(gui_graphics + '/back.png'))
        self.btn_back.Bind(wx.EVT_BUTTON, self.btn_review)
        self.btn_back.ToolTip = wx.ToolTip(f"Move back through {self.image_num} most recent cats")

        self.btn_go = wx.Button(self.panel, id=-1, pos=(455, 30), size=(45, 35))
        self.btn_go.SetBitmap(wx.Bitmap(gui_graphics + '/start.png'))
        self.btn_go.Bind(wx.EVT_BUTTON, self.btn_go_press)
        self.btn_go.ToolTip = wx.ToolTip("Start the spider or data dump")

        self.btn_fwd = wx.Button(self.panel, id=-1, pos=(520, 30), size=(45, 35))
        self.btn_fwd.name = "fwd"
        self.btn_fwd.SetBitmap(wx.Bitmap(gui_graphics + '/fwd.png'))
        self.btn_fwd.Bind(wx.EVT_BUTTON, self.btn_review)
        self.btn_fwd.ToolTip = wx.ToolTip(f"Move forward through {self.image_num} most recent cats")

        self.btn_clear_btdt = wx.Button(self.panel, id=-1, pos=(390, 75), size=(45, 35))
        self.btn_clear_btdt.SetBitmap(wx.Bitmap(gui_graphics + '/clear.png'))
        self.btn_clear_btdt.Bind(wx.EVT_BUTTON, self.btn_clr_btdt)
        self.btn_clear_btdt.ToolTip = wx.ToolTip("Clears the btdt list")

        self.btn_reject = wx.Button(self.panel, id=-1, pos=(455, 75), size=(45, 35))
        self.btn_reject.SetBitmap(wx.Bitmap(gui_graphics + '/dislike.png'))
        self.btn_reject.Bind(wx.EVT_BUTTON, self.btn_reject_press)
        self.btn_reject.ToolTip = wx.ToolTip("Crap cat! Go to next")

        self.btn_accept = wx.Button(self.panel, id=-1, pos=(520, 75), size=(45, 35))
        self.btn_accept.SetBitmap(wx.Bitmap(gui_graphics + '/like.png'))
        self.btn_accept.Bind(wx.EVT_BUTTON, self.btn_accept_press)
        self.btn_accept.ToolTip = wx.ToolTip("Good cat! start finding faces")

        self.btn_auto = wx.ToggleButton(self.panel, id=-1, pos=(390, 120), size=(45, 35))
        self.btn_auto.SetBitmap(wx.Bitmap(gui_graphics + '/repeat.png'))
        self.btn_auto.Bind(wx.EVT_TOGGLEBUTTON, self.btn_auto_go)
        self.btn_auto.ToolTip = wx.ToolTip("Toggles between manual and full auto operation WARNING! full auto will lock the gui until it finds a cat to skin. You can only access the toggle button as the dead cat spins.")

        self.spn_scale = floatspin.FloatSpin(
                                            self.panel,
                                            id=-1,
                                            pos=(450, 120),
                                            size=(55,25),
                                            value=1.08,
                                            min_val=1.01,
                                            max_val=1.4,
                                            increment=.01,
                                            digits=2,
                                            agwStyle=floatspin.FS_LEFT
                                            )
        self.spn_scale.Bind(wx.EVT_SPINCTRL, self.spn_scale_OnSpin)
        self.spn_scale.Bind(wx.EVT_TEXT, self.spn_scale_OnSpin)
        self.spn_scale.ToolTip = wx.ToolTip("Scale factor for Haar (default 1.08). Min-1.01; Max-1.4. Smaller number finds more faces but is slower")

        self.spn_neig = wx.SpinCtrl(
                                    self.panel,
                                    id=-1,
                                    pos=(520, 120),
                                    size=(45, 25),
                                    value='5',
                                    min=1,
                                    max=20
                                    )       #size=(55, 35),
        self.spn_neig.Bind(wx.EVT_SPINCTRL, self.spn_neig_OnSpin)
        self.spn_neig.Bind(wx.EVT_TEXT, self.spn_neig_OnSpin)
        self.spn_neig.ToolTip = wx.ToolTip("Neighbour factor for Haar (default 5). More is more accurate but slower")

        self.cat_sld = wx.Slider(
            self.panel,
            value=1,
            minValue=1,
            maxValue=200,
            pos=(15, 20),
            size=(320, -1),
            style=wx.SL_HORIZONTAL|wx.SL_LABELS
            )

        self.progress = wx.Gauge(
            self.panel,
            -1,
            100,
            pos=(20, 120),
            size=(315, -1),
            style=wx.GA_HORIZONTAL|wx.GA_SMOOTH
            )

        self.progress.SetValue(0)
        self.progress.SetRange(self.cat_sld.GetValue())
        self.progress.SetForegroundColour(wx.Colour(255, 255, 255))

        self.r = praw.Reddit('bot1')    # Initialises reddit bot to download cat images
        self.btdt = self.get_btdt()     # setting up and loading list of downloaded/rejected images

        self.term_msg(f"You have {self.Cat_count()} raw cats")
        self.term_msg(f"btdt currently has {len(self.btdt)} entries\n")

    # button functions
    def btn_go_press(self, event=None):
        self.reject_cat = 0
        #self.good_cat = 0
        #self.auto = 0
        if event:
            if self.btn_go_toggle:
                self.btn_go_toggle = 0
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/pause.png'))
                self.btn_go.Update()
                self.run = 1
            else:
                self.btn_go_toggle = 1
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/start.png'))
                self.term_msg("Paused for manual...\nClick 'Go' for Auto")
                self.run = 0
                self.btn_go.Update()
        else:
            self.run = 0
            self.btn_go_toggle = 1
            self.btn_go.SetBitmap(wx.Bitmap(gui_graphics + '/start.png'))
            self.btn_go.Update()

        if self.review:
            self.review = 0
            image = self.image_store[self.current_pic]
            # Store state of auto/manual toggle, enforce 'Auto',
            # search for cat face, reset toggle on return
            auto = self.auto
            self.auto = 1
            self.find_cats(image)
            self.auto = auto

        while self.run:
            self.get_cats()

    def btn_reject_press(self, event):
        self.good_cat = 0
        self.reject_cat = 1

    def btn_accept_press(self, event):
        self.reject_cat = 0
        self.good_cat = 1

    def btn_clr_btdt(self, event):
        self.btdt = []
        self.term_msg("btdt:")
        self.term_msg(f"{self.btdt}\n")

    def btn_review(self, event):
        pic_num = len(self.image_store)
        self.review = 1
        self.good_cat = 1
        name = event.GetEventObject().name
        if pic_num == 0:
            self.term_msg("No cats")
            return
        if name == "back":
            if self.inc >= pic_num:
                self.inc = 0
            self.cat_panel.draw(self.image_store[self.inc])
            self.current_pic = self.inc
            self.inc += 1
        else:
            if self.inc < 0:
                self.inc = pic_num - 1
            self.cat_panel.draw(self.image_store[self.inc])
            self.current_pic = self.inc
            self.inc -= 1

    def btn_auto_go(self, event=None):
        if event:
            state = event.GetEventObject().GetValue()
            if state == True:
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/manual.png'))
                self.term_msg("Automatic operation initiated")
                self.btn_auto.Update()
                self.auto = 1
            else:
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/repeat.png'))
                self.term_msg("Manual operation initiated")
                self.auto = 0
                self.btn_auto.Update()
        else:
            self.auto = 0
            self.btn_auto.SetValue(False)
            self.btn_go.SetBitmap(wx.Bitmap(gui_graphics + '/repeat.png'))

    def spn_scale_OnSpin(self, event):
        self.haar_scale = self.spn_scale.GetValue()

    def spn_neig_OnSpin(self, event):
        self.haar_neig = self.spn_neig.GetValue()

    def get_btdt(self):
        try:
            with open('btdt.pkl', 'rb') as f:
                btdt = pickle.load(f)
            return btdt
        except:
            self.term_msg("No btdt file, creating new")
            # Collect btdt from any existing files to prevent re-download
            files = os.listdir(raw_cats)
            if files:
                for f in files:
                    btdt.append(f[:6])
                btdt = list(dict.fromkeys(btdt))
            else:
                btdt = []
            with open('btdt.pkl', 'wb') as f:
                pickle.dump(btdt, f)
            return btdt

    def show_im(self, image):
        self.cat_panel.draw(image)
        self.cat_panel.Update()
        if self.auto == 1:
            pass
        else:
            time.sleep(.02)
        return

    def term_msg(self, msg=None):
        if not msg:
            pass
        else:
            self.term_panel.term.WriteText(msg+"\n")
            self.term_panel.term.Update()
        return

    def get_cats(self):
        pic = self.Cat_count()
        num = self.cat_sld.GetValue()
        if pic < num:
            self.term_msg("Launching spider...")
            self.progress.SetRange(num)
            while pic < num:
                num = self.cat_sld.GetValue()
                self.spider()
                pic = self.Cat_count()
                if pic > num: pic = num
                self.progress.SetValue(pic)
                self.progress.Update()
                if not self.run:
                    return
            self.term_msg("=========================")
            self.term_msg("Check for noses and click Play, or press Enter...")
            self.btn_go_press()
        else:
            self.progress.SetRange(pic)
            Cat_list = [f for f in os.listdir(
                raw_cats) if os.path.isfile(os.path.join(raw_cats, f))]
            for i in range(pic):
                self.term_msg(f"Scanning {Cat_list[i]}, {pic-i} to go")
                s_cat = os.path.join(raw_cats, Cat_list[i])
                d_cat = os.path.join(dead_cats, Cat_list[i])
                #image = cv.imread(s_cat,0)
                self.show_im(s_cat)
                self.dataBlocks(s_cat)
                os.rename(s_cat, d_cat)
                self.progress.SetValue(pic - i)
                self.progress.Update()
                time.sleep(.01)
            
            self.progress.SetValue(0)
            self.progress.Update()
            self.term_msg("Generating new cats\n")
            time.sleep(1)
            for i in range(9):
                image = generate.img(i)
                self.show_im(image)
                self.term_msg(f"Generating {i} pixel cat\n")
                time.sleep(1)
            av_im, post_im = generate.av_img()
            #image = cv.imread(av_im, 0)
            self.show_im(av_im)
            self.term_msg("Generating average cat\n")
            time.sleep(1)
            #image = cv.imread(post_im, 0)
            self.show_im(post_im)
            self.term_msg("Generating posterised average cat\n")
            time.sleep(1)
            image = generate.max_rndm_img()
            self.show_im(image)
            self.term_msg("Generating weighted random cat\n")
            os.remove('tmp_img.png')
            tmp_cats =[f for f in os.listdir(
                tmp_img_pth) if os.path.isfile(os.path.join(tmp_img_pth, f))]
            for f in tmp_cats:
                os.remove(os.path.join(tmp_img_pth, f))

            time.sleep(3)
            self.show_im(av_im)
            self.btn_go_press()

    def spider(self):
        for submission in self.r.subreddit('cats').new(limit=None):
            if not self.run:
                break
            href = submission.url
            user = submission.id
            if (href.endswith(".png") or href.endswith(".jpg")) and user not in self.btdt:
                # Add user to list to prevent duplicates and save
                self.btdt.append(user)
                with open('btdt.pkl', 'wb') as f:
                    pickle.dump(self.btdt, f)
                self.term_msg(f"btdt currently has {len(self.btdt)} entries")
                # Download image
                self.term_msg("Downloading")
                with urllib.request.urlopen(href) as im:
                    image = np.asarray(bytearray(im.read()), dtype="uint8")
                    image = cv.imdecode(image, cv.IMREAD_COLOR) #IMREAD_COLOR
                    #Save a tmp image for initial manipulation
                    cv.imwrite(img_pth, image)
                    # Put images into cache for review if called
                    cache_img = os.path.join(tmp_img_pth, f"cache {dt.now():%d-%m-%Y %H:%M:%S}.png")
                    cv.imwrite(cache_img, image)
                    if len(self.image_store) < self.image_num:
                        self.image_store.insert(0, cache_img)
                    else:
                        self.image_store.insert(0, cache_img)
                        # Remove excess image from cache
                        os.remove(self.image_store[-1])
                        self.image_store.pop()

                self.find_cats(img_pth)
                pic = self.Cat_count()
                self.term_msg(f"Currently {pic} raw_cats in captivity\n")
                if pic > 0:
                    break
        # Remove temp file

        return

    ##################    Image processing functions:   ########################
    ################## takes raw images from spider and ######################## 
    ##################      finds,  resizes, crops,     ########################
    ##################      posterises and saves        ########################

    def find_cats(self, img_pth):     #Takes name of temp file from spider
        # Open and view raw downloaded image
        # image = cv.cvtColor(image, cv.COLOR_BGR2RGB)    #COLOR_RGB2BGR
        im = cv.imread(img_pth)

        # Make image square with padding and resize
        old_size = im.shape[:2] # old_size is in (height, width) format

        ratio = float(im_resize_init)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        im = cv.resize(im, (new_size[1], new_size[0]))

        delta_w = im_resize_init - new_size[1]
        delta_h = im_resize_init - new_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)

        color = [0, 0, 0]
        im = cv.copyMakeBorder(im, top, bottom, left, right, cv.BORDER_CONSTANT, value=color)
        rows, cols, _ = im.shape
        cv.imwrite(img_pth, im)

        self.show_im(img_pth)
        if self.auto == 1:
            pass
        else:
            for _ in range(50000):
                if self.run:
                    wx.GetApp().Yield()
                    if self.reject_cat:
                        self.reject_cat = 0 # reset switch for next cat
                        self.term_msg("Crap cat!")
                        return
                    if self.good_cat:
                        self.term_msg("There be cats!")
                        break
                else:
                    return
        # Standardise color, convert to grayscale and normalise...
        # the range 0 - 255 and view each step
        #im = cv.imread(img_pth)
        im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
        norm_img = np.zeros((rows, cols))
        im = cv.normalize(im, norm_img, 0, 255, cv.NORM_MINMAX)
        cv.imwrite(img_pth, im)
        faces = cat_face2.detectMultiScale(im, 1.04, 3, minSize=(128,128))
        detect = len(faces) #+ len(eyes)
        if detect or self.good_cat:
            self.show_im(img_pth)
            self.good_cat = 0   #reset switch for next cat1
            self.term_panel.term.WriteText("Looking for cats...\n")
            # Rotate image and finer check for cat faces1
            inc = 72    #sets increment for rotation of image1. eg. 72=5°
            for i in range(0, 360, int(360/inc)):  # rotate a1t 5 degree increments
                # Routine to rotate and display image in search of cats
                M = cv.getRotationMatrix2D((cols/2, rows/2), i, 1)
                rot_im = cv.warpAffine(im, M, (cols, rows))
                cv.imwrite(img_pth, rot_im)
                self.show_im(img_pth)
                # Check rotated image for cats and crop/save any found
                faces = cat_face2.detectMultiScale(
                    rot_im,
                    self.haar_scale,
                    self.haar_neig,
                    minSize=(128,128)
                    )
                wx.GetApp().Yield()
                if self.reject_cat:
                    self.reject_cat = 0 # reset switch for next cat
                    break
                if not self.run:
                    break
                if len(faces):
                    self.term_panel.term.WriteText("Cats ahoy!\nCutting cats!\n")
                    for (x, y, w, h) in faces:
                        crop_img = rot_im[y:y+h, x:x+w]
                        # Display and save found image
                        # From this point on program references the raw_cat image
                        # not the temp_img in the current directory
                        # Need to calculate number for file to save at end of directory
                        try:
                            Cat_list = [f for f in os.listdir(
                                    raw_cats) if os.path.isfile(os.path.join(raw_cats, f))]
                            Cat_list = [int(i.split('_')[0]) for i in Cat_list]
                            Cat_list.sort(key = int)
                            pic = Cat_list[-1] + 1
                        except:
                            pic = 1
                        img_pth_crppd = os.path.join(raw_cats,f'{pic}_{self.btdt[-1]}.png')
                        crop_img = self.Skin_cats(crop_img, img_pth_crppd)
                        cv.imwrite(img_pth_crppd, crop_img)
                        self.show_im(img_pth_crppd)
                        pic = self.Cat_count()
                        self.term_msg(f"Slashed cat no. {pic}\n")

        else:
            self.term_msg("No cats!")
        self.term_msg("_____________________________________")
        return

    def Skin_cats(self, crop_img, img_pth_crppd):
        self.term_msg("Skinning cats...")
        def show(im, pth):
            cv.imwrite(pth, im)
            self.show_im(pth)

        # Open original downloaded image, get dimensions (numpy returns h,w)
        def resize_image(im):
            h, w = im.shape
            if h != img_y or w != img_x:
                # resize photo to target size: img_x, img_y. Photos come in many
                # shapes so, 1) get target width percentage of actual width
                percent = (img_x/float(w))
                # 2) reduce height by same percentage and...
                hsize = round(float(h)*float(percent))
                #   ...normalise to img_y (getting values < img_y)
                if hsize < img_y:
                    hsize = img_y
                # 3) resize image to new dimensions (resize expects w,h)
                im = cv.resize(im, (img_x, hsize), 
                               interpolation=cv.INTER_CUBIC)
                # 4) crop image centered on height (target width, img_x, is datum)
                #    cropped image=image[y:y+h,x:x+w]
                im = im[round(hsize/2-img_y/2):round(hsize/2+img_y/2), 0:img_x]
            return im

        def posterise(im):
            av = [] # List of im values to calc average darkness
            n = [0, 28, 57, 85, 113, 142, 170, 198, 227, 255]
            # posteriser
            for y in range(img_y):
                for x in range(img_x):
                    pxl = im.item(y, x)
                    px_val = bisect.bisect_left(n, pxl)
                    # Convert to 10 gray values
                    im.itemset((y, x), int(n[px_val]))
                    av.append(pxl)
            return im, av

        """def adjust_gamma(img_pth, gamma=1.0):
            invGamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** invGamma) * 255
                              for i in np.arange(0, 256)]).astype("uint8")

            return cv.LUT(img_pth, table)"""

        # Get image, convert, resize, posterise
        #image = cv.imread(f_out,0)
        # Resize image to img_x, img_y dimens
        crop_img = resize_image(crop_img)
        # Normalise the intensity range from 0 to 255
        cv.equalizeHist(crop_img)
        show(crop_img, img_pth_crppd)
        self.term_msg("Checking need to flip")
        left, right = [], []
        for y in range (img_y):
            for x in range (0, -(-img_x//2)):
                left.append(crop_img.item(y,x))
        for y in range (img_y):
            for x in range (img_x//2, img_x):
                right.append(crop_img.item(y,x))
        DOI_L = round(round(sum(left)/len(left)/32)*32)
        DOI_R = round(round(sum(right)/len(right)/32)*32)
        self.term_msg(str(DOI_L)+" "+str(DOI_R))

        if DOI_L > DOI_R:
            crop_img = cv.flip(crop_img, 1)
            show(crop_img, img_pth_crppd)
            self.term_msg("Flipped")
        else:
            self.term_msg("OK")
            #cv.imwrite(f_out, image)
        # Check for need to invert
        self.term_msg("checking need to lighten image")
        # Posterise image to 9 gray intensities from black to white
        crop_img, av = posterise(crop_img)
        """av = sum(av)/len(av)
        if av < 64:
            crop_img = adjust_gamma(crop_img, gamma=2.0)
            self.term_msg("Lightening")
            show(crop_img, img_pth_crppd)
        else:
            self.term_msg("OK")"""
        show(crop_img, img_pth_crppd)
        return crop_img

    def Cat_count(self):
        try:
            pic_num = len([f for f in os.listdir(raw_cats) if os.path.isfile(
                os.path.join(raw_cats, f))])
        except:
            pic_num = 1
        
        return pic_num

    def dataBlocks(self, s_cat):
        wndw_data, data, px = [], [], []
        im = cv.imread(s_cat, 0)
        px = [im.item(y,x) for y  in range(img_y) for x in range(img_x)]
        wndw_data = [Counter([px[x+img_x*y]]) for y  in range(img_y) for x in range(img_x)]
        try:
            f = open('test_data.pkl', 'rb')
            data = pickle.load(f)
            f.close()
            for i in range(len(wndw_data)):
                data[i] += wndw_data[i]
        except:
            print("No data file, creating new")
            data += wndw_data

        with open('test_data.pkl', 'wb') as f:
            pickle.dump(data, f)

#======================================================================
#---------------------Second page of notebook--------------------------
class explorer_panel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        topSplitter = wx.SplitterWindow(self)
        vSplitter_top = wx.SplitterWindow(topSplitter)
        vSplitter_btm = wx.SplitterWindow(topSplitter)

        image_out = Download_image(vSplitter_top)             #TopRight_explorer(vSplitter_top)
        terminal_panel = Terminal(vSplitter_btm)
        image_main = TopLeft_explorer(vSplitter_top, terminal_panel, image_out)
        Button_panel = Btm_explorer_Panel(vSplitter_btm, image_main, terminal_panel)

        vSplitter_top.SplitVertically(image_main, image_out)
        vSplitter_top.SetSashGravity(0.5)

        vSplitter_btm.SplitVertically(terminal_panel, Button_panel)
        vSplitter_btm.SetSashGravity(0.5)
        
        topSplitter.SplitHorizontally(vSplitter_top, vSplitter_btm)
        topSplitter.SetSashGravity(0.5)

        topSplitter.SetMinimumPaneSize(min_img_wndw)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

#----------------class for image editing/exploring on second page------
class TopLeft_explorer(wx.Panel):
    def __init__(self, parent, terminal_panel, image_out):
        super(TopLeft_explorer, self).__init__(parent)
        self.term_panel = terminal_panel
        self.image_out = image_out
        #load image
        if not os.path.exists(new_cats + '/img_0'):
            os.makedirs(new_cats + '/img_0')
        im_pth = new_cats + '/img_0'
        files = os.listdir(im_pth)
        im_pths = [os.path.join(im_pth, im_name) for im_name in files]
        try:
            img = max(im_pths, key=os.path.getctime)
            #opening_image = cv.imread(img)
            opening_image = img
        except:
            opening_image = os.path.join(pth + "/gui_graphics/Abe.png")

        # Intitialise the matplotlib figure
        self.figure = plt.figure(figsize=(1, 1))

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes)  

        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Initialise the rectangle
        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='black')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.axes.add_patch(self.rect)

        # Sizer to contain the canvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sizer)
        self.Fit()

        # Connect the mouse events to their relevant callbacks
        self.canvas.mpl_connect('button_press_event', self._onPress)
        self.canvas.mpl_connect('button_release_event', self._onRelease)
        self.canvas.mpl_connect('motion_notify_event', self._onMotion)

        # Lock to stop the motion event from behaving badly 
        # when the mouse isn't pressed
        self.pressed = False

        # If there is an initial image, display it on the figure
        if opening_image is not None:
            self.setImage(opening_image)

    def _onPress(self, event):
        ''' Callback to handle the mouse being clicked and held over the canvas'''

        # Check the mouse press was actually on the canvas
        if event.xdata is not None and event.ydata is not None:

            # Upon initial press of the mouse record the origin
            # and record the mouse as pressed
            self.pressed = True
            self.rect.set_linestyle('dashed')
            self.x0 = event.xdata
            self.y0 = event.ydata

    def _onRelease(self, event):
        '''Callback to handle the mouse being released over the canvas'''

        # Check that the mouse was actually pressed on the canvas
        # to begin with and this isn't a rogue mouse 
        # release event that started somewhere else
        if self.pressed:

            # Upon release draw the rectangle as a solid rectangle
            self.pressed = False
            self.rect.set_linestyle('solid')

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata

            # Set the width and height and origin of the bounding rectangle
            w, h = self.get_square(self.x0, self.x1)
            self.boundingRectWidth = w
            self.boundingRectHeight = h
            self.bouningRectOrigin = (self.x0, self.y0)

            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()
            self.term_msg(f"x0 = {round(self.x0)}, x1 = {round(self.x1)}")
            self.term_msg(f"y0 = {round(self.y0)}, y1 = {round(self.y1)}")
            self.term_msg(f"{round(self.boundingRectWidth)}w x {round(self.boundingRectHeight)}h \n")

            # cropped image=image[y:y+h,x:x+w]
            y = round(self.y0)
            x = round(self.x0)
            im_crop = self.im[y:y + h, x:x + w]
            #get pixel values in range 0 -9
            pix_var = [n.index(j) for i in im_crop for j in i]
            datum = int(len(pix_var)/2)
            cnt = 0
            for i in range(len(pix_var)):
                cnt += abs(pix_var[datum] - pix_var[i])
            av_var = cnt/(len(pix_var)-1)
            print(f"{pix_var} \n {len(pix_var)}, {av_var}, {cnt}")
            cv.imwrite(img_pth, im_crop)
            self.image_out.draw(img_pth)
            for y in range(h):
                for x in range(w):
                    pass
                    
    def _onMotion(self, event):
        '''Callback to handle the motion event created by the mouse moving over the canvas'''

        # If the mouse has been pressed draw an updated
        # rectangle when the mouse is moved so
        # the user can see what the current selection is
        if self.pressed:

            # Check the mouse was released on the canvas, and if it wasn't
            # then just leave the width and height as the last values
            # set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata

            # Set the width and height and draw the rectangle
            w, h = self.get_square(self.x0, self.x1)
            self.rect.set_width(w)
            self.rect.set_height(h)
            
            #self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()

    def get_square(self, x0, x1):
        w = round(x1 - x0)
        h =  w
        if self.y1 < self.y0 and x1 > x0:
            h *= -1
        elif self.y1 > self.y0 and x1 < x0:
            h *= -1
        return w, h

    def setImage(self, pathToImage):
        '''Sets the background image of the canvas'''
        self.image_out.draw(pathToImage)
        # Load the image into matplotlib and PIL
        self.im = cv.imread(pathToImage, cv.IMREAD_GRAYSCALE)
    
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(self.im, cmap='gray') 
        self.canvas.draw()
        self.Refresh()

    def term_msg(self, msg=None):
        if not msg:
            pass
        else:
            self.term_panel.term.WriteText(msg+"\n")
            self.term_panel.term.Update()
        return

    # Open original downloaded image, get dimensions (numpy returns h,w)
    def resize_image(im):
        im = cv2.imread(im)
        im_resized = cv2.resize(im, (224, 224), interpolation=cv2.INTER_LINEAR)

        plt.imshow(cv2.cvtColor(im_resized, cv2.COLOR_BGR2RGB))
        plt.show()

"""#----------------class for image output on second page------
   #---------------Superseded by using Download Image class------
class TopRight_explorer(wx.Panel):
    def __init__(self, parent):
        super(TopRight_explorer, self).__init__(parent)
        #load image
        im_pth = new_cats + '/av_cat'
        files = os.listdir(im_pth)
        im_pths =  [os.path.join(im_pth, im_name) for im_name in files]
        try:
            img_pth = max(im_pths, key=os.path.getctime)
        except:
            img_pth = os.path.join(pth + "/gui_graphics/Abe.png")

        # Intitialise the matplotlib figure
        self.figure = plt.figure(figsize=(1, 1))

        # Create an axes, turn off the labels and add them to the figure
        self.axes = plt.Axes(self.figure,[0,0,1,1])      
        self.axes.set_axis_off() 
        self.figure.add_axes(self.axes) 

        # Add the figure to the wxFigureCanvas
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Sizer to contain the canvas
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(self.sizer)
        self.Fit()

        # If there is an initial image, display it on the figure
        if img_pth is not None:
            self.setImage(img_pth)

    def setImage(self, img):
        '''Sets the background image of the canvas'''

        # Load the image into matplotlib and PIL
        image = cv.imread(img, cv.IMREAD_GRAYSCALE)
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image, cmap='gray') 
        self.canvas.draw()
        self.Refresh()"""

class Btm_explorer_Panel(wx.Panel):
    def __init__(self, parent, image_main, terminal_panel):
        wx.Panel.__init__(self, parent=parent)
        self.panel = wx.Panel(self, -1, size=(580, 180))
        self.image = image_main
        self.terminal_panel = terminal_panel
        self.conv = 0
        self.image_store = []
        self.image_num = 10
        self.inc = 0
        self.current_pic = 0

        # Seed image_store with standard opening image (latest img_0)
        im_pth = new_cats + '/img_0'
        files = os.listdir(im_pth)
        im_pths = [os.path.join(im_pth, im_name) for im_name in files]
        img = max(im_pths, key=os.path.getctime)
        self.image_store.insert(0, img)
        
        self.btn_back = wx.Button(self.panel, id=-1, pos=(38, 10), size=(45, 35))
        self.btn_back.name = "back"
        self.btn_back.SetBitmap(wx.Bitmap(gui_graphics + '/back.png'))
        self.btn_back.Bind(wx.EVT_BUTTON, self.btn_review)
        self.btn_back.ToolTip = wx.ToolTip(f"Move back through {self.image_num} most recent images")

        self.btn_file = wx.Button(self.panel, id=-1, pos=(98, 10), size=(45, 35))
        self.btn_file.SetBitmap(wx.Bitmap(gui_graphics + '/fileOpen.png'))
        self.btn_file.Bind(wx.EVT_BUTTON, self.btn_file_get)
        self.btn_file.ToolTip = wx.ToolTip("Open image file")

        self.btn_rndm = wx.Button(self.panel, id=-1, pos=(158, 10), size=(45, 35))
        self.btn_rndm.SetBitmap(wx.Bitmap(gui_graphics + '/randIm.png'))
        self.btn_rndm.Bind(wx.EVT_BUTTON, self.btn_rndm_get)
        self.btn_rndm.ToolTip = wx.ToolTip("Generate random image")

        self.btn_fwd = wx.Button(self.panel, id=-1, pos=(218, 10), size=(45, 35))
        self.btn_fwd.name = "fwd"
        self.btn_fwd.SetBitmap(wx.Bitmap(gui_graphics + '/fwd.png'))
        self.btn_fwd.Bind(wx.EVT_BUTTON, self.btn_review)
        self.btn_fwd.ToolTip = wx.ToolTip(f"Move forward through {self.image_num} most recent images")

        self.btn_conv = wx.ToggleButton(self.panel, id=-1, pos=(98, 55), size=(45, 35))
        self.btn_conv.SetBitmap(wx.Bitmap(gui_graphics + '/conv.png'))
        self.btn_conv.Bind(wx.EVT_TOGGLEBUTTON, self.btn_conv_get)
        self.btn_conv.ToolTip = wx.ToolTip("Use set size convolution window")

        self.spn_conv = wx.SpinCtrl(self.panel,
                                    id=-1,
                                    pos=(158, 55),
                                    size=(45, 25),
                                    value='3',
                                    min=1,
                                    max=32
                                    )       #size=(55, 35),
        self.spn_conv.Bind(wx.EVT_SPINCTRL, self.spn_conv_onspin)
        self.spn_conv.Bind(wx.EVT_TEXT, self.spn_conv_onspin)
        self.spn_conv.ToolTip = wx.ToolTip("Choose size of convolution window")


    def btn_review(self, event):
        pic_num = len(self.image_store)
        name = event.GetEventObject().name
        if pic_num == 0:
            self.term_msg("No images")
            return
        if name == "back":
            if self.inc >= pic_num:
                self.inc = 0
            self.current_pic = self.inc
            self.inc += 1
        else:
            if self.inc < 0:
                self.inc = pic_num - 1
            self.current_pic = self.inc
            self.inc -= 1
        
        self.image.setImage(self.image_store[self.current_pic])

    def btn_file_get(self, event):
        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open image file", wildcard="Image files (*.png)|*.png",
                        style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            self.add_to_store(pathname)
            self.image.setImage(pathname)

    def btn_rndm_get(self, event):
        rndm = MainIm
        for y in range(img_y):
            for x in range(img_x):
                rndm.itemset((y, x), random.choice(n))
        rnd_img_pth = os.path.join(tmp_img_pth, f"random{dt.now():%d-%m-%Y %H:%M:%S}.png")
        cv.imwrite(rnd_img_pth, rndm)
        self.add_to_store(rnd_img_pth)
        self.image.setImage(rnd_img_pth)

    def add_to_store(self, path):
        if len(self.image_store) < self.image_num:
            self.image_store.insert(0, path)
        else:
            self.image_store.insert(0, path)
            # Remove excess image from cache
            os.remove(self.image_store[-1])
            self.image_store.pop()
        
    def spn_conv_onspin(self, event):
        conv_size = self.spn_conv.GetValue()

        #change rectangle on explorer panel to chosen size-
        x = y = 0
        w = h = conv_size
        self.image.x0 = 0
        self.image.y0 = 0
        dimy, dimx = self.image.im.shape[:2]
        self.image.boundingRectWidth = w
        self.image.boundingRectHeight = h
        self.image.bouningRectOrigin = (y, x)

        # Draw the bounding rectangle
        self.image.rect.set_width(self.image.boundingRectWidth)
        self.image.rect.set_height(self.image.boundingRectHeight)
        self.image.rect.set_xy((y, x))
        self.image.canvas.draw()

        im_crop = self.image.im[y:y + h, x:x + w]
        cv.imwrite(img_pth, im_crop)
        self.image.image_out.draw(img_pth)
        self.image.image_out.Refresh()
        self.image.term_msg(f"{w}x{h} conv chosen")
        
    def btn_conv_get(self, event):
        if event:
            state = event.GetEventObject().GetValue()
            if state == True:
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/pause.png'))
                self.image.term_msg("Convolution runnning")
                self.btn_conv.Update()
                self.conv = 1
            else:
                event.GetEventObject().SetBitmap(wx.Bitmap(gui_graphics + '/conv.png'))
                self.image.term_msg("Convolution paused")
                self.conv = 0
                self.btn_conv.Update()
        else:
            self.conv = 0
            self.btn_conv.SetValue(False)
            self.btn_conv.SetBitmap(wx.Bitmap(gui_graphics + '/conv.png'))
        conv_size = self.spn_conv.GetValue()
        #change rectangle on explorer panel to chosen size-
        x = y = 0
        w = h = conv_size
        self.image.x0 = 0
        self.image.y0 = 0
        dimy, dimx = self.image.im.shape[:2]
        for y_range in range(dimy-h):
            for x_range in range(dimx-w):
                self.image.boundingRectWidth = w
                self.image.boundingRectHeight = h
                self.image.bouningRectOrigin = (x_range, y_range)

                # Draw the bounding rectangle
                self.image.rect.set_width(self.image.boundingRectWidth)
                self.image.rect.set_height(self.image.boundingRectHeight)
                self.image.rect.set_xy((x_range, y_range))
                self.image.canvas.draw()

                im_crop = self.image.im[y_range:y_range + h, x_range:x_range + w]
                # Calculate average variation from datum (central) pixel
                pix_var = [n.index(j) for i in im_crop for j in i]
                datum = int(len(pix_var)/2)
                cnt = 0
                for i in range(len(pix_var)):
                    cnt += abs(pix_var[datum] - pix_var[i])
                av_var = round(cnt/(len(pix_var)-1), 2)

                # Get color of central (datum) pixel
                pxl = n[len(n)//2]
                
                # Scaling the crop to enable text overlay
                scale = (dimy*10, dimx*10)
                im_crop = cv.resize(im_crop, scale, interpolation = cv.INTER_NEAREST)
                cv.putText(
                    im_crop,
                    str(av_var),
                    (280,330),
                    cv.FONT_HERSHEY_SIMPLEX, 
                    1,
                    (255-pxl, 255-pxl, 255-pxl, 255), #font color
                    5) #font stroke
                cv.imwrite(img_pth, im_crop)
                self.image.image_out.draw(img_pth)
                #self.image.image_out.Refresh()
                wx.GetApp().Yield()
                if self.conv == 0:
                    break
            if self.conv == 0:
                break

#======================================================================
class Main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, 
            parent = None, 
            title = "Borges Infinite Image", 
            size = (600,550)
            )
        self.SetIcon(wx.Icon(gui_graphics + '/Abe.png'))
        self.Bind(wx.EVT_CLOSE, self.OnCloseFrame)


        panel = wx.Panel(self)
        notebook = aui.AuiNotebook(panel)
        spider = Front_page(notebook)
        explorer = explorer_panel(notebook)
        notebook.AddPage(spider, 'Spider')
        notebook.AddPage(explorer, 'Explorer')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

    # Empties temp and destroys the main frame which quits the wxPython application
    def OnExitApp(self, event):
        tmp_cats =[f for f in os.listdir(
                tmp_img_pth) if os.path.isfile(os.path.join(tmp_img_pth, f))]
        for f in tmp_cats:
            os.remove(os.path.join(tmp_img_pth, f))
        self.Destroy()

    def OnCloseFrame(self, event):
        dialog = wx.MessageDialog(self, message = "Are you sure you want to quit?", caption = "Caption", style = wx.YES_NO, pos = wx.DefaultPosition)
        response = dialog.ShowModal()

        if (response == wx.ID_YES):
            self.OnExitApp(event)
        else:
            event.StopPropagation()

if __name__ == "__main__":
    app = wx.App()
    frame = Main()
    frame.Show()
    import wx.lib.inspection as wxli
    wxli.InspectionTool().Show()
    app.MainLoop()
    #app.MainLoop()
