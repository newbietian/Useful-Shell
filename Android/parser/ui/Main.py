# -*- coding: UTF-8 -*-
import wx
import os
import time
from multiprocessing import Process
from wx.lib.agw import ultimatelistctrl as ULC

from webserver import PythonWebServer
from images import images as image
from presenter.presenter import Presenter
import lang.lang as LANG
import tool.tools as tool

USE_GENERIC = 0

if USE_GENERIC:
    from wx.lib.stattext import GenStaticText as StaticText
else:
    StaticText = wx.StaticText

SPLASH_WIDTH=400
SPLASH_HEIGHT=250
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500

#---------------------------------------------------------------------------

__sWebProcess=None

def opj(path):
    """Convert paths to the platform-specific separator"""
    st = apply(os.path.join, tuple(path.split('/')))
    # HACK: on Linux, a leading / gets lost...
    if path.startswith('/'):
        st = '/' + st
    return st

def asyncStartWebServer(start_callback, stop_callback):
    global __sWebProcess
    if __sWebProcess and __sWebProcess.is_alive():
        print "__sWebProcess is running"
        return False
    __sWebProcess = Process(target=__asyncStartWebServer, args=(start_callback, stop_callback))
    __sWebProcess.daemon = True
    __sWebProcess.start()

def __asyncStartWebServer(start_callback=None, stop_callback=None):
    PythonWebServer.addServerStartListener(start_callback)
    PythonWebServer.addServerStopedListener(stop_callback)
    PythonWebServer.startServer()

# ---------------------------------------------------------------------------

def main():
    try:
        demoPath = os.path.dirname(__file__)
        os.chdir(demoPath)
    except:
        pass
    app = Application(False)
    app.MainLoop()

#---------------------------------------------------------------------------

class Application(wx.App):
    def OnInit(self):
        self.SetAppName(LANG.app_name)
        splash = SplashScreen()
        splash.Show()
        return True

# ---------------------------------------------------------------------------

class SplashScreen(wx.SplashScreen):
    global __sWebProcess
    def __init__(self):
        showtime = 100
        wx.SplashScreen.__init__(self, image.app_splash.GetBitmap(),
                                 wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT,
                                 showtime, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.fc = wx.FutureCall(showtime, self.ShowMain)

        # register service callback
        asyncStartWebServer(self.__onWebServerStarted, self.__onWebServerStopped)

    # TODO TypeError: can't pickle PySwigObject objects in windows
    def __onWebServerStarted(self):
        print "Server Started"

    # TODO TypeError: can't pickle PySwigObject objects in windows
    def __onWebServerStopped(self, reason):
        global __sWebProcess
        print "Server stopped: ", reason
        if reason == 0x01:
            pass
        elif reason == 0x02:
            print PythonWebServer.__STOP_REASON__[reason]
            pass
        elif reason == 0x03:
            pass
        # if __sWebProcess and __sWebProcess.is_alive:
        #     print "__sWebProcess.terminate()"
        #     __sWebProcess.terminate()

    def OnClose(self, evt):
        # Make sure the default handler runs too so this window gets
        # destroyed
        evt.Skip()
        self.Hide()

        # if the timer is still running then go ahead and show the
        # main frame now
        if self.fc.IsRunning():
            self.fc.Stop()
            self.ShowMain()

    def ShowMain(self):
        frame = MainWindow(None)
        frame.Show()
        if self.fc.IsRunning():
            self.Raise()

#---------------------------------------------------------------------------


class AppStatusBar(wx.StatusBar):
    __Target_Field=1

    def __init__(self, parent, level='info', str=''):
        wx.StatusBar.__init__(self, parent, -1)

        self.__info__= {
            "info": image.web_service_info.GetBitmap(),
            "success": image.web_service_success.GetBitmap(),
            "error": image.web_service_error.GetBitmap()
        }
        self.state = level
        self.parent = parent
        self.string = str

        # This status bar has one field
        self.SetFieldsCount(2)
        self.SetStatusWidths([-22,-1])
        self.sizeChanged = False
        self.Bind(wx.EVT_SIZE, self.__OnSize)
        self.Bind(wx.EVT_IDLE, self.__OnIdle)

        self.SetLevel(level=level)
        self.SetString(string=str)

        # set the initial position of the message
        self.__Reposition()
        self.Bind(wx.EVT_ENTER_WINDOW, self.__OnEnterWindow)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.__OnLevelWindow)

    def SetLevel(self, level):
        self.state = level
        image = self.__getStateImage()
        #self.stateIcon = wx.BitmapButton(self, -1, image ,(image.GetWidth(), image.GetHeight()))
        self.stateIcon = wx.StaticBitmap(self, -1, image)
        self.__Reposition()
        return self

    def SetString(self,string):
        self.string = self.__getStateString(string)
        self.SetStatusText(self.string, 0)
        return self

    def GetLevel(self):
        return self.state

    def __getStateImage(self):
        return self.__info__[self.state]

    def __getStateString(self, str):
        #return "        " + str
        return str

    def __OnSize(self, evt):
        self.__Reposition()  # for normal size events

        # Set a flag so the idle time handler will also do the repositioning.
        # It is done this way to get around a buglet where GetFieldRect is not
        # accurate during the EVT_SIZE resulting from a frame maximize.
        self.sizeChanged = True

    def __OnIdle(self, evt):
        if self.sizeChanged:
            self.__Reposition()

    # reposition the checkbox
    def __Reposition(self):
        rect = self.GetFieldRect(self.__Target_Field)
        self.stateIcon.SetPosition((rect.x + 6, rect.y + 3))
        self.stateIcon.SetSize((rect.height - 4, rect.height - 4))
        self.sizeChanged = False

    def __OnEnterWindow(self,evt):
        print "__OnEnterWindow"
        #self.SetToolTipString("jahahahahahah")
        #self.stateDetail = wx.Panel(self.parent, -1, pos=(10, 400), size=(200,40))
        #self.stateDetail.SetBackgroundColour('yellow')

    def __OnLevelWindow(self, evt):
        print "__OnLevelWindow"
        #self.stateDetail.Hide()

