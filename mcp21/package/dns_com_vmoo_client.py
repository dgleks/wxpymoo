import re
import mcp21.core as mcp21
import mcp21.registry as registry
from mcp21.package import MCPPackageBase
from window.outputpane import EVT_ROW_COL_CHANGED

class MCPPackage(MCPPackageBase):
    def __init__(self, conn):
        MCPPackageBase.__init__(self, conn)

        self.package = 'dns-com-vmoo-client'
        self.min     = '1.0'
        self.max     = '1.0'

        registry.register(self, ['dns-com-vmoo-client-disconnect'])

    def dispatch(self, msg):
        if msg.message == 'dns-com-vmoo-client-disconnect': self.do_disconnect(msg)

    def Initialize(self):
        self.connection.output_pane.Bind(EVT_ROW_COL_CHANGED, self.send_screensize)

    def do_disconnect(self, msg):
        mcp21.debug("Got a disconnect from dns-com-vmoo-client")

    def mcp_negotiate_end(self):
        self.send_info()
        self.send_screensize()

    def send_info(self):
        # TODO - actual versioning please
        mcp21.server_notify(
            'dns-com-vmoo-client-info', {
                'name'             : 'wxpymoo',
                'text-version'     : 'pre-alpha',
                'internal-version' : '1',

            }
        )

    def send_screensize(self, msg = None):
        mcp21.server_notify(
            'dns-com-vmoo-client-screensize', {
                'cols' : str(self.connection.output_pane.cols),
                'rows' : str(self.connection.output_pane.rows),
            }
        )