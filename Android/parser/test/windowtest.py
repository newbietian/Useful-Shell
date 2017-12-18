# coding=utf-8
import os
import wx

from ui.test.spliterwindowtest import newframe

if __name__ == '__main__':
    newapp=wx.App(False)
    #启动画面
    #登录对话框
    #主框架
    print os.getcwd()
    frame=newframe()
    frame.Show()
    newapp.MainLoop()