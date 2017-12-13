# coding=utf-8
import wx
import os
from ui.spliterwindowtest import newframe

if __name__ == '__main__':
    newapp=wx.App(False)
    #启动画面
    #登录对话框
    #主框架
    print os.getcwd()
    frame=newframe()
    frame.Show()
    newapp.MainLoop()