# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

img_pth = "Cats/new_cats/av_cat/new_cat_av 07-09-2020 18:49.png"
min_img_wndw = 295
class MyFrame1 ( wx.Frame ):

    def __init__( self ):
        wx.Frame.__init__ ( self, parent=None, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_splitter1 = wx.SplitterWindow( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )

        self.m_panel6 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.Size( min_img_wndw,min_img_wndw ), wx.TAB_TRAVERSAL )
        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        bSizer6.SetMinSize( wx.Size( min_img_wndw,min_img_wndw ) )
        self.m_bitmap2 = wx.StaticBitmap(self, bitmap=wx.Bitmap(wx.Image(min_img_wndw, min_img_wndw)))
        #self.m_bitmap2 = wx.StaticBitmap( self.m_panel6, wx.ID_ANY, wx.Bitmap( u"Cats/new_cats/av_cat/new_cat_av 07-09-2020 18:49.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_bitmap2, 1, wx.EXPAND|wx.ALL, 5)
        display_im  = wx.Image(img_pth, wx.BITMAP_TYPE_ANY)
        display_im = display_im.Scale(min_img_wndw, min_img_wndw)
        self.m_bitmap2.SetBitmap(wx.Bitmap(display_im))
        self.Refresh()


        self.m_panel6.SetSizer( bSizer6 )
        self.m_panel6.Layout()
        self.m_panel7 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 295,295 ), wx.TAB_TRAVERSAL )
        bSizer7 = wx.BoxSizer( wx.VERTICAL )

        bSizer7.SetMinSize( wx.Size( 295,295 ) )
        self.m_textCtrl1 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.m_textCtrl1.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
        self.m_textCtrl1.SetMinSize( wx.Size( 295,295 ) )

        bSizer7.Add( self.m_textCtrl1, 0, wx.ALL, 5 )


        self.m_panel7.SetSizer( bSizer7 )
        self.m_panel7.Layout()
        self.m_splitter1.SplitVertically( self.m_panel6, self.m_panel7, 0 )
        bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 5 )

        self.m_splitter2 = wx.SplitterWindow( self.m_panel4, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter2.Bind( wx.EVT_IDLE, self.m_splitter2OnIdle )

        self.m_panel8 = wx.Panel( self.m_splitter2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_splitter2.Initialize( self.m_panel8 )
        bSizer3.Add( self.m_splitter2, 1, wx.EXPAND, 5 )

        self.m_slider2 = wx.Slider( self.m_panel4, wx.ID_ANY, 1, 1, 200, wx.Point( -1,-1 ), wx.Size( 295,10 ), wx.SL_HORIZONTAL )
        bSizer3.Add( self.m_slider2, 0, wx.ALL, 5 )

        self.m_gauge1 = wx.Gauge( self.m_panel4, wx.ID_ANY, 100, wx.DefaultPosition, wx.Size( 295,10 ), wx.GA_HORIZONTAL )
        self.m_gauge1.SetValue( 0 )
        bSizer3.Add( self.m_gauge1, 0, wx.ALL, 5 )


        self.m_panel4.SetSizer( bSizer3 )
        self.m_panel4.Layout()
        bSizer3.Fit( self.m_panel4 )
        self.m_notebook1.AddPage( self.m_panel4, u"Spider", True )
        self.m_panel41 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer31 = wx.BoxSizer( wx.VERTICAL )

        self.m_splitter11 = wx.SplitterWindow( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter11.Bind( wx.EVT_IDLE, self.m_splitter11OnIdle )

        self.m_panel61 = wx.Panel( self.m_splitter11, wx.ID_ANY, wx.DefaultPosition, wx.Size( 295,295 ), wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        bSizer61.SetMinSize( wx.Size( 295,295 ) )
        self.m_bitmap21 = wx.StaticBitmap( self.m_panel61, wx.ID_ANY, wx.Bitmap( u"Cats/new_cats/av_cat/new_cat_av 07-09-2020 18:49.png", wx.BITMAP_TYPE_ANY ), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer61.Add( self.m_bitmap21, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_panel61.SetSizer( bSizer61 )
        self.m_panel61.Layout()
        self.m_panel71 = wx.Panel( self.m_splitter11, wx.ID_ANY, wx.DefaultPosition, wx.Size( 295,295 ), wx.TAB_TRAVERSAL )
        bSizer71 = wx.BoxSizer( wx.VERTICAL )

        bSizer71.SetMinSize( wx.Size( 295,295 ) )
        self.m_textCtrl11 = wx.TextCtrl( self.m_panel71, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_textCtrl11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BACKGROUND ) )
        self.m_textCtrl11.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
        self.m_textCtrl11.SetMinSize( wx.Size( 295,295 ) )

        bSizer71.Add( self.m_textCtrl11, 0, wx.ALL, 5 )


        self.m_panel71.SetSizer( bSizer71 )
        self.m_panel71.Layout()
        self.m_splitter11.SplitVertically( self.m_panel61, self.m_panel71, 0 )
        bSizer31.Add( self.m_splitter11, 1, wx.EXPAND, 5 )

        self.m_splitter21 = wx.SplitterWindow( self.m_panel41, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.m_splitter21.Bind( wx.EVT_IDLE, self.m_splitter21OnIdle )

        self.m_panel81 = wx.Panel( self.m_splitter21, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.m_splitter21.Initialize( self.m_panel81 )
        bSizer31.Add( self.m_splitter21, 1, wx.EXPAND, 5 )


        self.m_panel41.SetSizer( bSizer31 )
        self.m_panel41.Layout()
        bSizer31.Fit( self.m_panel41 )
        self.m_notebook1.AddPage( self.m_panel41, u"Explorer", False )

        bSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass

    def m_splitter1OnIdle( self, event ):
        self.m_splitter1.SetSashPosition( 0.5 )
        self.m_splitter1.Unbind( wx.EVT_IDLE )

    def m_splitter2OnIdle( self, event ):
        self.m_splitter2.SetSashPosition( 0.5 )
        self.m_splitter2.Unbind( wx.EVT_IDLE )

    def m_splitter11OnIdle( self, event ):
        self.m_splitter11.SetSashPosition( 0.5 )
        self.m_splitter11.Unbind( wx.EVT_IDLE )

    def m_splitter21OnIdle( self, event ):
        self.m_splitter21.SetSashPosition( 0.5 )
        self.m_splitter21.Unbind( wx.EVT_IDLE )

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame1()
    frame.Show()
    app.MainLoop()
