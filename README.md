# GitHub Get Organisation Users
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
        
### How to use
* Run the program.
  *  During the first run there will be wargnins like "WARNING - No login name github-username found!".
    ~~~
    python3 github_get_org_users.py -c config.ini

    2021-12-16 16:24:40,919 - INFO - Loaded configuration:
    user = github-user
    access_token = <CENSORED>
    organisation_name = myorganization
    output_path = ./output/
    real_names_json = ./output/real_names.json
    log_path = ./logs/
    log_level = debug
    2021-12-16 16:24:40,921 - DEBUG - Starting new HTTPS connection (1): api.github.com:443
    2021-12-16 16:24:41,176 - DEBUG - https://api.github.com:443 "GET /orgs/myorganization/members?per_page=100 HTTP/1.1" 200 None
    2021-12-16 16:24:41,179 - DEBUG - Opening JSON file: ./output/real_names.json
    2021-12-16 16:24:41,182 - DEBUG - Opening JSON file: ./output/real_names.json
    2021-12-16 16:24:41,182 - WARNING - No login name github-username found!
    2021-12-16 16:24:41,182 - WARNING - No login name another-username found!
    2021-12-16 16:24:41,182 - INFO - Writing JSON: ./output/github_unknown_users_20211216-162441.json
    2021-12-16 16:24:41,183 - INFO - Writing JSON: ./output/github_known_users_20211216-162441.json
    2021-12-16 16:24:41,183 - INFO - Writing CSV: ./output/github_known_users_20211216-162441.csv
    ~~~

* 3 files are created in to output folder.
    * github_unknown_users_20211216-162441.json
        * All the users that don't exist in real_names.json
    * github_known_users_20211216-162441.json
        * All known users in JSON format.
    * github_known_users_20211216-162441.csv
        * All known users in CSV format.

* If you want to compare the GitHub users names into real names, you can create real_names.json.
  * Copy the ./output/github_unknown_users_20211216-162441.json to the program root folder and rename it into real_names.json.
    ~~~
    # Check that you are in the program root folder
    pwd
    /home/iisti/scripts/github_get_org_users/
    # Copy and rename the file.
    cp ./output/github_unknown_users_20211216-162441.json ./real_names.json
    ~~~
    
    * Before adding real names into the JSON, github_unknown_users_20211216-162441.json content should be something like:
        ~~~
        {
            "github-username": null,
            "another-username": null
        }
        ~~~
    * After adding the real names the real_names.json should be something liek:
        ~~~
        {
            "github-username": "Firstname Lastname",
            "another-username": "Firstname2 Lastname2"
        }
        ~~~

* Now if one runs the program again, there shouldn't be warnings like "WARNING - No login name github-username found!".
* If the GitHub user name is not in real_names.json, there should be warning bells ringing, is the user valid, or has somebody added user which shouldn't be in the system?
