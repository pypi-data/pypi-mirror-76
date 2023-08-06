#from distutils.core import setup
from setuptools import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = str(f.read())

setup(
  name = 'obify',         # How you named your package folder (MyLib)
  packages = ['obify'],   # Chose the same as "name"
  version = '0.0.2',      # Start with a small number and increase it with every change you make
  license='GNU GPL-v3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library provides a set of data structures that will work on python objects similar to collections framework in java',   # Give a short description about your library
  description_content_type = "text/plain",
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = 'Aman Chourasiya',                   # Type in your name
  author_email = 'aman@amanchourasiya.com',      # Type in your E-Mail
  url = 'https://github.com/amanchourasiya/obify',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/amanchourasiya/obify/archive/v_002.tar.gz',    # I explain this later on
  keywords = ['Collections', 'Objects', 'Data structures'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          #'validators',
          #'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
  ],
)