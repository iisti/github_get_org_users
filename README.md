# github_get_org_users
A Python program to retrieve GitHub organisation users.

## Development instructions
### On Windows 10
1. Install WSL (Windows Subsystem Linux (the easiest way to use Linux in Windows)

### Installing Python3 and virtualenv on Debian WSL
1. Clone the repository
       
       git clone https://github.com/iisti/github_get_org_users.git
1. Install Python3 and pip3

       sudo apt-get install python3 python3-pip
1. Install virtualenv using pip3

       pip3 install virtualenv
1. Create virtual environment

       virtualenv github_get_org_users/virtualenv
1. Activate virtual environment

       source github_get_org_users/virtualenv/bin/activate
1. One can check which virtualenv is in use by:

       echo $VIRTUAL_ENV
       /home/iisti/scripts/github_get_org_users/virtualenv
1. Deactivate (just to know how it's done)

       deactivate
       
1. Install modules
        
        # Remember to activate virtualenv before
        pip3 install -r requirements.txt
