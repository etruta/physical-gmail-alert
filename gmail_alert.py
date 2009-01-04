#!/usr/bin/env python

"""
physical-gmail-alert is a python script that physically alert the arrival of gmails 
Copyright (C) 2008  laboratorio (info@laboratorio.us)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__version__ = "0.1"

import time
import imaplib
import firmata

debug = True

class GmailAlert:
    def __init__(self):
        print """
                #################################
                # PHYSICAL GMAIL ALERT : START  #
                #################################
                """
        
        self.ammount_blink = 3
        self.time_refresh  = 10
        
        if debug: print "# Connecting in arduino..."
        self.arduino = firmata.Arduino('/dev/tty.usbserial-A4001JwZ')
        self.arduino.pin_mode(12, firmata.OUTPUT)        
        
        if debug: print "# Connecting in imap gmail server..."
        self.server = imaplib.IMAP4_SSL('imap.gmail.com')
        self.ammount = 0
        self.connect()
        
    def connect(self):
        
        if debug: print "# Reading file credentials..."
        f = open('credentials.txt', 'r')
        content = f.read()
        credentials = content.split('\n')
        f.close()
        
        if debug: print "# Loging in imap gmail server..."
        login = self.server.login(credentials[0], credentials[1])
        if login[0] == 'OK':
            self.verify()
        else:
            print "# ERROR: Bad credentials!"
        
    def verify(self):
        
        if debug: print "# Verifing Inbox..."
        select = self.server.select()
        if select[0] == 'OK':
            
            if self.ammount != select[1][0]:
                self.ammount = select[1][0]
                for i in range(self.ammount_blink):
                    self.blink()
                
            time.sleep(self.time_refresh)
            self.verify()
            
        else:
           print "# ERROR: Read Inbox!"
           self.connect()
    
    def blink(self):
        if debug: print "BLINK: " + str(self.ammount)
        self.arduino.digital_write(12, firmata.HIGH)
        time.sleep(2)
        self.arduino.digital_write(12, firmata.LOW)
        time.sleep(1)
        
    def __destroy__(self):
        self.server.close();
        self.server.logout();

if __name__ == "__main__":
    s = GmailAlert()