# Image downloader GUI
Launches spider, downloads images from r/cats/new, scans for  full frontal cat faces, clips face from image, reduces to 64x64 pixels, grayscale, 9 intensities, saves. On completion of image gathering analyses each image, records pixel intensities and saves to an 'intensity value':'number of occurences' key:val dict. Dict is then used to generate various images. On completion of analysis images are moved to a holding folder for future use as an image database of cropped cat faces.