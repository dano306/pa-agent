#-*- coding: utf8 -*-

import wx
import wx.lib.agw.hyperlink as hl

class CPaagentDlg(wx.Dialog):

    ABOUT_INFO_PER_LINE = ur'''关于pa-agent(1.0)：
pa-agent是一款小巧的网络工具，提高对国外网站的访问质量；
pa-agent是开源项目，承诺100%不窥探用户隐私，请您放心使用。
'''
    
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX ,
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
        #增加了CreateButtonArea之后，必须指定dialog的高，及aboutInfo的高，才能够正常显示了。
        self.aboutInfo = wx.StaticText(self, -1, CPaagentDlg.ABOUT_INFO_PER_LINE, size=(-1, 90))
        ret_sizer.Add(self.aboutInfo, flag = wx.ALIGN_LEFT | wx.LEFT | wx.RIGHT, border=10)
        
        project_hl = hl.HyperLinkCtrl(self, -1, "了解更多信息，请访问项目主页",
                                        URL="https://github.com/dano306/pa-agent")
        ret_sizer.Add(project_hl, 0, wx.ALL, 10)
        
        return ret_sizer

    def CreateSettingArea(self):

        ret_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btnAutoRun = wx.ToggleButton(self, -1, u"开机运行")
        ret_sizer.Add(self.btnAutoRun, flag = wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        self.btnAutoUpdate = wx.ToggleButton(self, -1, u"自动更新")
        ret_sizer.Add(self.btnAutoUpdate, flag = wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        
        return ret_sizer


    def CreateUI(self):
        
        topsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 10)))    #纯粹增加边距
        topsizer.Add(self.CreateButtonArea(), flag = wx.ALIGN_CENTER_HORIZONTAL)
        
        wx.StaticLine(self, -1, pos=(0,50), size=(300,1), style=wx.LI_VERTICAL)
        topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 20)))    #纯粹增加边距
        topsizer.Add(self.CreateSettingArea(), flag = wx.ALIGN_CENTER_HORIZONTAL)

        wx.StaticLine(self, -1, pos=(0,100), size=(300,1), style=wx.LI_VERTICAL)
        topsizer.Add(wx.StaticText(self, -1, "", size=(-1, 25)))    #纯粹增加边距
        topsizer.Add(self.CreateAboutArea())
        
        #final
        self.SetSizer(topsizer)


class   CPaagentTrayIcon(wx.TaskBarIcon):

    def __init__(self):
        wx.TaskBarIcon.__init__(self)

        self.TBMENU_CLOSE   = wx.NewId()
        
        self.iconNormal = wx.Icon(ur'..\resource\chain_bridge.ico', wx.BITMAP_TYPE_ICO)
        self.iconMsg = wx.Icon(ur'..\resource\chain_direct.ico', wx.BITMAP_TYPE_ICO)
        self.OnTrayShow_Normal()

        self.menu = self.CreatePopupMenu()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        menu.Append(self.TBMENU_CLOSE, u'退出')
#        menu.AppendSeparator()

        return menu

    def OnTrayShow_Msg(self):
        self.SetIcon(self.iconMsg, u'您有新的消息，请及时查收')

    def OnTrayShow_Normal(self):
        self.SetIcon(self.iconNormal, u'pa-agent')
