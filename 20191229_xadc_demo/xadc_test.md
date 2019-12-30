---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.0'
      jupytext_version: 0.8.6
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

```python
from pynq import Overlay, MMIO
import pynq.lib.dma
```

```python
overlay = Overlay('/home/xilinx/rfsoc_demos/20191229_xadc_demo/design_1.bit')
adc = overlay.xadc_wiz_0
```

```python
ADDRESS_RANGE = 0x1000
ADDRESS_OFFSET = 0x10

from pynq import MMIO
# mmio = MMIO(IP_BASE_ADDRESS, ADDRESS_RANGE)

# data = 0xdeadbeef
# self.mmio.write(ADDRESS_OFFSET, data)
# result = self.mmio.read(ADDRESS_OFFSET)
```

```python
for j in range(10):
   print(adc.mmio.read(0x200,length=4) * (503/65536) - 273)
```

```python
help(adc.mmio)
```

```python
(adc.mmio.virt_base)
```

```python

```
