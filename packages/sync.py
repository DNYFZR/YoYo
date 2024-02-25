# Package Sync 
# Ensure all build dependencies in setup.cfg are installed in the Python environment 

import sys, configparser, subprocess

config = configparser.ConfigParser()
config.read('setup.cfg')
packages = config.get('options', 'install_requires').strip('\n').split('\n')

# Install each package
for package in packages:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
