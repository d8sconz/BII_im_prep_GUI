#!/usr/bin/env python3.7

import asyncio
import bisect
import itertools
import os
# Pickle for saving/retrieving data file
import pickle
import time
# Counter for pixel value k:v countable dict where,
# k = pixel value, and v = number of occurences
from collections import Counter

import aiohttp
import cv2 as cv

# Matplotlib chosen for image render because it works.
# Need to return to this and try wxStaticBitmap again with wx.GetApp().Yield()
import matplotlib.pyplot as plt
import numpy as np
import praw
import wx
import wx.lib.agw.aui as aui
#import wx.lib.mixins.inspection as wit

import matplotlib as mpl
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

import generate

# ------------------file variables-------------------
# Base path
pth = os.path.dirname(os.path.abspath('__file__'))
# temp file for initial image handling
img_pth = os.path.join(pth, "tmp_img.png")
# Folders, subfolders for processed images
all_cats = os.getcwd() + '/Cats'
raw_cats = all_cats + '/raw_cats'
dead_cats = all_cats + '/dead_cats'
# Classifier files for face recognition
cascades1 = all_cats + '/cascades/haarcascade_frontalcatface.xml'
cascades2 = all_cats + '/cascades/haarcascade_frontalcatface_extended.xml'
cascades3 = all_cats + '/cascades/haarcascade_eye.xml'
# Classifiers for face recognition
cat_face1 = cv.CascadeClassifier(cascades1)
cat_face2 = cv.CascadeClassifier(cascades2)
cat_face3 = cv.CascadeClassifier(cascades3)
# Processed image dimensions
min_img_wndw = 295      # min size of top panels
img_y, img_x = 64, 64   # raw cat size
im_resize_init = 1280   # Initial resize dimension of downloaded images

#Ghost of programs past - for use with wx.staticBitmap if I return to it
MainIm = np.zeros((img_x, img_y), np.uint8)

# ---------------class for panel containing image-----------------
class TopLeft_spider(wx.Panel):
    def __init__(self, parent):
        super(TopLeft_spider, self).__init__(parent)
        #load image
        im_pth = all_cats + '/new_cats/av_cat'
        files = os.listdir(im_pth)
        im_pths =  [os.path.join(im_pth, im_name) for im_name in files]
        img = max(im_pths, key=os.path.getctime)

        self.figure = Figure()
        self.axes = self.figure.add_axes([0, 0, 1, 1])
        self.axes.axis('off')
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.draw(img)

    def draw(self, img_pth):
        self.figure.clf()
        #self.figure = Figure(frameon=False)
        self.axes = self.figure.add_axes([0, 0, 1, 1])
        self.axes.axis('off')
        #self.canvas = FigureCanvas(self, -1, self.figure)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.SetDimension ( 0, 0, min_img_wndw, min_img_wndw)
        self.SetSizer(self.sizer)

        img = cv.imread(img_pth)
        self.axes.imshow(img).set_array(img)
        self.canvas.draw()

class TopLeft_explorer(wx.Panel):
    def __init__(self, parent):
        super(TopLeft_explorer, self).__init__(parent)
        #load image
        im_pth = all_cats + '/new_cats/av_cat'
        files = os.listdir(im_pth)
        im_pths =  [os.path.join(im_pth, im_name) for im_name in files]
        img_pth = max(im_pths, key=os.path.getctime)

        # Intitialise the matplotlib figure
        self.figure = plt.figure()

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
        self.sizer.Add(self.canvas, 3, wx.ALL)
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
        if img_pth is not None:
            self.setImage(img_pth)


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
            self.boundingRectWidth =  self.x1 - self.x0
            self.boundingRectHeight =  self.y1 - self.y0
            self.bouningRectOrigin = (self.x0, self.y0)

            # Draw the bounding rectangle
            self.rect.set_width(self.boundingRectWidth)
            self.rect.set_height(self.boundingRectHeight)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()


    def _onMotion(self, event):
        '''Callback to handle the motion event created by the mouse moving over the canvas'''

        # If the mouse has been pressed draw an updated rectangle when the mouse is moved so 
        # the user can see what the current selection is
        if self.pressed:

            # Check the mouse was released on the canvas, and if it wasn't then just leave the width and 
            # height as the last values set by the motion event
            if event.xdata is not None and event.ydata is not None:
                self.x1 = event.xdata
                self.y1 = event.ydata
            
            # Set the width and height and draw the rectangle
            self.rect.set_width(self.x1 - self.x0)
            self.rect.set_height(self.y1 - self.y0)
            self.rect.set_xy((self.x0, self.y0))
            self.canvas.draw()


    def setImage(self, pathToImage):
        '''Sets the background image of the canvas'''
        
        # Load the image into matplotlib and PIL
        image = cv.imread(pathToImage) 

        # Save the image's dimensions from PIL
        self.imageSize = image.size
        
        # Add the image to the figure and redraw the canvas. Also ensure the aspect ratio of the image is retained.
        self.axes.imshow(image,aspect='equal') 
        self.canvas.draw()



