#!/bin/bash

# File to manage the apllication containing important code both Python and command line

cd /Users/apcox/Dropbox/Python/peer_review_ai

# Create a virtual environment
pip3 install virtualenv
virtualenv peerenv
source peerenv/bin/activate

# Reads the current environemnt and creates a requirements.txt file listing # all the required packages and version

pip3 freeze > requirements.txt

# python3 --version
# pwd
# dir
# ls -a
# !printenv


pip3 install -r requirements.txt


#  To run

#  run chmod u+x manage_app.sh from terminal
