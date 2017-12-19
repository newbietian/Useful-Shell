#coding=utf-8
import wx

class CourseListCtrl(wx.ListCtrl):
    def __init__(self, parent, subDatas, size, id=-1, pos=(0, 0), style=wx.LC_SMALL_ICON):
        wx.ListCtrl.__init__(self, parent, id, pos, size, style)

        self.subDatas = subDatas
        self.InitUI()
        pass
    def InitUI(self):
        il = wx.ImageList(45, 45, True)
        logoBmp = wx.Bitmap(r"D:\book_icon.png", wx.BITMAP_TYPE_PNG)
        il.Add(logoBmp)

        self.AssignImageList(il, wx.IMAGE_LIST_SMALL)
        self.ShowListDatas(self.subDatas)
        pass
    def ShowListDatas(self, datas):
        self.subDatas = datas
        for index in range(len(self.subDatas)):
            subject = self.subDatas[index]
            content = u"科目：{0} 科目介绍：{1}".format(subject.get('name', ''), subject.get('intro', ''))
            self.InsertImageStringItem(index, content, 0)

    def refreshDataShow(self, newDatas):
        self.datas = newDatas
        self.DeleteAllItems()
        self.ShowListDatas(self.datas)
        self.Refresh()
