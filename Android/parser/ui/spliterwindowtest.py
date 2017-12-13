#-*- coding=utf-8 -*-
import wx
import wx.lib.buttons as buttons
import lang.lang
import os

def getHomePath():
    if os.environ['HOME']:
        return os.environ['HOME']
    if os.path.expandvars('$HOME'):
        return os.path.expandvars('$HOME')
    if os.path.expanduser('~'):
        return os.path.expanduser('~')

class AppStatusBar(wx.StatusBar):
    __info__= {
        "info": "images/info.png",
        "success": "images/success.png",
        "error": "images/error.png"
    }
    __Target_Field=1

    def __init__(self, parent, level='info', str=''):
        wx.StatusBar.__init__(self, parent, -1)

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
        image = wx.Bitmap(self.__getStateImage(), wx.BITMAP_TYPE_PNG)
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

        bm_new = wx.Bitmap("images/new.png", wx.BITMAP_TYPE_PNG)
        self.AddLabelTool(self.TOOL_NEW, "New", bm_new, shortHelp="新增任务", longHelp="在任务列表中新增任务")
        self.AddSeparator()

        bm_history = wx.Bitmap("images/clean_history.png", wx.BITMAP_TYPE_PNG)
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

        self.LogText = text = wx.TextCtrl(self, self.__LOG_TEXT_ID, "", size=(300, -1))
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

        # --------------------------------------------------------
        # src
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Src:")
        label.SetHelpText("Please select the project root directory.")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)

        self.SrcText = text = wx.TextCtrl(self, self.__SRC_TEXT_ID, "", size=(300, -1))
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
                defaultDir=getHomePath(),
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
class newframe(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,'Log Analysis Tool',size=(800,500))
        self.Centre()
        self.SetMinSize((800,500))
        self.SetMaxSize((800,500))
        self.mainWindow()
        self.statusbar()
        self.toolbar()

    #主体窗口
    def mainWindow(self):
        self.mw=wx.SplitterWindow(self,style=wx.SP_NOSASH|wx.SP_NOBORDER)
        self.panel1=wx.Panel(self.mw,-1,style=wx.SUNKEN_BORDER)
        #self.panel1.SetBackgroundColour('#5bb686')

        self.finished_sp = wx.SplitterWindow(self.mw, style=wx.SP_LIVE_UPDATE)
        self.finished_sp_p1 = wx.Panel(self.finished_sp, -1, style=wx.SUNKEN_BORDER)
        self.finished_sp_p2 =wx.Panel(self.finished_sp, -1, style=wx.SUNKEN_BORDER)
        #self.finished_sp_p1.SetBackgroundColour('#5bb686')
        #self.finished_sp_p2.SetBackgroundColour('#5bb686')

        self.finished_sp.SplitHorizontally(self.finished_sp_p1, self.finished_sp_p2, 300)
        self.finished_sp.SetMinimumPaneSize(200)

        self.mw.SplitVertically(self.panel1,self.finished_sp,300)
        self.mw.SetMinimumPaneSize(300)

        #newTask = wx.Bitmap("images/new.png", wx.BITMAP_TYPE_PNG)
        #self.chooseLogButton = wx.BitmapButton(self.panel1,10,newTask,
        #                                 pos=(100, 150),size=(150,150))

    #状态栏
    def statusbar(self):
        self.sb= AppStatusBar(self)
        self.SetStatusBar(self.sb)

    #工具栏
    def toolbar(self):
        self.tb = AppToolBar(self)
        self.SetToolBar(self.tb)
        self.tb.SetOnToolClicked(self.__OnToolBarItemClick)

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

    #状态栏坐标显示
    # def OnMotion(self,event):
    #     self.statusbar.SetStatusText(u'光标坐标:  '+str(event.GetPositionTuple()),0)
    # #菜单栏
    # def menubar(self):
    #     menubar=wx.MenuBar()
    #     menu1=wx.Menu()
    #     menu2=wx.Menu()
    #     menu3=wx.Menu()
    #     menubar.Append(menu1,u'文件')
    #     menubar.Append(menu2,u'设置')
    #     menubar.Append(menu3,u'退出')
    #     self.SetMenuBar(menubar)
    # #panel1按钮数据
    # def buttondata(self):
    #     return [['./pic/homepage.png',u'主页'],
    #            ['./pic/lock.png',u'个人人密码管理助手'],
    #            ['./pic/diary.png',u'日记每一天']]
    # #panel1按钮创建
    # def buttoncreate(self,index):
    #     pic=wx.Image(self.buttondata()[index][0],wx.BITMAP_TYPE_PNG).Scale(80,80).ConvertToBitmap()
    #     self.button=buttons.GenBitmapButton(self.panel1,-1,pic,size=(150,120))
    #     self.button.SetBezelWidth(7)
    #     self.button.SetBackgroundColour('CORAL')
    #     self.button.SetToolTipString(self.buttondata()[index][1])
    #     return self.button
    # #panel1按钮添加
    # def panel1buttonadd(self):
    #     self.button1=self.buttoncreate(0)
    #     self.button2=self.buttoncreate(1)
    #     self.button3=self.buttoncreate(2)
    #     sizer = wx.FlexGridSizer( rows=0,cols=1, hgap=5, vgap=5)
    #     sizer.Add(self.button1,0,wx.EXPAND)
    #     sizer.Add(self.button2,0,wx.EXPAND)
    #     sizer.Add(self.button3,0,wx.EXPAND)
    #     sizer.AddGrowableCol(0, proportion=1)
    #     sizer.Layout()
    #     self.panel1.SetSizer(sizer)
    #     self.panel1.Fit()
    # #按钮事件绑定
    # def panel1buttonbind(self):
    #     self.Bind(wx.EVT_BUTTON,self.initindex,self.button1)
    #     self.Bind(wx.EVT_BUTTON,self.KEYhandler,self.button2)
    #     self.Bind(wx.EVT_BUTTON,self.RIJIhandler,self.button3)
    # #自定义光标
    # def cursorinit(self):
    #     cursorpic=wx.Image('./pic/cursor.png',wx.BITMAP_TYPE_PNG)
    #     self.cursor=wx.CursorFromImage(cursorpic)
    #     self.SetCursor(self.cursor)
    # #关闭index定时器
    # def Shutdowntimer(self):
    #     try:
    #         self.index.timer.Stop()
    #         del self.index.timer
    #     except:
    #         pass

if __name__ == '__main__':
    newapp=wx.App(False)
    #启动画面
    #登录对话框
    #主框架
    frame=newframe()
    frame.Show()
    newapp.MainLoop()