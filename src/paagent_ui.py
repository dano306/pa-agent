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
