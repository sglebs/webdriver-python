import atomac
import time
atomac.launchAppByBundleId('com.apple.calculator')
calc = atomac.getAppRefByBundleId('com.apple.calculator')
time.sleep(2)
window = calc.windows()[0]
print window
print window.AXTitle
print window.getAttributes()
print window.getActions()
print window.AXIdentifier
print window.AXChildren
print window.buttons()
window.sendKeys ("234*2")



# atomac.launchAppByBundleId('com.apple.Automator')
# automator = atomac.getAppRefByBundleId('com.apple.Automator')
# print automator.windows()
# window = automator.windows()[0]
# print window.AXTitle
# print window.getAttributes()
# print window.AXIdentifier
# print window.sheets()
# #print window.AXChildren
# sheet = window.sheets()[0]
# print sheet
# print sheet.AXIdentifier
# #print sheet.AXTitle
# print sheet.AXChildren
# print sheet.buttons()
# close = sheet.buttons('Close')[0]
# print close
# print close.AXIdentifier
# print close.getActions()
# print close.getAttributes()
# print close.AXTitle
# close.Press()