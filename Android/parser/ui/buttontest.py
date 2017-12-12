import wx

def main():
    app=wx.PySimpleApp()
    frame=wx.Frame(None, -1 , 'Icon', wx.DefaultPosition, wx.Size(350,300))
    frame.SetIcon(wx.Icon('Tipi.ico',wx.BITMAP_TYPE_ICO))
    frame.Center()
    frame.Show()
    app.MainLoop()

if __name__ =='__main__':
    main()