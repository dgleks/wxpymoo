import wx
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver

from window.inputpane import InputPane
from window.outputpane import OutputPane
from mcp21.core import MCPCore
import prefs
from prefs import EVT_PREFS_CHANGED

class ConnectionClient(LineReceiver):
    def lineReceived(self, line):
        self.factory.connection.output_pane.display(line)

    def output(self, line):
        self.sendLine(line.encode('utf-8'))

    def connectionMade(self):
        self.connected = True
        # turn on TCP keepalive if possible
        try:
            self.transport.setTcpKeepAlive(1)
        except AttributeError: pass

        prefs.set('last_world', self.factory.connection.world.get('name'))

    def connectionLost(self, reason):
        self.connected = False

class ConnectionClientFactory(ClientFactory):
    def __init__(self, connection):
        self.connection = connection
        self.protocol   = ConnectionClient

    def buildProtocol(self, addr):
        p = ClientFactory.buildProtocol(self, addr)
        self.connection.input_receiver = p
        return p

    #def clientConnectionFailed(self, connector, reason):
        #print("connection failed:", reason.getErrorMessage())
        #reactor.stop()

    #def clientConnectionLost(self, connector, reason):
        #print('connection lost:', reason.getErrorMessage())
        #reactor.stop()


# the 'connection' contains both the network connection and the i/o ui
class Connection(wx.SplitterWindow):
    def __init__(self, mainwindow):
        wx.SplitterWindow.__init__(self, mainwindow.tabs, style = wx.SP_LIVE_UPDATE)
        self.world          = None
        self.input_receiver = None
        self.debug_mcp      = None

        self.input_pane     = InputPane(self, self)
        self.output_pane    = OutputPane(self, self)

        # these two are set with dns_com_awns_serverinfo but hypothetically
        # -could- come from the saved world also
        self.home_url       = ''
        self.help_url       = ''

        #self.keepalive     = Keepalive(self)
        self.connector = None

        self.SplitHorizontally(self.output_pane, self.input_pane)
        self.SetMinimumPaneSize(self.input_pane.font_size()[1] + 2)

        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.saveSplitterSize )
        self.Bind(wx.EVT_SIZE, self.HandleResize)

        mainwindow.Bind(EVT_PREFS_CHANGED, self.doPrefsChanged)

    def doPrefsChanged(self, evt):
        self.input_pane.restyle_thyself()
        self.output_pane.restyle_thyself()
        evt.Skip()

    def saveSplitterSize(self, evt):
        size = self.GetSize()
        prefs.set('input_height', size.GetHeight() - evt.GetSashPosition())

    def HandleResize(self, evt):
        size = self.GetSize()
        input_height = int(prefs.get('input_height')) or 25
        self.SetSashPosition(size.GetHeight() - input_height, True)
        self.output_pane.ScrollIfAppropriate()

    def ShowMessage(self, message):
        wx.GetApp().GetTopWindow().GetStatusBar().SetStatusText(message)

    def Close(self):
        if self.input_receiver and self.input_receiver.connected:
            self.output_pane.display("wxpymoo: Connection closed.\n");
        # force it again just to be sure
        #self.keepalive.Stop()
        self.connector.disconnect()

    # connection.connect ([host], [port])
    #
    # existing connections will remember their host and port if not supplied here,
    # for ease of reconnect etc.
    def connect(self, world):
        self.world = world
        host =     world.get('host')
        port = int(world.get('port'))
        self.connector = reactor.connectTCP(host, port, ConnectionClientFactory(self))

        self.mcp = MCPCore(self)

        # TODO - 'if world.connection.keepalive'
        #self.keepalive.Start()

    def output(self, stuff):
        self.input_receiver.output(stuff)

    def reconnect(self):
        if self.connector: self.Close()
        self.connect(self.world)

class Keepalive(wx.EvtHandler):
    ######################
    # This is a stupid brute-force keepalive that periodically tickles the
    # connection by sending a single space.  Not magical or brilliant.
    def __init__(self, connection):
        wx.EvtHandler.__init__(self)
        self.connection = connection
        self.timer = wx.Timer()

        self.timer.Bind(wx.EVT_TIMER, self.on_keepalive)

    def Start(self):
        self.timer.Start(60000, False) # 1 minute TODO make this a pref?

    def Stop(self):
        self.timer.Stop()

    def on_keepalive(self, evt):
        # TODO - this is pretty brute-force, innit?
        # This'll likely break on worlds that actually
        # are character-based instead of line-based.
        self.connection.output(" ")
