# Library
import pyvisa

class power_control():
    def __init__(self):
        self.vlim = 0
        self.ilim = 0
        self.V = 0
        self.I = 0
        self.volt = 0
        self.curr = 0
        self.rm = pyvisa.ResourceManager()
        print(self.rm.list_resources())
        list = self.rm.list_resources()
        self.my_instrument = self.rm.open_resource(list[0])
        print(self.my_instrument.query('*IDN?'))
       

    def getData_V(self,vlim):
        self.vlim = vlim

    def getData_I(self,ilim):
        self.ilim = ilim

    def getData_VD(self,V):
        self.V = V

    def getData_ID(self,I):
        self.I = I

    def reset(self):
        self.my_instrument.write('*RST')
        print('reset!')

    def set_VI_lim(self):
        U ='ULIM '+str(self.vlim)
        I = 'ILIM '+str(self.ilim)
        self.my_instrument.write(U)
        #self.my_instrument.write('DELAY 10.00')
        self.my_instrument.write(I)
        print(U)
        print(I)

    def set_VI(self):
        #if (self.V > self.vlim) or (self.I > self.ilim):
         #   print('invalid')
        #else:
            #U ='USET '+str(self.V)
            #I = 'ISET '+str(self.I)
        #self.V=10
        print(self.V)
        print(self.I)
        
        self.my_instrument.write("USET %f" %self.V)
       
        self.my_instrument.write("ISET %f" %self.I)
        self.my_instrument.write("OUTPUT ON")
            #print(U)
           # print(I)

    def read_VI(self):
        #self.my_instrument.write('DELAY 10.00')
        self.volt = self.my_instrument.query('UOUT?')
        print(self.my_instrument.query('UOUT?'))
        print(self.my_instrument.query('IOUT?'))
        #self.my_instrument.write('DELAY 10.00')
        self.curr = self.my_instrument.query('IOUT?')
        return self.volt, self.curr
