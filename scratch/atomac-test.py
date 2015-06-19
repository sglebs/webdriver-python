import atomac
atomac.launchAppByBundleId('com.apple.Automator')
automator = atomac.getAppRefByBundleId('com.apple.Automator')
print automator.windows()
window = automator.windows()[0]
print window.AXTitle
print window.getAttributes()
print window.AXIdentifier
print "window._convenienceMatch:"
print window._convenienceMatch('*', 'AXIdentifier', "_NS:09")
sheet = window.sheets()[0]
print sheet
print sheet.AXIdentifier
print sheet.buttons()
close = sheet.buttons('Close')[0]
print close
print close.AXIdentifier
print "sheet._convenienceMatch:"
print sheet._convenienceMatch('*', 'AXIdentifier', "_NS:09")
print close.getActions()
close.Press()