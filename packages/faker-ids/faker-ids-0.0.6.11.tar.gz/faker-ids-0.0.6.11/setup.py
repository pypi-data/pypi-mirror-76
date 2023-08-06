from setuptools import setup, find_packages

setup(
  name='faker-ids',
  version='0.0.6.11',
  description='Fake id generator. Fetches upto 5 MILLION fake details like firstname, lastnam, emailid and mobile number.',
  long_description=open('readme.txt').read(),# + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Balaji Betadur',
  author_email='balajibetadur@gmail.com',
#   classifiers=classifiers,
  keywords=['fakeid','indians','indian fake ids','faker','fakes','fake ids','python','fake-ids python','fake indian ids python'],
  license='MIT', 
  packages=['faker_ids'], # find_packages(),
  package_dir={'faker_ids': 'faker_ids'},
  package_data={'faker_ids': ['data/*']},
  include_package_data=True,
  install_requires=['pandas'] 
) 