import atomac
atomac.launchAppByBundleId('com.apple.Automator')
automator = atomac.getAppRefByBundleId('com.apple.Automator')
print automator.windows()
window = automator.windows()[0]
print window.AXTitle
print window.getAttributes()
print window.AXIdentifier
print window.AXChildren
sheet = window.sheets()[0]
print sheet
print sheet.AXIdentifier
print sheet.buttons()
close = sheet.buttons('Close')[0]
print close
print close.AXIdentifier
print close.getActions()
print close.getAttributes()
print close.AXTitle
close.Press()