import atomac
atomac.launchAppByBundleId('com.apple.Automator')
automator = atomac.getAppRefByBundleId('com.apple.Automator')
print automator.windows()
window = automator.windows()[0]
print window.AXTitle
print window.getAttributes()
print window.AXIdentifier
sheet = window.sheets()[0]
print sheet
close = sheet.buttons('Close')[0]
print close.getActions()
close.Press()