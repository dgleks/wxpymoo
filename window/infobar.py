import wx

import prefs
class InfoBar(wx.InfoBar):

    def __init__(self, parent):
        wx.InfoBar.__init__(self, parent)
        self.SetShowHideEffects(wx.SHOW_EFFECT_NONE, wx.SHOW_EFFECT_NONE)

        self.buttons = {}

    def InfoBarMessage(self, message, buttons = [], style = wx.ICON_INFORMATION):
        for b in buttons:
            # This whole hoop-jumping is because self.AddButton doesn't return the button.
            b['id'] = wx.NewIdRef()
            self.AddButton(b['id'], b['name'])
            self.Bind(wx.PyEventBinder(wx.wxEVT_COMMAND_BUTTON_CLICKED), self.doButton)
            self.buttons[b['name']] = b

        super().ShowMessage(message, style)

    def doButton(self, evt):
        name = evt.GetEventObject().GetLabel()
        func = self.buttons[name]['callback']
        func(evt)

    def Dismiss(self, evt = None):

        for _, b in self.buttons.items():
            self.Unbind(wx.PyEventBinder(wx.wxEVT_COMMAND_BUTTON_CLICKED))
            self.RemoveButton(b['id'])

        self.buttons = {}
        super().Dismiss()
