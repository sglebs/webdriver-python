# pip install paver
# http://paver.github.com/paver/#installation
from paver.easy import *
from paver.setuputils import setup
import os

__author__ = 'mqm'

@task
def model_tests():
    os.system("date; nosetests --with-spec --spec-color; date")