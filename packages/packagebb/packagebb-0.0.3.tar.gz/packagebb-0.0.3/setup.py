from setuptools import setup, find_packages

setup(
  name='packagebb',
  version='0.0.3',
  description='A very basic adding library',
  long_description=open('readme.txt').read(),# + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Joshua Lowe',
  author_email='balajibetadur@gmail.com',
  license='MIT', 
#   classifiers=classifiers,
  keywords='adding', 
  packages=['packagebb'], # find_packages(),
  install_requires=[''] 
)