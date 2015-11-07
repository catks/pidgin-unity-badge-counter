#!/usr/bin/env python
from gi.repository import Unity, Gio, GObject, Dbusmenu
import dbus, gobject
from dbus.mainloop.glib import DBusGMainLoop
launcher = Unity.LauncherEntry.get_for_desktop_id ("pidgin.desktop")
count=0
lastsignal=-1
def countnotify(account, sender, message, conversation, flags):
    global count
    count+=1
    launcher.set_property("count", count)
    launcher.set_property("count_visible", True)
def view(conv, type):
    print type
    global count 
    global lastsignal
    if (type == 4 & lastsignal == 4): # Corresponds to UNSEEN_STATE_CHANGED and others I can't distinguish now     
      count=0
      launcher.set_property("count_visible", False)
    else:
      lastsignal=type

dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()

bus.add_signal_receiver(countnotify,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ReceivedImMsg")

bus.add_signal_receiver(view,
                        dbus_interface="im.pidgin.purple.PurpleInterface",
                        signal_name="ConversationUpdated") ##Not Work

loop = gobject.MainLoop()
loop.run()
