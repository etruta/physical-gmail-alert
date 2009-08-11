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

__version__ = "0.3"

import time
import imaplib
import serial

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
        
        self.serial_port = '/dev/tty.usbserial-A6007WIV'
        
        if debug: print "# Connecting in XBee/Arduino with serial..."
        try:
            self.serial = serial.Serial(self.serial_port, 9600)
        except:
            if debug: print "# ERROR: Connecting in XBee/Arduino with serial..."
        
        try:
            if debug: print "# Connecting in imap gmail server..."
            self.server = imaplib.IMAP4_SSL('imap.gmail.com')
            self.ammount = 0
            self.connect()
        except:
            if debug: print "# ERROR: Connecting in imap gmail server..."
            
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
            
            if self.ammount < select[1][0]:
                for i in range(self.ammount_blink):
                    self.blink()
            
            self.ammount = select[1][0]
            
            time.sleep(self.time_refresh)
            self.verify()
            
        else:
           print "# ERROR: Read Inbox!"
           self.connect()
    
    def blink(self):
	
        if debug: print "BLINK!"
        self.serial.write('H')
        time.sleep(2)
			
	
    def __destroy__(self):
        self.serial.close()
        self.server.close()
        self.server.logout()

if __name__ == "__main__":
    s = GmailAlert()