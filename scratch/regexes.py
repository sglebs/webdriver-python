__author__ = 'mqm'

import re
import atomac
import time

#atomac.launchAppByBundleId('com.apple.mail')
mail = atomac.getAppRefByBundleId('com.apple.mail')
time.sleep(2)
window = mail.windows()[0]
print window
#input = "AXToolbar/AXButton"
#input = "AXToolbar/AXButton[2]"
#input = 'AXToolbar/AXButton[name=New Message]'
#input = '/AXWindow[1]/AXToolbar/AXButton[name=New Message]'
#input = '/AXWindow[title=New Message]/AXTextField[4]'
input = '/AXWindow[title=New Message]/AXScrollArea/AXWebArea/AXStaticText'


parts = input.split('/')
current_node = window
for part in parts:
    print part
    if current_node is None:
        break
    if part == "":
        current_node = mail
        continue
    search_result_like_array = re.search('(\w+)[[]?(\d+)[]]?', part)
    search_result_like_property= re.search('(\w+)[[]?(\w+)=([^]]+)[]]?', part)
    if search_result_like_array is not None:
        role = search_result_like_array.group(1)
        index = int(search_result_like_array.group(2))
        current_node = current_node.findAll(AXRole=role)[index-1]
    elif search_result_like_property is not None:
        role = search_result_like_property.group(1)
        prop_name = search_result_like_property.group(2)
        prop_value = search_result_like_property.group(3)
        if prop_name == "name":
            current_node = current_node.findFirst(AXRole=role, AXDescription=prop_value)
        elif prop_name == "id":
            current_node = current_node.findFirst(AXRole=role, AXIdentifier=prop_value)
        elif prop_name == "title":
            current_node = current_node.findFirst(AXRole=role, AXTitle=prop_value)
        else:
            current_node = current_node.findFirst(AXRole=part)
    else:
        current_node = current_node.findFirst(AXRole=part)
    print current_node
print current_node
print current_node.getActions()
print current_node.getAttributes()
print current_node.AXDescription
print current_node.AXIdentifier