# -----------------------------------------------------------------------------------------

class AppShowWindow(wx.SplitterWindow):
    def __init__(self, parent, ID):
        wx.SplitterWindow.__init__(self, parent, ID, style=wx.SP_LIVE_UPDATE)


# ------------------------------------------------------------------------------------------

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
        info._text = LANG.task_log_path
        self.ulc.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = ULC.ULC_FORMAT_LEFT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_HYPERTEXT
        info._text = LANG.task_status
        self.ulc.InsertColumnInfo(1, info)

        self.ulc.SetColumnWidth(0, 600)
        self.ulc.SetColumnWidth(1, 200)

        self.ulc.InsertImageStringItem(0, "haha", 0)
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
# ------------------------------------------------------------------------------------------

class UlcTaskDoneList(wx.Panel):
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
        info._text = LANG.finished
        self.ulc.InsertColumnInfo(0, info)

        info = ULC.UltimateListItem()
        info._format = ULC.ULC_FORMAT_LEFT
        info._mask = wx.LIST_MASK_TEXT | wx.LIST_MASK_IMAGE | wx.LIST_MASK_FORMAT | ULC.ULC_MASK_HYPERTEXT
        self.ulc.InsertColumnInfo(1, info)

        self.ulc.SetColumnWidth(0, 600)
        self.ulc.SetColumnWidth(1, 200)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.ulc, 1, flag=wx.EXPAND)
        self.SetSizer(sizer)

#-------------------------------------------------------------------------------------------

class AppToolBar(wx.ToolBar):
    __TBFLAGS__ = (wx.TB_HORIZONTAL
               | wx.NO_BORDER
               | wx.TB_FLAT
               # | wx.TB_TEXT
               # | wx.TB_HORZ_LAYOUT
               )
    TOOL_NEW=10
    TOOL_CLEAN=20
    TOOL_HELP=30
    def __init__(self, parent):
        wx.ToolBar.__init__(self, parent, style=self.__TBFLAGS__)

        tsize = (24, 24)
        bm_help = wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, tsize)
        self.SetToolBitmapSize(tsize)

        bm_new = image.action_new.GetBitmap()
        self.AddLabelTool(self.TOOL_NEW, "New", bm_new, shortHelp="新增任务", longHelp="在任务列表中新增任务")
        self.AddSeparator()

        bm_history = image.action_clean_history.GetBitmap()
        self.AddLabelTool(self.TOOL_CLEAN, "Clean", bm_history, shortHelp="删除历史", longHelp="删除列表中的历史记录")
        self.AddSeparator()

        self.AddLabelTool(self.TOOL_HELP, "Help", bm_help, shortHelp="帮助", longHelp="帮助文档")
        self.AddSeparator()

    def SetOnToolClicked(self, callback):
        self.OnToolClick = callback
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.TOOL_NEW)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.TOOL_CLEAN)
        self.Bind(wx.EVT_TOOL, self.OnToolClick, id=self.TOOL_HELP)

