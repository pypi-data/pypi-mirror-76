from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='Math2.0',
  version='0.0.1',
  description='maths library with some intermediate function',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ayush Sharma',
  author_email='ayushsmh2504@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='maths', 
  packages=find_packages(),
  install_requires=[''] 
)