import wx
import wx.richtext as rtc
import prefs
import re
from utility import platform

class BasePane(rtc.RichTextCtrl):

    def __init__(self, parent, connection, style):
        rtc.RichTextCtrl.__init__(self, parent, style)

        self.connection = connection
        self.cols = 0
        self.rows = 0
        self.basic_style = None
        self.fg_colour = ''
        self.bg_colour = ''

        self.Clear()
        self.restyle_thyself()

    def restyle_thyself(self):
        basic_style = rtc.RichTextAttr()
        self.fg_colour = prefs.get('fgcolour')
        self.bg_colour = prefs.get('bgcolour')
        basic_style.SetTextColour      (self.fg_colour)
        basic_style.SetBackgroundColour(self.bg_colour)

        self.SetBackgroundColour(self.bg_colour)
        self.SetBasicStyle(basic_style)
        self.basic_style = basic_style

        font = wx.NullFont
        font.SetNativeFontInfoFromString(prefs.get('font'))
        self.SetFont(font)

        # is there a way to construct a font directly from an InfoString, instead of making
        # a generic one and then overriding it like this?
        font = wx.NullFont
        font.SetNativeFontInfoFromString(prefs.get('output_font'))
        self.SetFont(font)

        # set one character's worth of left margin
        font_width, font_height = self.font_size()
        self.SetMargins((font_width, -1))

        self.update_size()

    def font_size(self):
        font = self.GetFont()

        # suss out how big one character is
        dc = wx.ScreenDC()
        dc.SetFont(font)
        return dc.GetTextExtent('M')

    #### override in subclasses
    def check_for_interesting_keystrokes(self, evt):
        pass

    def update_size(self, evt = None):
        pass
