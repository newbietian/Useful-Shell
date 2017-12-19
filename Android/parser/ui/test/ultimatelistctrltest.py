#-*- coding=utf-8 -*-
import wx
from wx.lib.agw import ultimatelistctrl as ULC
from ui.images import images as image

########################################################################
class TestPanel(wx.Panel):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)

        try:
            font = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
            boldfont = wx.SystemSettings_GetFont(wx.SYS_DEFAULT_GUI_FONT)
        except AttributeError:
            # wxPython 4 / Phoenix updated SystemSettings
            font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
            boldfont = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)

        boldfont.SetWeight(wx.BOLD)
        boldfont.SetPointSize(14)

        self.il = ULC.PyImageList(20, 20)
        self.il.Add(image.task_process.getBitmap())
        self.il.Add(image.task_start.getBitmap())
        self.il.Add(image.task_waiting.getBitmap())
        self.il.Add(image.task_done.getBitmap())



        self.ultimateList = ULC.UltimateListCtrl(self, agwStyle=wx.LC_REPORT
                                                                | wx.LC_VRULES
                                                                | wx.LC_HRULES)

        self.ultimateList.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        # 参考资料
        # http://xoomer.virgilio.it/infinity77/Phoenix/lib.agw.ultimatelistctrl.UltimateListItem.html#lib.agw.ultimatelistctrl.UltimateListItem
        # 设置第一列的样式
        # 创建一个ULC list item
        info = ULC.UltimateListItem()
        # mask可以出现哪些形式的
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info._format = ULC.ULC_FORMAT_LEFT
        info._kind = 1
        info._text = "Artist Name"
        self.ultimateList.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = ULC.ULC_FORMAT_LEFT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info._text = "Title"
        info._font = boldfont
        self.ultimateList.InsertColumnInfo(1, info)

        # info = ULC.UltimateListItem()
        # info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        # info._format = 0
        # info._text = "Genre"
        # info._font = font
        # info._image = []
        #self.ultimateList.InsertColumnInfo(2, info)



        for i in range(10):
            index = self.ultimateList.InsertImageStringItem(i,
                                                            "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android",
                                                            3)
            #self.ultimateList.InsertStringItem(i, "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android")
            item = self.ultimateList.GetItem(i, 1)
            if i < 3 :
                self.gauge = wx.Gauge(self.ultimateList, -1, size=(250,20),style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
                self.gauge.SetValue(20)
                item.SetWindow(self.gauge)
                self.ultimateList.SetItem(item)
                self.ultimateList.SetStringItem(i, 1, "99%")
            else:
                self.ultimateList.SetStringItem(i, 1, "Waiting...")
        #self.ultimateList.SetStringItem(0, 2, "Rock")

        #self.ultimateList.InsertStringItem(1, "Puffy")
        #self.ultimateList.SetStringItem(1, 1, "Bring It!")
        #self.ultimateList.SetStringItem(1, 2, "Pop")

        #self.ultimateList.InsertStringItem(2, "Family Force 5")
        #self.ultimateList.SetStringItem(2, 1, "III")
        #self.ultimateList.SetStringItem(2, 2, "Crunk")

        self.ultimateList.SetColumnWidth(0, 500)
        self.ultimateList.SetColumnWidth(1, 300)
        self.ultimateList.SetItemSpacing(10)
        #self.ultimateList.SetColumnWidth(2, 100)

        #item = self.ultimateList.GetItem(1, 1)
        #self.gauge = wx.Gauge(self.ultimateList, -1, size=(300,20),style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        #self.gauge.SetValue(20)
        #item.SetWindow(self.gauge)
        #self.ultimateList.SetItem(item)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ultimateList, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)



########################################################################
class TestFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MvP UltimateListCtrl Demo")
        panel = TestPanel(self)
        self.SetSize((800,500))
        self.Centre()
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()