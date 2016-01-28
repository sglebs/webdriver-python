webdriver-python
================

This is an experiment to implement a [Selenium Remote WebDriver](https://code.google.com/p/selenium/wiki/JsonWireProtocol) in Python, to enable a remote
client in Selenium to drive MacOS Desktop apps (say the Calculator).

#### Install

* git clone <this repo>; cd webdriver-python
* virtualenv ~/venvs/webdriver-python
* . ~/venvs/webdriver-python/bin/activate
* pip install -r requirements.txt


#### Run

##### Webdriver Server
* python rest_server.py
* http://localhost:4444/ping

You should be able to see something like this: {"time": "2015-05-07T12:21:30.208824"}
Now you can use this server as a Remote Web Driver for your apps.

##### FitNesse with Tests
Build first:
```
./gradlew installDist
```
then run a FitNesse server:
```
./build/install/webdriver-python/bin/webdriver-python -p 7070
```

then run a test from FitNesse: http://localhost:7070/WebDriver

You should see test results like this:

![FitNesse - Calculator](fitnesse.png)