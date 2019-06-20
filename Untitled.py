import os
pth = os.path.dirname(os.path.abspath('__file__'))
# folder for gui graphics
gui_graphics = pth + '/gui_graphics'
# temp file for initial image handling
img_pth = os.path.join(pth, "tmp_img.png")

print(os.path.basename(img_pth))