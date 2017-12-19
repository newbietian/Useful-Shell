#-*- coding=utf-8 -*-
import wx
from wx.lib.agw import ultimatelistctrl as ULC
from ui.images import images as image

########################################################################
class UlcTaskList(wx.Panel):
    """"""

    def AddTask(self, task):
        # self.ulc.InsertImageStringItem(0, "haha", 0)
        # task.log_path
        # task state_
        pass


    def OnItemSelected(self, event):
        self.currentIndex = event.m_itemIndex
        print "OnItemSelected: %s, %s\n" %(self.currentIndex, self.ulc.GetItemText(self.currentIndex))
        if self.ulc.GetPyData(self.currentIndex):
            print ("PYDATA = %s\n" % repr(self.ulc.GetPyData(self.currentIndex)))

        event.Skip()

    def OnHyperTextClicked(self,event):
        print "You click a hypertext"
        self.currentIndex = event.m_itemIndex
        item = self.ulc.GetItem(self.currentIndex, 1)
        if item.GetPyData():
            print ("PYDATA = %s\n" % repr(item.GetPyData()))

        allcount = self.ulc.GetItemCount()
        print allcount

        self.ulc.InsertImageStringItem(allcount,
                                                        "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android",
                                       0)

        event.Skip()
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

        self.il = ULC.PyImageList(20, 20)
        self.il.Add(image.task_process.getBitmap())
        self.il.Add(image.task_start.getBitmap())
        self.il.Add(image.task_waiting.getBitmap())
        self.il.Add(image.task_done.getBitmap())

        self.ulc = ULC.UltimateListCtrl(self, agwStyle=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES)
        self.ulc.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

        self.Bind(ULC.EVT_LIST_ITEM_HYPERLINK, self.OnHyperTextClicked, self.ulc)
        self.Bind(ULC.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.ulc)

        # 参考资料
        # http://xoomer.virgilio.it/infinity77/Phoenix/lib.agw.ultimatelistctrl.UltimateListItem.html#lib.agw.ultimatelistctrl.UltimateListItem
        # 设置第一列的样式
        # 创建一个ULC list item
        info = ULC.UltimateListItem()
        # mask可以出现哪些形式的
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT
        info._format = ULC.ULC_FORMAT_LEFT
        info._text = "已完成"
        self.ulc.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = ULC.ULC_FORMAT_LEFT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_HYPERTEXT
        info._text = ""
        self.ulc.InsertColumnInfo(1, info)

        self.ulc.SetColumnWidth(0, 600)
        self.ulc.SetColumnWidth(1, 200)

        # add a item
        self.ulc.InsertImageStringItem(0, "haha", 0)
        # change item image
        self.ulc.SetItemColumnImage(0, 0, 3)

        #change  item state
        self.ulc.SetStringItem(0,1,"Waiting")

        # set hyper text
        item = self.ulc.GetItem(0, 1)
        item.SetHyperText(True)
        self.ulc.SetItem(item)

        #


        # for i in range(10):
        #     index = self.ulc.InsertImageStringItem(i,
        #                                                     "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android",
        #                                            0)
        #     #self.ultimateList.InsertStringItem(i, "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android")
        #     item = self.ulc.GetItem(i, 1)
        #     if i < 3 :
        #         self.gauge = wx.Gauge(self.ulc, -1, size=(200, 20), style=wx.GA_HORIZONTAL | wx.GA_SMOOTH)
        #         self.gauge.SetValue(20)
        #         item.SetWindow(self.gauge)
        #         self.ulc.SetItem(item)
        #         self.ulc.SetStringItem(i, 1, "99%")
        #     else:
        #         self.ulc.SetStringItem(i, 1, "Waiting...")
        #
        # item = self.ulc.GetItem(5, 1)
        # item.SetHyperText(True)
        # s = "https://www.google.com.hk"
        # item.SetPyData(s)
        # self.ulc.SetItem(item)

        #self.ultimateList.SetStringItem(0, 2, "Rock")

        #self.ultimateList.InsertStringItem(1, "Puffy")
        #self.ultimateList.SetStringItem(1, 1, "Bring It!")
        #self.ultimateList.SetStringItem(1, 2, "Pop")

        #self.ultimateList.InsertStringItem(2, "Family Force 5")
        #self.ultimateList.SetStringItem(2, 1, "III")
        #self.ultimateList.SetStringItem(2, 2, "Crunk")


        #item = self.ultimateList.GetItem(1, 1)
        #self.gauge = wx.Gauge(self.ultimateList, -1, size=(300,20),style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        #self.gauge.SetValue(20)
        #item.SetWindow(self.gauge)
        #self.ultimateList.SetItem(item)


        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ulc, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)



########################################################################
class TestFrame(wx.Frame):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MvP UltimateListCtrl Demo")
        panel = UlcTaskList(self)
        self.SetSize((800,500))
        self.Centre()
        self.Show()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = TestFrame()
    app.MainLoop()