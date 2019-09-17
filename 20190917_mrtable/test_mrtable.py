from pynq import Overlay
import time
import mrtable

bit = Overlay('../mr_table_x1.bit')
bit.mr_table_0.load_table(bit.axi_dma_0)
bit.mr_table_0.start()
time.sleep(5)
bit.mr_table_0.stop()