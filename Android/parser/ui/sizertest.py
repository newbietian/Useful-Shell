import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, (-1, -1), wx.Size(250,50))
        panel=wx.Panel(self, -1)
        #box=wx.BoxSizer(wx.HORIZONTAL)
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(wx.Button(panel, -1, 'Button1'),1)
        box.Add(wx.Button(panel, -1, 'Button2'), 1)
        box.Add(wx.Button(panel, -1, 'Button3'), 1)

        panel.SetSizer(box)
        self.Centre()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None,-1,'wxboxsizer.py')
        frame.Show()
        return True

app=MyApp(0)
app.MainLoop()