#---------------------------------------------------------------------------------------------

class AppNewTaskDialog(wx.Dialog):
    LogPath=''
    SrcPath=''
    LogChooseType=''

    __LOG_TEXT_ID=0x001
    __LOG_BTN_ID=0x002
    __LOG_CHOOSE_ID=0x003
    __SRC_TEXT_ID=0x010
    __SRC__BTN_ID=0x020

    __WILDCARD = "All files (*.*)|*.*"
    __LOG_FILE_TYPE = ['file', 'dir']

    __STYLE_FILE=__LOG_FILE_TYPE[0]
    __STYLE_DIR=__LOG_FILE_TYPE[1]

    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
    ):
        self.LogPath = ''
        self.SrcPath = ''

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        # --------------------------------------------------------
        # log
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Log:")
        label.SetHelpText("Please select the log file/directory.")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.LogText = text = wx.TextCtrl(self, self.__LOG_TEXT_ID, "", size=(300, -1), style=wx.TE_READONLY)
        self.LogText.Bind(wx.EVT_TEXT, self.__OnLogTextChanged)
        text.SetHelpText("Please select the log file/directory.")
        box.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        ch = wx.Choice(self, self.__LOG_CHOOSE_ID, (100, 50), choices=self.__LOG_FILE_TYPE)
        ch.Bind(wx.EVT_CHOICE, self.__LogTypeChoosed, ch)
        self.LogChooseType = ch.GetStringSelection()

        box.Add(ch, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        bsize=(16,16)
        open = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_TOOLBAR, bsize)
        btn = wx.BitmapButton(self, self.__LOG_BTN_ID, open, size=(40, -1))
        btn.SetHelpText("Please select the log file/directory.")
        btn.Bind(wx.EVT_BUTTON, self.__OnButtonClicked, id=self.__LOG_BTN_ID)

        box.Add(btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # error tip
        self.logErrorTip = wx.StaticText(self, -1, "Log path must be set")
        self.logErrorTip.SetForegroundColour((0xff, 0, 0))

        sizer.Add(self.logErrorTip, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # --------------------------------------------------------
        # src
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Src:")
        label.SetHelpText("Please select the project root directory.")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.SrcText = text = wx.TextCtrl(self, self.__SRC_TEXT_ID, "", size=(300, -1), style=wx.TE_READONLY)
        text.SetHelpText("Please select the project root directory.")
        box.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)

        bsize=(16,16)
        open = wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_TOOLBAR, bsize)
        btn = wx.BitmapButton(self, self.__SRC__BTN_ID, open, size=(40, -1))
        btn.SetHelpText("Please select the log file/directory.")
        btn.Bind(wx.EVT_BUTTON, self.__OnButtonClicked, id=self.__SRC__BTN_ID)
        box.Add(btn, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # --------------------------------------------------------
        # line
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)

        # --------------------------------------------------------
        # cancel and ok button
        btnsizer = wx.StdDialogButtonSizer()

        # if wx.Platform != "__WXMSW__":
        #     btn = wx.ContextHelpButton(self)
        #     btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_OK, "新增")
        btn.Bind(wx.EVT_BUTTON, self.__OnConfirmClicked)
        #btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL,"取消")
        #btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def __OnLogTextChanged(self, env):
        if env.GetString():
            self.logErrorTip.Hide()
        else:
            self.logErrorTip.Show()

    def __OnConfirmClicked(self, env):
        print "clicked"
        if not self.LogPath or self.LogPath == '':
           pass
        else:
            env.Skip()

    def __OnButtonClicked(self,env):
        print "__OnButtonClicked ", env.GetId()
        id = env.GetId()
        if id == self.__LOG_BTN_ID:
            self.LogPath = self.__ChooseFileOrDir("Choose Log Files/Directory",self.LogChooseType)
            self.LogText.SetValue(self.LogPath)
        elif id == self.__SRC__BTN_ID:
            self.SrcPath = self.__ChooseFileOrDir("Choose Src Directory", self.__STYLE_DIR)
            self.SrcText.SetValue(self.SrcPath)

    def __LogTypeChoosed(self,env):
        print "__LogTypeChoose ", env.GetId()
        id = env.GetId()
        if id == self.__LOG_CHOOSE_ID:
            self.LogChooseType=env.GetString()
            print env.GetString()


    def __ChooseFileOrDir(self, message, style):
        path=''
        if style == self.__STYLE_DIR:
            # In this case we include a "New directory" button.
            dlg = wx.DirDialog(self, message,
                               style=wx.DD_DEFAULT_STYLE
                               # | wx.DD_DIR_MUST_EXIST
                               # | wx.DD_CHANGE_DIR
                               )

            # If the user selects OK, then we process the dialog's data.
            # This is done by getting the path data from the dialog - BEFORE
            # we destroy it.
            if dlg.ShowModal() == wx.ID_OK:
                print 'You selected: %s\n' % dlg.GetPath()
                path = dlg.GetPath()

            # Only destroy a dialog after you're done with it.
            dlg.Destroy()
        elif style==self.__STYLE_FILE:
            # Create the dialog. In this case the current directory is forced as the starting
            # directory for the dialog, and no default file name is forced. This can easilly
            # be changed in your program. This is an 'open' dialog, and allows multitple
            # file selections as well.
            #
            # Finally, if the directory is changed in the process of getting files, this
            # dialog is set up to change the current working directory to the path chosen.
            dlg = wx.FileDialog(
                self, message=message,
                defaultDir=tool.getHomePath(),
                defaultFile="",
                wildcard=self.__WILDCARD,
                style=wx.OPEN | wx.CHANGE_DIR # | wx.MULTIPLE
            )

            # Show the dialog and retrieve the user response. If it is the OK response,
            # process the data.
            if dlg.ShowModal() == wx.ID_OK:
                # This returns a Python list of files that were selected.
                print 'You selected: %s\n' % dlg.GetPath()
                path = dlg.GetPath()

            # Destroy the dialog. Don't do this until you are done with it!
            # BAD things can happen otherwise!
            dlg.Destroy()
        return path

