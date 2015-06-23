import atomac
import time
import pyscreeze
atomac.launchAppByBundleId('com.apple.calculator')
calc = atomac.getAppRefByBundleId('com.apple.calculator')
time.sleep(2)
window = calc.windows()[0]
print window.getAttributes()
print window.AXPosition
print window.AXSize
rect = [window.AXPosition[0], window.AXPosition[1], window.AXSize[0], window.AXSize[1]]
print rect
calc_img = pyscreeze.screenshot(region=rect)
calc_img.load() #important!!!!!
calc_img.save("calc.png", "PNG")
print calc_img
from base64 import encodestring, b64encode
from StringIO import StringIO
buffer_in_memory = StringIO()
calc_img.save(buffer_in_memory, 'PNG')
buffer_in_memory.seek(0)
img_base_64 = b64encode(buffer_in_memory.getvalue())
print img_base_64