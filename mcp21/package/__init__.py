import wx

class MCPPackageBase(wx.EvtHandler):
    def __init__(self, mcp):
        wx.EvtHandler.__init__(self)

        self.activated = None
        self.callback = None
        self.max = 0.0
        self.min = 0.0
        self.message = ''
        self.package = ''
        self.mcp = mcp

    def Initialize(self):
        pass

    def mcp_negotiate_end(self):
        pass
