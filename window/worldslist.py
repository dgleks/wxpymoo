import wx
import wx.html

import prefs
from worlds import worlds
from connection import Connection

import webbrowser

class DescriptionBox(wx.html.HtmlWindow):
    def OnLinkClicked(self, link):
        webbrowser.open(link.GetHref())

conntypes = [ 'Direct', 'SSL', 'SSH Fwd' ]

class WorldsList(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, name = 'Worlds List', style = wx.RESIZE_BORDER)

        self.parent = parent

        worlds_label      = wx.StaticText(self, label = "World:")
        self.world_picker = wx.Choice(self, style     = wx.CB_SORT )

        for world in worlds: self.world_picker.Append(world)

        host_label = wx.StaticText(self, label = "Host:")
        port_label = wx.StaticText(self, label = "Port:")

        self.host = wx.TextCtrl(self)

        # stick port + type into their own boxsizer
        self.port = wx.SpinCtrl(self)
        self.port.SetRange(1, 65535)
        self.port.SetValue(7777)
        self.conntype = wx.Choice(self, choices = conntypes )
        port_sizer = wx.BoxSizer(wx.HORIZONTAL)
        port_sizer.Add(self.port,     1, wx.EXPAND)
        port_sizer.Add([5,5],         0, wx.EXPAND)
        port_sizer.Add(self.conntype, 0, wx.EXPAND)

        username_label = wx.StaticText(self, label = "Username:")
        password_label = wx.StaticText(self, label = "Password:")
        self.username  = wx.TextCtrl(self)
        self.password  = wx.TextCtrl(self, style = wx.TE_PASSWORD)

        self.ssh_username_label = wx.StaticText(self, label = "SSH User:")
        self.ssh_loc_host_label = wx.StaticText(self, label = "SSH Host:")
        self.ssh_username       = wx.TextCtrl(self)
        self.ssh_loc_host       = wx.TextCtrl(self)

        field_sizer = wx.FlexGridSizer(cols = 2, hgap = 5, vgap = 5)
        field_sizer.AddMany([
            (worlds_label           , 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.world_picker      , 0, wx.EXPAND                              , 0),
            (host_label             , 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.host              , 0, wx.EXPAND                              , 0),
            (port_label             , 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (port_sizer             , 0, wx.EXPAND                              , 0),
            (username_label         , 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.username          , 0, wx.EXPAND                              , 0),
            (password_label         , 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.password          , 0, wx.EXPAND                              , 0),
            (self.ssh_username_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.ssh_username      , 0, wx.EXPAND                              , 0),
            (self.ssh_loc_host_label, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0),
            (self.ssh_loc_host      , 0, wx.EXPAND                              , 0),
        ])
        field_sizer.AddGrowableCol(1)

        self.desc = DescriptionBox(self, style = wx.BORDER_NONE)
        desc_box = wx.StaticBoxSizer(wx.StaticBox(self, label = "Description:"), wx.VERTICAL)
        desc_box.Add(self.desc, 1, wx.EXPAND)

        #self.note = wx.TextCtrl(self, style = wx.TE_MULTILINE|wx.BORDER_NONE)
        #note_box = wx.StaticBoxSizer(wx.StaticBox(self, label = "Notes:"), wx.VERTICAL)
        #note_box.Add(self.note, 1, wx.EXPAND)

        mcp_check          = wx.CheckBox(self, label = "MCP 2.1")
        login_dialog_check = wx.CheckBox(self, label = "Use Login Dialog")
        shortlist_check    = wx.CheckBox(self, label = "On Short List")
        checkbox_sizer     = wx.GridSizer(3, 2, 0, 0)
        checkbox_sizer.AddMany([
            (mcp_check         , 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5),
            (login_dialog_check, 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5),
            (shortlist_check   , 0, wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER_VERTICAL, 5),
        ])

        new_button   = wx.Button(self, label = "New")
        reset_button = wx.Button(self, label = "Reset")
        save_button  = wx.Button(self, label = "Save")

        button_sizer = wx.FlexGridSizer(cols = 3, rows = 1, hgap = 0, vgap = 0)
        button_sizer.AddMany ([
            (new_button  , 0, wx.ALL|wx.ALIGN_RIGHT, 5),
            (reset_button, 0, wx.ALL               , 5),
            (save_button , 0, wx.ALL               , 5),
        ])
        button_sizer.AddGrowableCol(0)

        self.Bind(wx.EVT_BUTTON, self.on_new, new_button)
        self.Bind(wx.EVT_BUTTON, self.on_reset, reset_button)
        self.Bind(wx.EVT_BUTTON, self.on_save, save_button)

        world_details_staticbox = wx.StaticBox(self)
        self.world_details_box  = wx.StaticBoxSizer(world_details_staticbox, wx.VERTICAL)
        self.world_details_box.AddMany ([
            (field_sizer   , 0, wx.ALL|wx.EXPAND, 5),
            (desc_box      , 1, wx.ALL|wx.EXPAND, 5),
            #(note_box      , 1, wx.ALL|wx.EXPAND, 5),
            (checkbox_sizer, 0, wx.EXPAND       , 5),
            (button_sizer  , 0, wx.EXPAND       , 0),
        ])

        main_button_sizer = self.CreateButtonSizer( wx.OK | wx.CANCEL )

        # Hax: change the "OK" button to "Connect"
        # This is a hoop-jumping exercise to use the platform-specific locations
        # of "OK" and "Cancel" instead of the hoop-jumping exercise of making my
        # own buttons.  There's almost certainly a better way to do this.
        for b in main_button_sizer.GetChildren():
            bwin = b.GetWindow()
            if (not bwin) or (bwin.GetLabel() != '&OK'): continue
            bwin.SetLabel('&Connect')
            break

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.world_details_box, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        main_sizer.Add(main_button_sizer     , 0, wx.EXPAND | wx.ALL            , 5)

        last_world_name = prefs.get('last_world')
        last_world = self.world_picker.FindString(last_world_name)
        # if we no longer have that world, go back to the top of the list
        if last_world < 0:
            last_world_name = self.world_picker.GetString(0)
            last_world = self.world_picker.FindString(last_world_name)

        self.world_picker.SetSelection(last_world)
        self.fill_thyself()

        self.SetSizerAndFit(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.Bind(wx.EVT_CHOICE, self.select_world, self.world_picker)
        self.Bind(wx.EVT_CHOICE, self.show_ssh_fields_if_appropriate, self.conntype)
        self.Bind(wx.EVT_BUTTON, self.on_connect, id = wx.ID_OK)

        self.show_ssh_fields_if_appropriate()


    def select_world(self, evt):
        self.fill_thyself()

    # TODO - make wxpymoo.World have a notion of "connect to yourself"
    # Also therefore merge wxpymoo.world and wxpymoo.window.world
    def on_connect(self, evt):
        world = worlds[self.world_picker.GetStringSelection()]
        self.parent.openWorld(world)
        self.Hide()

    def on_save (self, evt):
        world = worlds[self.world_picker.GetStringSelection()]

        world['host'] = self.host.GetValue()
        world['port'] = self.port.GetValue()
        world['conntype'] = self.conntype.GetStringSelection()
        world['username'] = self.username.GetValue()
        world['password'] = self.password.GetValue()
        world['desc'] = self.desc.GetOpenedPage()
        #world['note'] = welf.note.GetValue()

        if world['conntype'] == 2:  # ssh fwd
            world['ssh_username'] = self.ssh_username.GetValue()
            world['ssh_loc_host'] = self.ssh_loc_host.GetValue()
        else:
            world['ssh_username'] = ''
            world['ssh_loc_host'] = ''

        world.save() # TODO - error checking, like at all

    def on_reset(self, evt):
        # repopulate with the data from the World as last saved
        self.fill_thyself()

    def on_new  (self, evt):
        print("TODO: got a 'new' button click")

    def fill_thyself(self):
        world = worlds[self.world_picker.GetStringSelection()]

        self.host.SetValue(unicode(world.get("host")   ) or "")
        self.port.SetValue(    int(world.get("port")   ) or "")

        self.conntype.SetStringSelection(world.get("conntype") or "Direct")
        self.username.SetValue(    world.get("username") or "")
        self.password.SetValue(    world.get("password") or "")

        desc = unicode(world.get('description'))
        if not desc or desc == "None": desc = ''
        self.desc.SetPage(desc)
        # TODO - figure out how to get the Right Size instead of hard-coded 200px
        self.desc.SetMinSize((1, 200))

        #note = unicode(world.get('note'))
        #if not note or note == "None": note = ''
        #self.note.SetValue(note)

        self.ssh_username.SetValue(world.get("ssh_username") or "")
        self.ssh_loc_host.SetValue(world.get("ssh_loc_host") or "")

        self.show_ssh_fields_if_appropriate()

    def show_ssh_fields_if_appropriate(self, evt = None):
        to_show = self.conntype.GetSelection() == conntypes.index('SSH Fwd')
        self.ssh_username_label.Show(to_show)
        self.ssh_loc_host_label.Show(to_show)
        self.ssh_username.Show(to_show)
        self.ssh_loc_host.Show(to_show)

        self.world_details_box.Layout()
