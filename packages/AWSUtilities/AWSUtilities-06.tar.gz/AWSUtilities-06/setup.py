from distutils.core import setup
setup(
  name = 'AWSUtilities',         # How you named your package folder (MyLib)
  packages = ['AWSUtilities'],   # Chose the same as "name"
  version = '06',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Basic S2 helper functions used for various projects',   # Give a short description about your library
  author = 'Mark Ruse',                   # Type in your name
  author_email = 'mark.ruse@live.com',      # Type in your E-Mail
  url = 'https://github.com/MarkRuse/AWSUtilities',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/MarkRuse/AWSUtilities/archive/v_03.tar.gz',    # I explain this later on
  keywords = ['AWS', 'Utility', 'S3'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
	'boto3',
	'botocore' ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
