import wx


class Frame(wx.Frame):
    """Frame class."""

    def __init__(self, parent=None, id=-1, title="Title",
                 pos=wx.DefaultPosition, size=(400, 200)):
        """Create a Frame instance."""
        wx.Frame.__init__(self, parent, id, title, pos, size)

        self.text_id = wx.NewId()
        self.text = wx.TextCtrl(self, self.text_id)
        self.text.Bind(wx.EVT_RIGHT_UP, self.OnRightClick, id=self.text_id)

        self.statusbar = self.CreateStatusBar(1, 0)

        wx.CallAfter(self.call, 1, 'abc', name="ccc", help="test")
        wx.FutureCall(5000, self.call, 'call after 100ms', name="test")

    def OnRightClick(self, event):
        wx.MessageBox("message window", "message", wx.OK, self)

    def call(self, *args, **kwargs):
        message = repr(args) + repr(kwargs)
        print message
        self.SetStatusText(message, 0)


class App(wx.App):
    """Application class."""

    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


def main():
    app = App()
    app.MainLoop()


if __name__ == '__main__':
    main()