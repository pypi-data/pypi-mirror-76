from setuptools import setup, find_packages

setup(
  name='faker-ids',
  version='0.0.1',
  description='Fake indian id generator.',
  long_description=open('readme.txt').read(),# + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Balaji Betadur',
  author_email='balajibetadur@gmail.com',
  license='MIT', 
#   classifiers=classifiers,
  keywords='fakeid', 
  packages=['faker_ids'], # find_packages(),
  install_requires=['pandas','json'] 
) 