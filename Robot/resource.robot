*** Settings ***
Documentation     A resource file with reusable keywords and variables.
...
...               The system specific keywords created here form our own
...               domain specific language. They utilize keywords provided
...               by the imported Selenium2Library.
Library           Selenium2Library

*** Variables ***
${WEB_DRIVER_URL}    http://localhost:4444/wd/hub
${BROWSER}           firefox
${INITIAL URL}       #
${MACOS_APP}         com.apple.calculator

*** Keywords ***
Open App
    Open browser    ${INITIAL URL}     ${BROWSER}     remote_url=${WEB_DRIVER_URL}     desired_capabilities=bundleId:${MACOS_APP}
