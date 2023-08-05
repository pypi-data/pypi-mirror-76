# fw102c.py
#
# Thorlabs FW102C - Six-Position Motorized Filter Wheel - Python interface

# Gilles Simond <gilles.simond@unige.ch>	

# who       when        what
# --------  ----------  -------------------------------------------------
# gsimond   20140922    modified from Adrien.Deline version
#

import io,re,sys
from serial import Serial, SerialException

class FW102C(object):
    """
       Class to control the ThorLabs FW102C filter wheel
       
          fwl = Thorlabs.FW102C(port='COM5')
          fwl.help()
          fwl.command('pos=5')
          fwl.query('pos?')
          fwl.close()
          
       The following table describes all of the available commands and queries:
        *idn?     Get ID: Returns the model number and firmware version
        pos=n     Moves the wheel to filter position n
        pos?      Get current Position
        pcount=n  Set Position Count: Sets the wheel type where n is 6 or 12
        pcount?   Get Position Count: Returns the wheel type
        trig=0    Sets the external trigger to the input mode
        trig=1    Sets the external trigger to the output mode
        trig?     Get current Trigger Mode
        speed=0   Sets the move profile to slow speed
        speed=1   Sets the move profile to high speed
        speed?    Returns the move profile mode
        sensors=0 Sensors turn off when wheel is idle to eliminate stray light
        sensors=1 Sensors remain active
        sensors?  Get current Sensor Mode
        baud=0    Sets the baud rate to 9600
        baud=1    Sets the baud rate to 115200
        baud?     Returns the baud rate where 0 = 9600 and 1 = 115200
        save      This will save all the settings as default on power up
        
    """
    isOpen   = False
    devInfo  = None

    def __init__(self, port, logger):

        self.log = logger

        try:
            self._fw = Serial(port=port, baudrate=115200,
                                  bytesize=8, parity='N', stopbits=1,
                                  timeout=1, xonxoff=0, rtscts=0)
        except  SerialException as ex:
            self.log.error('Port {0} is unavailable: {1}'.format(port, ex))
            return
        except  OSError as ex:
            self.log.error('Port {0} is unavailable: {1}'.format(port, ex))
            return
        self._sio = io.TextIOWrapper(io.BufferedRWPair(self._fw, self._fw, 1),
                       newline=None, encoding='ascii')


        
        self._sio.write(str('*idn?\r'))
        self.devInfo = self._sio.readlines(2048)[1][:-1]

        
        self.log.info(self.devInfo)
        self._sio.write(str('pos?\r'))
        self.pos = self._sio.readlines(2048)[1][:-1]

        self.log.info ('position={}'.format(self.pos))
        self._sio.write(str('pcount?\r'))
        self.pcount = self._sio.readlines(2048)[1][:-1]

        self.log.info ('pcount={}'.format(self.pcount))
        self._sio.write(str('trig?\r'))
        self.trig = self._sio.readlines(2048)[1][:-1]

        self.log.info ('trig={}'.format(self.trig))
        self._sio.write(str('speed?\r'))
        self.speed = self._sio.readlines(2048)[1][:-1]

        self.log.info ('speed= {}'.format(self.speed))
        self._sio.write(str('sensors?\r'))
        self.sensors = self._sio.readlines(2048)[1][:-1]

        self.log.info ('sensors={}'.format(self.sensors))
        self._sio.write(str('baud?\r'))
        self.baud = self._sio.readlines(2048)[1][:-1]

        if self.baud: 
            self.baud = 115200
        else: 
            self.baud = 9600
        self.log.info ('baud= {}'.format(self.baud))
				
        self._sio.flush()
        self.isOpen  = True
    # end def __init__
    
    def help(self):
        print(self.__doc__)
    # end def help
    
    def close(self):
        if not self.isOpen:
            print("Close error: Device not open")
            return "ERROR"
        #end if
        
        self._fw.close()
        self.isOpen = False
        return "OK"
    # end def close
	
    def query(self, cmdstr):
        """
           Send query, get and return answer
        """
        if not self.isOpen:
            self.log.error("Query error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        ans = 'ERROR'
        self._sio.flush()
        res = self._sio.write(str(cmdstr+'\r'))
        if res:
            ans = self._sio.readlines(2048)[1][:-1]
        #print 'queryans=',repr(ans)
        return ans
    # end def query
	
    def command(self, cmdstr):
        """
           Send command, check for error, send query to check and return answer
           If no error, answer value should be equal to command argument value
        """
        if not self.isOpen:
            self.log.error("Command error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        ans = 'ERROR'
        self._sio.flush()
        cmd = cmdstr.split('=')[0]
        res = self._sio.write(str(cmdstr+'\r'))
        ans = self._sio.readlines(2048)
        regerr = re.compile("Command error.*")
        errors = [m.group(0) for l in ans for m in [regerr.search(l)] if m]
        #print 'res=',repr(res),'ans=',repr(ans),cmd
        if len(errors) > 0:
            return errors[0]
        ans = self.query(cmd+'?')
        #print 'ans=',repr(ans),cmd+'?'
        return ans
    # end def command
	
    def getinfo(self):
        if not self.isOpen:
            self.log.error("Getinfo error: Device not open")
            return "DEVICE NOT OPEN"
        #end if
        
        return self.devInfo
    # end def getinfo
	
#end class FW102C

# # Class test, when called directly
# if __name__ == "__main__":
#     fwl = FW102C(port='COM10')
#     if not fwl.isOpen:
#         print("FWL INIT FAILED")
#         sys.exit(2)
#     print('**info',fwl.getinfo())
#     print( '**idn?',fwl.query('*idn?'))
    
#     print( '**pos=5',fwl.command('pos=5'))
#     print( '**pos?',fwl.query('pos?'))
#     print( '**pos=7',fwl.command('pos=7'))
#     print( '**pos?',fwl.query('pos?'))
#     print( '**pos=3',fwl.command('pos=3'))
#     print( '**pos?',fwl.query('pos?'))
#     print( '**pos=6',fwl.command('pos=6'))
#     print( '**pos?',fwl.query('pos?'))
#     print( '**qwzs=3',fwl.command('qwz=3'))
#     print( '**pos?',fwl.query('pos?'))
#     print( fwl.close())