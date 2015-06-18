from selenium import webdriver
cap = {
'device' : 'iphone',
'language': 'en',
'locale': 'en_US',
'CFBundleName': 'InternationalMountains',
'simulator':True,
'variation':'iPhone5s'
}
driver = webdriver.Remote("http://localhost:5555/wd/hub", cap)
# cells = driver.find_elements_by_class_name ("UIATableCell")
# print len(cells)
#print cells
# for cell in cells:
#     print cell

cellByName = driver.find_element_by_name ("Mountain 1")
print (cellByName)
cellByName.click()

# cellByXPath = driver.find_element_by_xpath ("//UIATableCell[contains(@name,'Mountain 1')]")
# print (cellByXPath)
# cellByXPath.click()

driver.close()