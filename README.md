webdriver-python
================

This is an experiment to implement a [Selenium Remote WebDriver](https://code.google.com/p/selenium/wiki/JsonWireProtocol) in Python, to enable a remote
client in Selenium to drive Python Desktop apps (say in [PyQt](https://wiki.python.org/moin/PyQt) ).

#### Install

* git clone <this repo>; cd webdriver-python
* virtualenv ~/venvs/webdriver-python
* . ~/venvs/webdriver-python/bin/activate
* pip install -r requirements.txt


#### Run

* python rest_server.py
* http://localhost:4444/ping

You should be able to see something like this: {"time": "2015-05-07T12:21:30.208824"}
Now you can use this server as a Remote Web Driver for your apps.

