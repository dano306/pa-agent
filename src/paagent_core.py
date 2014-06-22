#-*- coding: utf8 -*-

#python安装目录下的 Lib\site-packages\sitecustomize.py
#引入它的目的是，设置当前python运行环境的默认字符集是utf8
import sitecustomize

import wx
import paagent_ui


class   CPaagentApp(wx.App):

    EVT_UPDATETHREAD_ID   = wx.NewId()
    
    class UpdateThreadEvent(wx.PyEvent):
        def __init__(self, data):
            """Init Result Event."""
            wx.PyEvent.__init__(self)
            self.SetEventType(CPaagentApp.EVT_UPDATETHREAD_ID)
            self.data = data

    def OnInit(self):
        self.cfgFile = None    #存在配置文件对象
        self.updateThread = None
        self.isOnDestroy = [False]

        self.dlg = paagent_ui.CPaagentDlg(None, -1, 'pa-agent', size=(300, 280))
        self.tray = paagent_ui.CPaagentTrayIcon()
        
        #控件初始值的填充(与UI没有十分明确的界限，但不妨，视情况而调整)
        self.InitDefaultValue()
        
        #注册所有事件
        self.RegisterEventHandle()
        
        #全部准备完成，进入显示阶段
        self.dlg.Show()
        self.SetTopWindow(self.dlg)
        return True

    def InitDefaultValue(self):
        pass

    def RegisterEventHandle(self):
        
        #注册dialog的事件
        self.dlg.Bind(wx.EVT_CHAR_HOOK, self.OnEvtCharHook)
        self.dlg.Bind(wx.EVT_ICONIZE, self.OnIconize)
        self.dlg.Bind(wx.EVT_CLOSE, self.OnDestroy)

        #注册tray的事件
        self.tray.Bind(wx.EVT_TASKBAR_LEFT_UP, self.OnTaskBarActivate)
        self.tray.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=self.tray.TBMENU_CLOSE)


    def OnEvtCharHook(self, evt):
        if evt.KeyCode == wx.WXK_ESCAPE :
            self.dlg.Iconize()
            self.dlg.Hide()
        else :
            #print 'this is not escape key'
            evt.Skip()

    def OnIconize(self, evt):
        self.dlg.Iconize()
        self.dlg.Hide()

    def OnDestroy(self, evt):
        
        self.isOnDestroy[0] = True
        self.tray.RemoveIcon()
        self.dlg.Destroy()
        #必须有这一句调用，win7的任务管理器里，exe进程才会消失，否则，程序退出了但进程还在，一直占用着资源
        wx.GetApp().Exit()

    def OnTaskBarActivate(self, evt):
        #self.OnTrayShow_Normal()
        if self.dlg.IsIconized():
            self.dlg.Restore()
            self.dlg.Show()
            #下面这一句，使得对话窗显示到最前端
            self.dlg.Raise()
        else:
            self.dlg.Iconize()
            self.dlg.Hide()

    def OnTaskBarClose(self, evt):
        self.tray.RemoveIcon()                   #这一步可以取消系统托盘区的图标，否则程序退出后图标一直还在
        self.dlg.Close()
        wx.GetApp().Exit()

if __name__ == '__main__' :
    app = CPaagentApp()
    app.MainLoop()
    app.ExitMainLoop()
