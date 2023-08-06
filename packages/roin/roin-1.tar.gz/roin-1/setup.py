from setuptools import setup
ins='''pygame
pyttsx3
pywin32
comtypes
pygame-gui
keyboard
wheel
Js2Py
selenium
chromedriver-autoinstaller
html2text
requests
opencv-python'''
setup(
    name='roin',
    version='1',
    description='This is just a module for easier installation of Rosehip dependencies',
    install_requires=ins.split('\n'),
    url='https://github.com/donno2048/Rosehip',
    author='Elisha Hollander'
)