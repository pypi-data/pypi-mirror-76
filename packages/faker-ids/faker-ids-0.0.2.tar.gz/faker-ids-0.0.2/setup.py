from setuptools import setup, find_packages

setup(
  name='faker-ids',
  version='0.0.2',
  description='Fake id generator. Fetches upto 5 MILLION fake details like firstname, lastnam, emailid and mobile number.',
  long_description=open('readme.txt').read(),# + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Balaji Betadur',
  author_email='balajibetadur@gmail.com',
  license='MIT', 
#   classifiers=classifiers,
  keywords=['fakeid','indians','indian fake ids','faker','fakes','fake ids','python','fake-ids python','fake indian ids python'],
  packages=['faker_ids'], # find_packages(),
  install_requires=['pandas','json'] 
) 