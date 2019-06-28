import wx
import os

from InteractiveRecognizer import InteractiveRecognizer
import PyInstallerUtils

pth = os.path.dirname(os.path.abspath('__file__'))
# folder for gui graphics
gui_graphics = pth + '/gui_graphics'
# temp file for initial image handling
img_pth = os.path.join(pth, "tmp_img.png")
# Folders, subfolders for processed images
all_cats = pth + '/Cats'
raw_cats = all_cats + '/raw_cats'
dead_cats = all_cats + '/dead_cats'
new_cats = all_cats + '/new_cats'
# Classifier files for face recognition
cascades1 = all_cats + '/cascades/haarcascade_frontalcatface.xml'
cascades2 = all_cats + '/cascades/haarcascade_frontalcatface_extended.xml'
cascades3 = all_cats + '/cascades/haarcascade_eye.xml'

def main():
    app = wx.App()
    recognizerPath = PyInstallerUtils.resourcePath(
            'recognizers/lbph_cat_faces.xml')
    cascadePath = PyInstallerUtils.resourcePath(
            # Uncomment the next argument for LBP.
            #'cascades/lbpcascade_frontalcatface.xml')
            # Uncomment the next argument for Haar with basic
            # features.
            #'cascades/haarcascade_frontalcatface.xml')
            # Uncomment the next argument for Haar with extended
            # features.
            #'cascades/haarcascade_frontalcatface_extended.xml'
            cascades2)
    interactiveRecognizer = InteractiveRecognizer(
            recognizerPath, cascades2,
            scaleFactor=1.2, minNeighbors=1,
            minSizeProportional=(0.125, 0.125),
            title='Interactive Cat Face Recognizer')
    interactiveRecognizer.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
