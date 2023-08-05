from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyurban',
  version='0.0.1',
  description='A information collector from Urban Dictionary',
  long_description="This is a module which will help you to get meanings,examples,author names from Urban Dictionary.\n\n\n Example: \n\n import pyurbandictionary\n meaning('Google')\n example('Google') \n author('Google')",
  url='',  
  author='Srijon Kumar',
  author_email='srijonkumar18@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='urbandictionary',
  packages=find_packages(),
  install_requires=['requests','bs4'] 
)