# ---------------class for panel containing terminal output-----------
class TopRight(wx.Panel):
    def __init__(self, parent):
        super(TopRight, self).__init__(parent)
        self.term = wx.TextCtrl(self, size = (200,100),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
        self.term.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.term.SetBackgroundColour(wx.BLACK)     
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.term, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Layout()

# -----------------Panel for all controls------------------------- 
class BottomPanel(wx.Panel):
    def __init__(self, parent, image_panel, terminal_panel):
        wx.Panel.__init__(self, parent = parent)
        self.panel = wx.Panel(self, -1, size=(580,180))
        self.btn1 = wx.Button(self.panel, label='Go!', id=1, pos =(400,30))
        self.btn2 = wx.Button(self.panel, label='Crap Cat!', id=2, pos =(400,70))
        self.btn3 = wx.Button(self.panel, label='Good Cat!', id=2, pos =(400,110))
        self.btn1.SetDefault()
        self.btn1.SetFocus()
        
        self.btdt = []   # list of already visited sites (Been There Done That)
        self.r = praw.Reddit('bot1')    # Initialises reddit bot to download cat images

        self.cat_panel = image_panel
        self.term_panel = terminal_panel

        self.cat_sld = wx.Slider(
            self.panel, 
            value = 1, 
            minValue = 1, 
            maxValue = 200, 
            pos=(15,20), 
            size=(320,-1), 
            style=wx.SL_HORIZONTAL|wx.SL_LABELS
            )
        
        self.progress = wx.Gauge(
            self.panel, 
            -1, 
            100, 
            pos=(20,100),
            size=(315,-1), 
            style=wx.GA_HORIZONTAL|wx.GA_SMOOTH
            )

        self.progress.SetValue( 0 )
        self.progress.SetRange(self.cat_sld.GetValue())
        self.progress.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

        self.btn1.Bind(wx.EVT_BUTTON, self.button1_press)
        self.btn2.Bind(wx.EVT_BUTTON, self.button2_press)
        self.btn3.Bind(wx.EVT_BUTTON, self.button3_press)

    def button1_press(self, event):
        self.reject_cat = 0
        self.good_cat = 0
        self.get_cats()

    def button2_press(self, event):
        self.good_cat = 0
        self.reject_cat = 1
        self.btn1.SetDefault()
        self.btn1.SetFocus()

    def button3_press(self, event):
        self.reject_cat = 0
        self.good_cat = 1
        self.btn1.SetDefault()
        self.btn1.SetFocus()
    def get_focus(self):
        focused = wx.Window.FindFocus()
        if focused == self.btn1:
            return 2
        elif focused == self.btn2:
            return 1
    
    def spider(self):
        def get_pic(href):
            parts = 8  # number of parts for asyncio download
            #print("\nSaving {}".format(href))
            #print(f"Checking {href}...", '\n')
            self.term_msg("Downloading...")
            loop_until_done(href, parts)
            return

        def loop_until_done(image_url, parts):
            #loop = asyncio.get_event_loop()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            bs = loop.run_until_complete(download(image_url, parts))
            try:
                with open(img_pth, "wb") as fi:
                    fi.write(bs)
            except OSError:
                print("Damaged file rejected")
            return
        
        async def download(url, parts):
            async def get_partial_content(u, i, start, end):
                async with aiohttp.ClientSession() as sess:
                    async with sess.get(u, headers={
                            "Range": "bytes={}-{}".format(
                                    start, end - 1 if end else "")}) as _resp:
                        return i, await _resp.read()

            async with aiohttp.ClientSession() as sess:
                async with sess.get(url) as resp:
                    try:
                        size = int(resp.headers["Content-Length"])
                    except KeyError:
                        self.spider()

            ranges = list(range(0, size, size // parts))

            res, _ = await asyncio.wait([get_partial_content(url, i, start, end)
                                        for i, (start, end)
                                        in enumerate(itertools.zip_longest
                                                    (ranges, ranges[1:],
                                                    fillvalue=""))])
            sorted_result = sorted(task.result() for task in res)
            return b"".join(data for _, data in sorted_result)

        #pic = 1
        # Collect btdt from any existing files to prevent re-download
        files = os.listdir(raw_cats)
        for f in files:
            self.btdt.append(f[:6])
        self.btdt = list(dict.fromkeys(self.btdt))
        
        for submission in self.r.subreddit('cats').new(limit=None):
            href = submission.url
            user = submission.id
            if (href.endswith(".png") or href.endswith(".jpg")) and user not in self.btdt:
                # Add user to list to prevent duplicates
                self.btdt.append(user)
                # Download image
                get_pic(href)
                # Find appropriate faces, crop, posterise, save - passes name of temp file
                self.find_cats(img_pth)
                # Count files in raw_cats folder and break from loop when limit is reached
                pic = self.Cat_count()
                if pic > 0:
                    break
        # Remove temp file
        
        return
    
    ##################    Image processing functions:   #######################
    ################## takes raw images from spider and ####################### 
    ##################      finds,  resizes, crops,     #######################
    ##################      posterises and saves        #######################
    
    def find_cats(self,img_pth):     #Takes name of temp file from spider
        # Open and view raw downloaded image
        image = cv.imread(img_pth, cv.COLOR_RGB2BGR)
        self.show_im(img_pth, image)
        # Standardise color, convert to grayscale and normalise...
        # the range 0 - 255 and view each step
        if image.shape[2]:
            image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        self.show_im(img_pth, image)
        cv.equalizeHist(image)  # np.zeros((img_y, img_x))
        #image = cv.normalize(image,  normalisedImg, 0, 255, cv.NORM_MINMAX)
        self.show_im(img_pth, image)

        # Make image square with padding and resize
        old_size = image.shape[:2] # old_size is in (height, width) format

        ratio = float(im_resize_init)/max(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        image = cv.resize(image, (new_size[1], new_size[0]))

        delta_w = im_resize_init - new_size[1]
        delta_h = im_resize_init - new_size[0]
        top, bottom = delta_h//2, delta_h-(delta_h//2)
        left, right = delta_w//2, delta_w-(delta_w//2)

        color = [0, 0, 0]
        image = cv.copyMakeBorder(image, top, bottom, left, right, cv.BORDER_CONSTANT,
            value=color)

        rows,cols = image.shape
        #faces = cat_face3.detectMultiScale(image, 1.05, 5)
        #eyes = cat_face2.detectMultiScale(image, 1.035, 5)
        faces = cat_face1.detectMultiScale(image, 1.04, 3, minSize=(128,128))
        detect = len(faces) #+ len(eyes)
        if detect or self.good_cat:
            self.good_cat = 0   #reset switch for next cat
            self.term_panel.term.WriteText("Looking for cats...\n")
            # Rotate image and finer check for cat faces
            for i in range(0,360,int(360/72)):  # rotate at 5 degree increments
                # Routine to rotate and display image in search of cats
                M = cv.getRotationMatrix2D((cols/2,rows/2),i,1)
                rot_im = cv.warpAffine(image,M,(cols,rows))
                self.show_im(img_pth, rot_im)
                # Check rotated image for cats and crop/save any found
                faces = cat_face2.detectMultiScale(rot_im, 1.08, 5, minSize=(128,128))
                if len(faces):
                    self.term_panel.term.WriteText("Cats ahoy!\nCutting cats!\n")
                    for (x, y, w, h) in faces:
                        crop_img = rot_im[y:y+h, x:x+w]
                        # Display and save found image
                        # From this point on program references the raw_cat image
                        # not the temp_img in the current directory
                        pic = self.Cat_count()
                        img_pth_crppd = os.path.join(raw_cats,f'{self.btdt[-1]}_{pic}.png')
                        self.show_im(img_pth_crppd, crop_img)
                        self.Skin_cats(img_pth_crppd)
                        self.term_msg(f"Slashed cat no. {pic}\n")
                
                if self.reject_cat:
                    self.reject_cat = 0 # reset switch for next cat
                    break
                wx.GetApp().Yield()

        else:
            self.term_msg("No cats!")            
        self.term_msg("___________________________________________")
        return

    def get_cats(self):
        pic = self.Cat_count()
        self.btn1.Disable()
        num = self.cat_sld.GetValue()
        if pic < num:
            self.term_msg("Launching spider...")
            self.progress.SetRange(num)
            while pic < num:
                num = self.cat_sld.GetValue()
                self.spider()
                pic = self.Cat_count()
                if pic > num: pic = num
                self.progress.SetValue( pic )
                self.progress.Update()
            self.term_msg("================================================")
            self.term_msg("Check for noses and click OK, or press Enter...")
        else:
            self.progress.SetValue(0)
            self.progress.Update()
            Cat_cnt = [f for f in os.listdir(
                raw_cats) if os.path.isfile(os.path.join(raw_cats, f))]
            for i in range(pic):
                self.term_msg(f"Scanning {Cat_cnt[i]}, {pic-i} to go")
                s_cat = os.path.join(raw_cats, Cat_cnt[i])
                d_cat = os.path.join(dead_cats, Cat_cnt[i])
                image = cv.imread(s_cat,0)
                self.show_im(s_cat, image)
                self.dataBlocks(s_cat)
                os.rename(s_cat, d_cat)
            for i in range(9):
                image = generate.img(i)
                self.show_im('tmp_img.png', image)
            av_im, post_im = generate.av_img()
            image = cv.imread(av_im,0)
            self.show_im(av_im, image)
            time.sleep(.5)
            image = cv.imread(post_im,0)
            self.show_im(post_im, image)
            image = generate.max_rndm_img()
            self.show_im('tmp_img.png', image)
            os.remove('tmp_img.png')
        self.btn1.Enable()

    def Skin_cats(self,f_out):
        self.term_msg("Skinning cats...")
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
            n = [0, 32, 64, 96, 128, 160, 192, 224, 255]
            # posteriser
            for y in range(img_y):
                for x in range(img_x):
                    pxl = im.item(y, x)
                    px_val = bisect.bisect_left(n, pxl)
                    # Convert to 12 gray values
                    im.itemset((y, x), int(n[px_val]))
                    av.append(im.item(y,x))
            return im, av
        
        def adjust_gamma(image, gamma=1.0):
            invGamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** invGamma) * 255
                for i in np.arange(0, 256)]).astype("uint8")
    
            return cv.LUT(image, table)
    
        # Get image, convert, resize, posterise
        image = cv.imread(f_out,0)
        # Resize image to img_x, img_y dimens
        image = resize_image(image)
        # Normalise the intensity range from 0 to 255
        cv.equalizeHist(image)
        self.show_im(f_out, image)
        self.term_msg("Checking need to flip")
        left, right = [], []
        for y in range (img_y):
            for x in range (0, -(-img_x//2)):
                left.append(image.item(y,x))
        for y in range (img_y):
            for x in range (img_x//2, img_x):
                right.append(image.item(y,x))
        DOI_L = round(round(sum(left)/len(left)/32)*32)
        DOI_R = round(round(sum(right)/len(right)/32)*32)
        self.term_msg(str(DOI_L)+" "+str(DOI_R))
    
        if DOI_L > DOI_R:
            image = cv.flip(image, 1)
            self.show_im(f_out, image)
            self.term_msg("Flipped")
        else:
            self.term_msg("OK")
            cv.imwrite(f_out, image)
        # Check for need to invert
        self.term_msg("checking need to lighten image")
        # Posterise image to 9 gray intensities from black to white
        image, av = posterise(image)
        av = sum(av)/len(av)
        if av < 64:
            image = adjust_gamma(image, gamma=2.0)
            self.term_msg("Lightening")
            self.show_im(f_out, image)
        else:
            self.term_msg("OK")
            self.show_im(f_out, image)
        return
    
    def Cat_count(self):
        pic_num = len([f for f in os.listdir(raw_cats) if os.path.isfile(
            os.path.join(raw_cats, f))])
        return pic_num
    
    def show_im(self, f_out, image):
        cv.imwrite(f_out, image)
        self.cat_panel.draw(f_out)
        if f_out == 'tmp_img.png':
            time.sleep(.5)
        else:
            time.sleep(.02)
        wx.GetApp().Yield()
        return

    def term_msg(self, msg):
        self.term_panel.term.WriteText(msg+"\n")
        wx.GetApp().Yield()
        return
        
    def subreddit_list(self):
        subreddits = list(self.r.user.subreddits())
        subs = [str(subreddit) for subreddit in subreddits]
        subs.sort(key=str.lower)
        return subs
                
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
            
        f = open('test_data.pkl', 'wb')
        pickle.dump(data, f)
        f.close()

class splitter_panel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)
 
        image_panel = TopLeft_spider(vSplitter)
        terminal_panel = TopRight(vSplitter)
        #terminal_panel.SetBackgroundColour(wx.BLACK)
        vSplitter.SplitVertically(image_panel, terminal_panel)
        vSplitter.SetSashGravity(0.5)

        panelThree = BottomPanel(topSplitter, image_panel, terminal_panel)
        topSplitter.SplitHorizontally(vSplitter, panelThree)
        topSplitter.SetSashGravity(0.5)

        topSplitter.SetMinimumPaneSize(min_img_wndw)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

class Btm_explorer_Panel(wx.Panel):
    def __init__(self, parent, image_panel, terminal_panel):
        wx.Panel.__init__(self, parent = parent)
        self.panel = wx.Panel(self, -1, size=(580,180))
        self.btn1 = wx.Button(self.panel, label='Go!', id=1, pos =(400,30))
        self.btn2 = wx.Button(self.panel, label='Crap Cat!', id=2, pos =(400,70))
        self.btn3 = wx.Button(self.panel, label='Good Cat!', id=2, pos =(400,110))
        self.btn1.SetDefault()
        self.btn1.SetFocus()
        
        self.btdt = []   # list of already visited sites (Been There Done That)
        self.r = praw.Reddit('bot1')    # Initialises reddit bot to download cat images

        self.cat_panel = image_panel
        self.term_panel = terminal_panel

        self.cat_sld = wx.Slider(
            self.panel, 
            value = 1, 
            minValue = 1, 
            maxValue = 200, 
            pos=(15,20), 
            size=(320,-1), 
            style=wx.SL_HORIZONTAL|wx.SL_LABELS
            )
        
        self.progress = wx.Gauge(
            self.panel, 
            -1, 
            100, 
            pos=(20,100),
            size=(315,-1), 
            style=wx.GA_HORIZONTAL|wx.GA_SMOOTH
            )

        self.progress.SetValue( 0 )
        self.progress.SetRange(self.cat_sld.GetValue())
        self.progress.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

        self.btn1.Bind(wx.EVT_BUTTON, self.button1_press)
        self.btn2.Bind(wx.EVT_BUTTON, self.button2_press)
        self.btn3.Bind(wx.EVT_BUTTON, self.button3_press)

    def button1_press(self, event):
        self.reject_cat = 0
        self.good_cat = 0
        self.get_cats()

    def button2_press(self, event):
        self.good_cat = 0
        self.reject_cat = 1
        self.btn1.SetDefault()
        self.btn1.SetFocus()

    def button3_press(self, event):
        self.reject_cat = 0
        self.good_cat = 1
        self.btn1.SetDefault()
        self.btn1.SetFocus()
    def get_focus(self):
        focused = wx.Window.FindFocus()
        if focused == self.btn1:
            return 2
        elif focused == self.btn2:
            return 1
    
class explorer_panel(wx.Panel):
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        topSplitter = wx.SplitterWindow(self)
        vSplitter = wx.SplitterWindow(topSplitter)
 
        image_panel = TopLeft_explorer(vSplitter)
        terminal_panel = TopRight(vSplitter)
        #terminal_panel.SetBackgroundColour(wx.BLACK)
        vSplitter.SplitVertically(image_panel, terminal_panel)
        vSplitter.SetSashGravity(0.5)

        panelThree = Btm_explorer_Panel(topSplitter, image_panel, terminal_panel)
        topSplitter.SplitHorizontally(vSplitter, panelThree)
        topSplitter.SetSashGravity(0.5)
        topSplitter.SetMinimumPaneSize(min_img_wndw)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

class PlotNotebook(wx.Panel):
    def __init__(self, parent, id=-1):
        wx.Panel.__init__(self, parent, id=id)
        self.nb = aui.AuiNotebook(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.nb, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def add(self, name):
        page = self.TopPanel(self.nb)
        self.nb.AddPage(page, name)
        return page.figure

class Main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, 
            parent = None, 
            title = "Borges Infinite Image", 
            size = (600,550)
            )
        self.SetIcon(wx.Icon("Abe.png"))

        panel = wx.Panel(self)
        notebook = aui.AuiNotebook(panel)
        splitter = splitter_panel(notebook)
        explorer = explorer_panel(notebook)
        notebook.AddPage(splitter, 'Spider')
        notebook.AddPage(explorer, 'Explorer')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        
if __name__ == "__main__":
    app = wx.App()
    frame = Main()
    frame.Show()
    app.MainLoop()
