import wx
from connection import Connection
from window.connectdialog import ConnectDialog
from window.prefseditor import PrefsEditor
from window.worldslist import WorldsList
from window.debugmcp import DebugMCP

import prefs
class Main(wx.Frame):
    #use WxMOO::Editor

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.status_bar = self.CreateStatusBar()

        self.buildMenu()

        self.addEvents()

        self.about_info = None
        self.connect_dialog = None
        self.prefs_editor = None
        self.worlds_list = None
        self.debug_mcp = None

        h = 600
        w = 800
        if prefs.get('save_window_size'):
            if prefs.get('window_width'):  w = int(prefs.get('window_width'))
            if prefs.get('window_height'): h = int(prefs.get('window_height'))
        self.SetSize((w, h))

        # TODO - don't connect until we ask for it.
        # TODO - probably want a tabbed interface for multiple connections
        # TODO - "on attempted connect, create a new tab, and populate with connection poop"
        self.tabs = wx.Notebook(self)

        self.sizer = wx.BoxSizer( wx.VERTICAL )
        self.sizer.Add(self.tabs, True, wx.ALL|wx.GROW)
        self.SetSizer(self.sizer)

        self.connection = Connection(self)
        # TODO - don't connect until we ask for it.
        self.connection.connect('hayseed.net',7777)
        splitter = self.connection.splitter

        self.tabs.AddPage(splitter, 'Hayseed')
        self.connection.input_pane.SetFocus()

    def buildMenu(self):
        WorldsMenu = wx.Menu()
        Worlds_worlds  = WorldsMenu.Append(-1, "&Worlds...",  "Browse list of worlds")
        Worlds_connect = WorldsMenu.Append(-1, "&Connect...", "Connect to a host and port")
        Worlds_close   = WorldsMenu.Append(wx.ID_CLOSE)
        WorldsMenu.AppendSeparator()
        Worlds_reconnect = WorldsMenu.Append(-1, "&Reconnect", "Close and re-open the current connection")
        Worlds_quit      = WorldsMenu.Append(wx.ID_EXIT)

        EditMenu = wx.Menu()
        Edit_cut   = EditMenu.Append(wx.ID_CUT)
        Edit_copy  = EditMenu.Append(wx.ID_COPY)
        Edit_paste = EditMenu.Append(wx.ID_PASTE)

        PrefsMenu = wx.Menu()
        Prefs_prefs = PrefsMenu.Append(wx.ID_PREFERENCES)

        WindowMenu = wx.Menu()
        Window_debugmcp = WindowMenu.Append(-1, "&Debug MCP", "")

        HelpMenu = wx.Menu()
        Help_help  = HelpMenu.Append(wx.ID_HELP)
        Help_about = HelpMenu.Append(wx.ID_ABOUT)

        MenuBar = wx.MenuBar()
        MenuBar.Append(WorldsMenu, "&Worlds")
        MenuBar.Append(EditMenu, "&Edit")
        MenuBar.Append(PrefsMenu, "&Preferences")
        MenuBar.Append(WindowMenu, "Windows")
        MenuBar.Append(HelpMenu, "&Help")

        self.SetMenuBar(MenuBar)

        # MENUBAR EVENTS
        self.Bind(wx.EVT_MENU, self.showWorldsList,      Worlds_worlds    )
        self.Bind(wx.EVT_MENU, self.showConnectDialog,   Worlds_connect   )
        self.Bind(wx.EVT_MENU, self.closeConnection,     Worlds_close     )
        self.Bind(wx.EVT_MENU, self.reconnectConnection, Worlds_reconnect )
        self.Bind(wx.EVT_MENU, self.quitApplication,     Worlds_quit      )

        self.Bind(wx.EVT_MENU, self.handleCut,   Edit_cut   )
        self.Bind(wx.EVT_MENU, self.handleCopy,  Edit_copy  )
        self.Bind(wx.EVT_MENU, self.handlePaste, Edit_paste )

        self.Bind(wx.EVT_MENU, self.showPrefsEditor, Prefs_prefs )

        self.Bind(wx.EVT_MENU, self.toggleDebugMCP, Window_debugmcp )

        self.Bind(wx.EVT_MENU, self.showHelp,     Help_help  )
        self.Bind(wx.EVT_MENU, self.showAboutBox, Help_about )

    def addEvents(self):
        return
        # TODO - this makes the output pane 1x1 upper left.  hrmn.
        #self.Bind(wx.EVT_SIZE, self.onSize)

    def closeConnection(self, evt):
        self.connection.Close()

    def reconnectConnection(self, evt):
        self.connection.reconnect()

    def onSize(self, evt):
        if prefs.get('save_window_size'):
            size = self.GetSize()
            prefs.set('window_width',  str(size.GetWidth()))
            prefs.set('window_height', str(size.GetHeight()))

    def handleCopy(self, evt):
        if   (self.output_pane.HasSelection()): self.output_pane.Copy()
        elif (self.input_pane .HasSelection()): self.input_pane .Copy()

    def handleCut(self, evt):
        self.input_pane.Cut

    def handlePaste(self, evt):
        self.input_pane.Paste

### DIALOGS AND SUBWINDOWS

    def showWorldsList(self, evt):
        if self.worlds_list is None: self.worlds_list = WorldsList(self)
        self.worlds_list.Show()

    def showConnectDialog(self, evt):
        if self.connect_dialog is None: self.connect_dialog = ConnectDialog(self)
        self.connect_dialog.Show()

    def showPrefsEditor(self, evt):
        if self.prefs_editor is None: self.prefs_editor = PrefsEditor(self)
        self.prefs_editor.Show()
        pass

    def toggleDebugMCP(self, evt):
        if self.debug_mcp is None: self.debug_mcp = DebugMCP(self)
        self.debug_mcp.toggle_visible()

    def showHelp(self, evt):
        pass

# TODO - WxMOO::Window::About
    def showAboutBox(self, evt):
        if self.about_info is None:
             info = wx.AboutDialogInfo()
             info.AddDeveloper('R Pickett (emerson@hayseed.net)')
             info.SetCopyright('(c) 2013-2016')
             info.SetWebSite('http://github.com/emersonrp/wxpymoo')
             info.SetName('wxpymoo')
             info.SetVersion('0.1')
             self.about_info = info
        wx.AboutBox(self.about_info)

    def quitApplication(self, evt):
        self.closeConnection
        self.Close(True)
