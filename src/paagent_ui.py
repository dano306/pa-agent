#-*- coding: utf8 -*-

import wx
import wx.lib.agw.hyperlink as hl

class CPaagentDlg(wx.Dialog):

    ABOUT_INFO_PER_LINE = ur'''关于pa-agent(1.0)：
pa-agent是一款小巧的网络工具，提高对国外网站的访问质量；
pa-agent是开源项目，承诺100%不窥探用户隐私，请您放心使用
'''
    
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        #=======================================================================
        # self.msg_db_info = None
        # self.PrepareDb()
        #=======================================================================

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # This extra style can be set after the UI object has been created.
        if 'wxMac' in wx.PlatformInfo and useMetal:
            self.SetExtraStyle(wx.DIALOG_EX_METAL)


        self.CreateUI()

        #=======================================================================
        # self.Bind(wx.EVT_CHAR_HOOK, self.OnEvtCharHook)
        # self.Bind(wx.EVT_CLOSE, self.OnDestroy)
        # self.Bind(wx.EVT_ICONIZE, self.OnIconize)
        #=======================================================================

    def CreateButtonArea(self):
        '''@return is a sizer'''
        
        ret_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnNormal = wx.ToggleButton(self, -1, u"正常访问")
        ret_sizer.Add(self.btnNormal, flag = wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        self.btnOptimize = wx.ToggleButton(self, -1, u"优化访问")
        ret_sizer.Add(self.btnOptimize, flag = wx.ALIGN_RIGHT | wx.RIGHT, border=10)        
        
        return ret_sizer

    def CreateAboutArea(self):
        '''@return is a sizer'''
        
        ret_sizer = wx.BoxSizer(wx.VERTICAL)
        
        #如果self.aboutInfo之后再没有其它控件：
        #不设置size，或size[1] < 某个值(随布局改变，数值不一样)，多行显示都不完整；
        #但是，size[1] > 某个值后，设置再大的值，也只是多行显示完整，但没有多出来的空间
        #如果self.aboutInfo之后有其它控件，size参数都可以不指定了
        self.aboutInfo = wx.StaticText(self, -1, CPaagentDlg.ABOUT_INFO_PER_LINE)
        ret_sizer.Add(self.aboutInfo, flag = wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, border=10)
        
        project_hl = hl.HyperLinkCtrl(self, -1, "了解更多信息，请访问项目主页",
                                        URL="https://github.com/dano306/pa-agent")
        ret_sizer.Add(project_hl, 0, wx.ALL, 10)
        
        return ret_sizer

    def CreateSettingArea(self):
        pass


    def CreateUI(self):
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 20)))    #纯粹增加边距
        topsizer.Add(self.CreateButtonArea(), flag = wx.ALIGN_CENTER_HORIZONTAL)
        
        topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 40)))    #纯粹增加边距
        wx.StaticLine(self, -1, pos=(0,70), size=(300,1), style=wx.LI_VERTICAL)

        topsizer.Add(self.CreateAboutArea())

        #topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 20)))    #纯粹增加边距
        #final
        self.SetSizer(topsizer)


class   CPaagentTrayIcon(wx.TaskBarIcon):

    def __init__(self):
        wx.TaskBarIcon.__init__(self)

        self.TBMENU_RESTORE = wx.NewId()
        self.TBMENU_CLOSE   = wx.NewId()
        
        self.iconNormal = wx.Icon(ur'..\resource\chain_direct.ico', wx.BITMAP_TYPE_ICO)
        self.iconMsg = wx.Icon(ur'..\resource\chain_direct.ico', wx.BITMAP_TYPE_ICO)
        self.OnTrayShow_Normal()
        
#        self.imgidx = 1

        self.menu = self.CreatePopupMenu()

        # bind some events
        #self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.OnTaskBarActivate)
        #self.Bind(wx.EVT_MENU, self.OnTaskBarActivate, id=self.TBMENU_RESTORE)
        #self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.TBMENU_CLOSE)

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.TBMENU_RESTORE, u'显示主窗口')
        menu.Append(self.TBMENU_CLOSE, u'退出')
#        menu.AppendSeparator()

        return menu

    def OnTrayShow_Msg(self):
        self.SetIcon(self.iconMsg, u'您有新的消息，请及时查收')

    def OnTrayShow_Normal(self):
        self.SetIcon(self.iconNormal, u'pa-agent')

    def OnTaskBarActivate(self, evt):
        self.OnTrayShow_Normal()
        if self.frame.IsIconized():
            self.frame.Restore()
            self.frame.Show()
            #下面这一句，使得对话窗显示到最前端
            self.frame.Raise()
        else:
            self.frame.Iconize()
            self.frame.Hide()

    def OnTaskBarClose(self, evt):
        #自行删除图标，再调用上级的Close；或调用上级的另一个接口，由上级负责删除托盘图标，都可以。
        #出于事件通知完整性的考虑，自行删除图标，再将退出事件通知上级，应该是比较不错的做法
        
        self.RemoveIcon()                   #这一步可以取消系统托盘区的图标，否则程序退出后图标一直还在
        #wx.CallAfter(self.frame.Close)      #直接close了，没有机会响应其它工作
        wx.CallAfter(self.frame.OnExit2)    #包装了另一个接口，它做了该做的事情后，再调用Close退出程序
