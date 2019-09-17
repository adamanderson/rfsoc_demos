import numpy as np
from pynq import Xlnk, DefaultIP
import xrfclk  # A python driver for the onboard clock synthesizer

class MrTable(DefaultIP):
    def __init__(self, description):
        super().__init__(description=description)
        
        self.BUFFER_LENGTH =((1 << 15)*16)
        self.DAC_MAX = (1 << 14-1) - 1
        
        self.MR_TABLE_DW_START_ADDR_REG = 0
        self.MR_TABLE_DW_WRITE_STATE_REG = 1
        self.MR_TABLE_DR_START_REG = 2
        
        self.write(4*self.MR_TABLE_DW_START_ADDR_REG,0x00000000)
        self.write(4*self.MR_TABLE_DW_WRITE_STATE_REG,0)
        self.write(4*self.MR_TABLE_DR_START_REG,0)
        
        self.xlnk = Xlnk()
        self.input_buffer = self.xlnk.cma_array(shape=(self.BUFFER_LENGTH,), dtype=np.int16)
        
        # set clocks
        fclk_1 = 204.8
        fclk_2 = 8*fclk_1
        xrfclk.set_all_ref_clks(fclk_1)


        fs = fclk_2
        ts = 1/fs
        n = np.arange(self.BUFFER_LENGTH)
        f = 14
        kr = f/fs*self.BUFFER_LENGTH
        ki = round(kr)
        fi = fs/self.BUFFER_LENGTH*ki
        y = 4*self.DAC_MAX*np.sin(2*np.pi*fi*n*ts)
        #y = n
        self.y = y.astype(np.int16)

    # Bind this python driver to the relevant IP. Path comes from VLNV in Vivado
    bindto = ['fnal.gov:user:mr_table:1.0']
    
    def load_table(self, dma):
        np.copyto(self.input_buffer,self.y)
        
        # Enable writes on mr_table.
        self.write(4*self.MR_TABLE_DW_WRITE_STATE_REG,1)
        
        # DMA data.
        dma.sendchannel.transfer(self.input_buffer)
        dma.sendchannel.wait()
        
        # Disable writes on mr_table.
        self.write(4*self.MR_TABLE_DW_WRITE_STATE_REG,0)

    def start(self):
#         self.write(4*MR_TABLE_DW_WRITE_STATE_REG,1) # enable writes
        self.write(4*self.MR_TABLE_DR_START_REG,1)       # start Mr. Table
        
    def stop(self):
        self.write(4*self.MR_TABLE_DR_START_REG,0)       # stop Mr. Table
        