*** Settings ***
Documentation     A test suite with a single test for multiplication
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Resource          resource.robot

*** Test Cases ***
Correct Multiplication
    Open App  calc.exe
    click element  name=clear
    click element  name=seven
    click element  name=three
    click element  name=multiply
    click element  name=four
    click element  name=equals
    capture page screenshot
    [Teardown]    Close Browser