#---------------------------------------------------------------------------------------------
#主框架
class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, LANG.app_name, size=(800,500))
        self.Centre()
        self.SetMinSize((800,500))
        self.SetMaxSize((800,500))
        self.mainWindow()
        self.statusbar()
        self.toolbar()
        self.presenter = Presenter(self)

    #主体窗口
    def mainWindow(self):
        self.mWindow = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.ulcTaskPanel = UlcTaskList(self.mWindow)#wx.Panel(self.finished_sp, -1, style=wx.SUNKEN_BORDER)
        self.ulcTaskDonePanel =UlcTaskDoneList(self.mWindow)#wx.Panel(self.finished_sp, -1, style=wx.SUNKEN_BORDER)

        self.mWindow.SplitHorizontally(self.ulcTaskPanel, self.ulcTaskDonePanel, 200)
        self.mWindow.SetMinimumPaneSize(30)

    #状态栏
    def statusbar(self):
        self.sb= AppStatusBar(self)
        self.SetStatusBar(self.sb)

    #工具栏
    def toolbar(self):
        self.tb = AppToolBar(self)
        self.SetToolBar(self.tb)
        self.tb.SetOnToolClicked(self.__OnToolBarItemClick)

    def AddTaskToProcessingList(self):
        #TODO self.ulcTaskPanel.
        pass

    # 工具栏点击处理
    def __OnToolBarItemClick(self, evt):
        print "__OnToolBarItemClick ", evt.GetId()
        id = evt.GetId()
        if id == AppToolBar.TOOL_NEW:
            self.__DoNew()
        elif id == AppToolBar.TOOL_CLEAN:
            self.__DoClean()
        elif id == AppToolBar.TOOL_HELP:
            self.__ShowHelp()

    def __DoNew(self):
        self.__ShowNewDialog()


    def __ShowNewDialog(self):
        dlg = AppNewTaskDialog(self, -1, "Add new task", size=(500, 200),
                         #style=wx.CAPTION | wx.SYSTEM_MENU | wx.THICK_FRAME,
                         style=wx.DEFAULT_DIALOG_STYLE, # & ~wx.CLOSE_BOX,
                         )
        dlg.CenterOnScreen()

        val = dlg.ShowModal()

        if val == wx.ID_OK:
            print "dlg.LogPath %s" % dlg.LogPath
            print "dlg.SrcPath %s" % dlg.SrcPath
            #TODO presenter
            print "You pressed OK\n"
        else:
            print "You pressed Cancel\n"

        dlg.Destroy()

    def __DoClean(self):
        pass

    def __ShowCleanDialog(self):
        pass

    def __ShowHelp(self):
        pass


#---------------------------------------------------------------------------
if __name__ == "__main__":
    print 'current pid is %s' % os.getpid()
    main()