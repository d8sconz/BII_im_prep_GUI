import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import wx
import wx.lib.agw.aui as aui

class TopRight(wx.Panel):
    def __init__(self, parent):
        super(TopRight, self).__init__(parent)
        self.term = wx.TextCtrl(self,
                                size=(200, 100),
                                style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH
                                )
        self.term.SetDefaultStyle(wx.TextAttr(wx.GREEN))
        self.term.SetBackgroundColour(wx.BLACK)     
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.term, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.term.WriteText("hello")
        self.term.Update

class TopLeft(wx.Panel):
    def __init__(self, parent):
        super(TopLeft , self).__init__(parent)

        img_pth = "av_cat.png"
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
        self.sizer.Add(self.canvas, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(self.sizer)
        
        # If there is an initial image, display it on the figure
        if img_pth is not None:
            self.setImage(img_pth)

    
    def setImage(self, pathToImage):
        # Load the image into matplotlib
        image = cv.imread(pathToImage) 
        # Add the image to the figure and redraw the canvas.
        self.axes.imshow(image)
        self.canvas.draw()

class explorer_panel(wx.Panel):
    def __init__(self, parent):
        #Constructor
        wx.Panel.__init__(self, parent)
        topSplitter = wx.SplitterWindow(self)
        image_panel = TopLeft(topSplitter)
        terminal_panel = TopRight(topSplitter)
        topSplitter.SplitVertically(image_panel, terminal_panel)
        topSplitter.SetSashGravity(0.5)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

class Main(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, 
            parent = None, 
            title = "Borges Infinite Image", 
            size = (600,350)
            )

        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)
        explorer = explorer_panel(notebook)
        notebook.AddPage(explorer, 'Explorer')
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

if __name__ == "__main__":
    app = wx.App()
    frame = Main()
    frame.Show()
    import wx.lib.inspection as wxli
    wxli.InspectionTool().Show()
    app.MainLoop()