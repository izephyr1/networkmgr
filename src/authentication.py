#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from net_api import scanWifiBssid, connectToSsid

wpa_supplican = "/etc/wpa_supplicant.conf"

class Authentication():
    def button(self):
        cancel = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        cancel.connect("clicked", self.close)
        connect = Gtk.Button(stock=Gtk.STOCK_CONNECT)
        connect.connect("clicked", self.add_to_wpa_supplicant)
        table = Gtk.Table(1, 2, True)
        table.set_col_spacings(10)
        table.attach(connect, 4, 5, 0, 1)
        table.attach(cancel, 3, 4, 0, 1)
        return table

    def close(self, widget):
        self.window.hide()

    def add_to_wpa_supplicant(self, widget):
        pwd = self.password.get_text()
        if self.eap_auth:
            Lock_Wpa_Supplicant(self.ssid, self.bssid, pwd, self.wificard, self.identity.get_text())
        else:
            Lock_Wpa_Supplicant(self.ssid, self.bssid, pwd, self.wificard)
        self.window.hide()

    def on_check(self, widget):
        if widget.get_active():
            self.password.set_visibility(True)
        else:
            self.password.set_visibility(False)

    def use_eap(self, widget):
        if widget.get_active():
            self.eap_auth = True
            self.identity.show()
            self.id_label.show()
        else:
            self.eap_auth = False
            self.identity.hide()
            self.id_label.hide()

    def __init__(self, ssid, bssid, wificard):
        self.wificard = wificard
        self.ssid = ssid
        self.bssid = bssid
        self.window = Gtk.Window()
        self.window.set_title("wi-Fi Network Authentication Required")
        self.window.set_border_width(0)
        # self.window.set_position(Gtk.WIN_POS_CENTER)
        self.window.set_size_request(500, 200)
        # self.window.set_icon_from_file("/usr/local/etc/gbi/logo.png")
        box1 = Gtk.VBox(False, 0)
        self.window.add(box1)
        box1.show()
        box2 = Gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, True, True, 0)
        box2.show()
        # Creating MBR or GPT drive
        title = "Authentication required by %s Wi-Fi Network" % ssid
        label = Gtk.Label("<b><span size='large'>%s</span></b>" % title)
        label.set_use_markup(True)
        pwd_label = Gtk.Label("Password:")
        self.id_label = Gtk.Label("Identity:")
        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.identity = Gtk.Entry()
        eap_auth = Gtk.CheckButton("Use WPA2-EAP to connect.")
        check = Gtk.CheckButton("Show password")
        eap_auth = Gtk.CheckButton("Use WPA2-EAP") 
        eap_auth.connect("toggled", self.use_eap)
        check.connect("toggled", self.on_check)
        table = Gtk.Table(1, 2, True)
        table.attach(label, 0, 5, 0, 1)
        table.attach(self.id_label,  1, 2, 1, 2)
        table.attach(self.identity,  2, 4, 1, 2)
        table.attach(pwd_label, 1, 2, 2, 3)
        table.attach(self.password, 2, 4, 2, 3)
        table.attach(check, 2, 4, 3, 4)
        table.attach(eap_auth, 4, 6, 3, 4)
        box2.pack_start(table, False, False, 0)
        box2 = Gtk.HBox(False, 10)
        box2.set_border_width(5)
        box1.pack_start(box2, False, True, 0)
        box2.show()
        # Add create_scheme button
        box2.pack_end(self.button(), True, True, 5)
        self.window.show_all()
        self.identity.hide()
        self.id_label.hide()


class Open_Wpa_Supplicant():
    def __init__(self, ssid, bssid, wificard):
        ws = '\nnetwork={'
        ws += '\n ssid="%s"' % ssid
        ws += '\n bssid=%s' % bssid
        ws += '\n key_mgmt=NONE\n}'
        wsf = open(wpa_supplican, 'a')
        wsf.writelines(ws)
        wsf.close()
        connectToSsid(ssid, wificard)


class Lock_Wpa_Supplicant():
    def __init__(self, ssid, bssid, pwd, wificard, identity=""):
        if identity != "":
            # /etc/wpa_supplicant.conf written by networkmgr
            ws =  '\nnetwork={'
            ws += '\n ssid="%s"' % ssid
            ws += '\n bssid=%s' % bssid
            ws += '\n key_mgmt=WPA-EAP'
            ws += '\n proto=WPA'
            ws += '\n identity="%s"' % identity
            ws += '\n psk="%s"\n}' % pwd
        elif 'RSN' in scanWifiBssid(bssid, wificard):
            ws = '\nnetwork={'
            ws += '\n ssid="%s"' % ssid
            ws += '\n bssid=%s' % bssid
            ws += '\n key_mgmt=WPA-PSK'
            ws += '\n proto=RSN'
            ws += '\n psk="%s"\n}' % pwd
        elif 'WPA' in scanWifiBssid(bssid, wificard):
            ws = '\nnetwork={'
            ws += '\n ssid="%s"' % ssid
            ws += '\n bssid=%s' % bssid
            ws += '\n key_mgmt=WPA-PSK'
            ws += '\n proto=WPA'
            ws += '\n psk="%s"\n}' % pwd
        else:
            ws = '\nnetwork={'
            ws += '\n ssid="%s"' % ssid
            ws += '\n bssid=%s' % bssid
            ws += '\n key_mgmt=NONE'
            ws += '\n wep_tx_keyidx=0'
            ws += '\n wep_key0=%s\n}' % pwd
        wsf = open(wpa_supplican, 'a')
        wsf.writelines(ws)
        wsf.close()
        connectToSsid(ssid, wificard)

